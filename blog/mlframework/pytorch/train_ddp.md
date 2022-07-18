# Pytorch多gpu训练

讲述大体流程，以及基本训练

比起基本流程训练，这种训练方式需要更改较多，也比较麻烦

## 参数增加

训练的时候需要增加几个参数，用于 `gpu` 之间同步

```python
# 是否启用SyncBatchNorm
parser.add_argument('--syncBN', type=bool, default=True)
# 不要改该参数，系统会自动分配
parser.add_argument('--device', default='cuda', help='device id (i.e. 0 or 0,1 or cpu)')
# 开启的进程数(注意不是线程),不用设置该参数，会根据nproc_per_node自动设置
parser.add_argument('--world-size', default=4, type=int,
                    help='number of distributed processes')
parser.add_argument('--dist-url', default='env://', help='url used to set up distributed training')
```

## 训练

```bash
def train():
  	# 初始化各进程环境
	  init_distributed_mode(args=args)
	  
	  # 参数初始化
	  rank = args.rank  # 主进程运行在哪个显卡
    device = torch.device(args.device)
    batch_size = args.batch_size
    weights_path = args.weights
    args.lr *= args.world_size  # 学习率要根据并行GPU的数量进行倍增
    
    # 给每个rank对应的进程分配训练的样本索引 对 dataset 再包装一下
    train_sampler = torch.utils.data.distributed.DistributedSampler(train_data_set)
    val_sampler = torch.utils.data.distributed.DistributedSampler(val_data_set)
    
    # 将样本索引每batch_size个元素组成一个list 支持batchsize训练
    train_batch_sampler = torch.utils.data.BatchSampler(train_sampler, batch_size, drop_last=True)
    
    # 在指定显卡打印信息
    if rank == 0:
        print('Using {} dataloader workers every process'.format(nw))
    
    # dataloader 还是正常包装
    train_loader = torch.utils.data.DataLoader(train_data_set,
                                               batch_sampler=train_batch_sampler,
                                               pin_memory=True,
                                               num_workers=nw)

    val_loader = torch.utils.data.DataLoader(val_data_set,
                                             batch_size=batch_size,
                                             sampler=val_sampler,
                                             pin_memory=True,
                                             num_workers=nw)
                                             
		# 模型
		model = Model()
		
		# 是否加载预训练模型
		if os.path.exists(weights_path):
        model.load_state_dict(load_weights_dict, strict=False)
    else:
        checkpoint_path = os.path.join(tempfile.gettempdir(), "initial_weights.pt")
        # 如果不存在预训练权重，需要将第一个进程中的权重保存，然后其他进程载入，保持初始化权重一致
        if rank == 0:
            torch.save(model.state_dict(), checkpoint_path)
				# 强制同步
        dist.barrier()
        # 这里注意，一定要指定map_location参数，否则会导致第一块GPU占用更多资源
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        
    # 是否冻结权重
    if args.freeze_layers:
        freeze_layers
    else:
        # 只有训练带有BN结构的网络时使用SyncBatchNorm采用意义
        if args.syncBN:
            # 使用SyncBatchNorm后训练会更耗时
            model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model).to(device)
            
    # 转为DDP模型
    model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.gpu])
    
    # optimizer
    optimizer = optimier()
    
    # loss function
    loss_function = Loss()
    
    # 训练
    for epoch in range(args.epochs):
    		train_sampler.set_epoch(epoch)
    		
    		######
    		# 一个epoch内操作
    		model.train()
    		mean_loss = torch.zeros(1).to(device)
    		optimizer.zero_grad()
    		# 在进程0中打印训练进度
    		if is_main_process():
        		data_loader = tqdm(data_loader)
        for step, data in enumerate(data_loader):
        		images, labels = data
        		pred = model(images.to(device))
            loss = loss_function(pred, labels.to(device))
            loss.backward()
            
            # 多卡同步loss
            loss = reduce_value(loss, average=True)
            mean_loss = mean_loss = (mean_loss * step + loss.detach()) / (step + 1)  # 计算平均损失
    				
    				# 在进程0中打印平均loss
            if is_main_process():
                data_loader.desc = "[epoch {}] mean loss {}".format(epoch, round(mean_loss.item(), 3))

            if not torch.isfinite(loss):
                print('WARNING: non-finite loss, ending training ', loss)
                sys.exit(1)

            optimizer.step()
            optimizer.zero_grad()
        
        # 等待所有进程计算完毕
        if device != torch.device("cpu"):
            torch.cuda.synchronize(device)
    		#####
    		
    		scheduler.step()
				
				# 一次epoch结束 主进程打印一些想要的信息或者保存模型
        if rank == 0:
            tb_writer.add_scalar(tags[0], mean_loss, epoch)
            tb_writer.add_scalar(tags[1], acc, epoch)
            tb_writer.add_scalar(tags[2], optimizer.param_groups[0]["lr"], epoch)

            torch.save(model.module.state_dict(), "./weights/model-{}.pth".format(epoch))
    		
		# 删除临时缓存文件
    if rank == 0:
        if os.path.exists(checkpoint_path) is True:
            os.remove(checkpoint_path)

    cleanup()
```

## 函数

训练脚本中有用到几个函数，这里列出来, 对部分接口包装一下

```python
import torch.distributed as dist


def init_distributed_mode(args):
    if 'RANK' in os.environ and 'WORLD_SIZE' in os.environ:
        args.rank = int(os.environ["RANK"])
        args.world_size = int(os.environ['WORLD_SIZE'])
        args.gpu = int(os.environ['LOCAL_RANK'])
    elif 'SLURM_PROCID' in os.environ:
        args.rank = int(os.environ['SLURM_PROCID'])
        args.gpu = args.rank % torch.cuda.device_count()
    else:
        print('Not using distributed mode')
        args.distributed = False
        return

    args.distributed = True

    torch.cuda.set_device(args.gpu)
    args.dist_backend = 'nccl'  # 通信后端，nvidia GPU推荐使用NCCL
    print('| distributed init (rank {}): {}'.format(
        args.rank, args.dist_url), flush=True)
    dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url,
                            world_size=args.world_size, rank=args.rank)
    dist.barrier()


def cleanup():
    dist.destroy_process_group()


def is_dist_avail_and_initialized():
    """检查是否支持分布式环境"""
    if not dist.is_available():
        return False
    if not dist.is_initialized():
        return False
    return True


def get_world_size():
    if not is_dist_avail_and_initialized():
        return 1
    return dist.get_world_size()


def get_rank():
    if not is_dist_avail_and_initialized():
        return 0
    return dist.get_rank()


def is_main_process():
    return get_rank() == 0


def reduce_value(value, average=True):
    world_size = get_world_size()
    if world_size < 2:  # 单GPU的情况
        return value

    with torch.no_grad():
        dist.all_reduce(value)
        if average:
            value /= world_size

        return value
```

## 启动

启动命令为

```bash
# nproc_per_node 为并行 gpu 数量
python -m torch.distributed.launch --nproc_per_node=8 --use_env train_ddp.py
```

如果要指定使用某几块GPU可使用如下指令

```bash
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.launch --nproc_per_node=2 --use_env train_ddp.py
```



