# Pytorch保存模型

### 一、模型的保存与加载

PyTorch中的保存（序列化，从内存到硬盘）与反序列化（加载，从硬盘到内存）

torch.save主要参数： obj：对象 、f：输出路径

torch.load 主要参数 ：f：文件路径 、map_location：指定存放位置、 cpu or gpu

**模型的保存的两种方法：**

```
#  1、保存整个Module
torch.save(net, path)
model.load(path)

#  2、保存模型参数
torch.save(net.state_dict() , path)
# 加载
model.load_state_dict(torch.load(model_path))
```

### 二 模型训练过程保存

将网络训练过程中的网络的权重，优化器的权重保存，以及epoch 保存，便于继续训练恢复

在训练过程中，可以根据自己的需要，每多少代，或者多少epoch保存一次网络参数，便于恢复，提高程序的鲁棒性。

```
checkpoint = {
        "net":model.state_dict(),
        "optimizer":optimizer.state_dict(),
        "epoch":epoch
}
if not os.path.isdir("./models/checkpoint"):
    os.mkdir("./models/checkpoint")
torch.save(checkpoint, './models/checkpoint/ckpt_best_%s.pth' %(str(epoch)))
```

### 三、模型的断点继续训练

```
if RESUME:
    path_checkpoint = "./models/checkpoint/ckpt_best_1.pth"  # 断点路径
    checkpoint = torch.load(path_checkpoint)  # 加载断点
    model.load_state_dict(checkpoint['net'])  # 加载模型可学习参数
    optimizer.load_state_dict(checkpoint['optimizer'])  # 加载优化器参数
    start_epoch = checkpoint['epoch']  # 设置开始的epoch
```

### 四、重点在于epoch的恢复

```
optimizer = torch.optim.SGD(model.parameters(),lr=0.1)
lr_schedule = torch.optim.lr_scheduler.MultiStepLR(optimizer,milestones=[10,20,30,40,50],gamma=0.1)
start_epoch = 9
# print(schedule)


if RESUME:
    path_checkpoint = "./model_parameter/test/ckpt_best_50.pth"  # 断点路径
    checkpoint = torch.load(path_checkpoint)  # 加载断点

    model.load_state_dict(checkpoint['net'])  # 加载模型可学习参数

    optimizer.load_state_dict(checkpoint['optimizer'])  # 加载优化器参数
    start_epoch = checkpoint['epoch']  # 设置开始的epoch
    lr_schedule.load_state_dict(checkpoint['lr_schedule'])

for epoch in range(start_epoch+1,80):

    optimizer.zero_grad()

    optimizer.step()
    lr_schedule.step()


    if epoch %10 ==0:
        print('epoch:',epoch)
        print('learning rate:',optimizer.state_dict()['param_groups'][0]['lr'])
        checkpoint = {
            "net": model.state_dict(),
            'optimizer': optimizer.state_dict(),
            "epoch": epoch,
            'lr_schedule': lr_schedule.state_dict()
        }
        if not os.path.isdir("./model_parameter/test"):
            os.mkdir("./model_parameter/test")
        torch.save(checkpoint, './model_parameter/test/ckpt_best_%s.pth' % (str(epoch)))
```

通过定义start_epoch变量来保证继续训练的时候epoch不会变化