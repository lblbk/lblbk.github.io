# Pytorch 训练

### 训练

**训练代码** 正常流程 

```python
    for epoch in range(epochs):
        net.train() # train模式
        data_loader = tqdm(train_loader) # tqdm进度条定义
        for idx, (imgs, labels) in enumerate(data_loader):
            optimizer.zero_grad() # 梯度归零
            loss = loss_func(imgs.to(device), labels)
            loss.backward() # 计算梯度
            optimizer.step() # 更新参数
            data_loader.desc = "[epoch {}] mean loss {}".format(epoch, round(loss.item(), 3))
        lr_scheduler.step()
        save_files = {
            'model': net.state_dict(),
            'optimizer': optimizer.state_dict(),
            'lr_scheduler': lr_scheduler.state_dict(),
            'epoch': epoch}
        torch.save(save_files, "model-{}.pth".format(epoch))
```

