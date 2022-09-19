# Tensorboard

- ##### 安装

```bash
pip install torch torchvision
pip install tensorboard
```

- ##### 引入包

```python
import torch
from torch.utils.tensorboard import SummaryWriter

# 默认文件夹是当前文件所在目录下的 'runs/'
writer = SummaryWriter()
```

- ##### 写入想要数据

```python
x = torch.arange(-5, 5, 0.1).view(-1, 1)
y = -5 * x + 0.1 * torch.randn(x.size())

model = torch.nn.Linear(1, 1)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)

def train_model(iter):
    for epoch in range(iter):
        y1 = model(x)
        loss = criterion(y1, y)
        # 写入想要记录的数据
        writer.add_scalar("Loss/train", loss, epoch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

train_model(10)
writer.flush()  # make sure that all pending events have been written to disk.
writer.close()  # if you do not need the summary writer anymore
```

- ##### **运行tensorboard**

```
# 运行文件后，文件所在目录下多出runs文件夹，文件所在目录下运行下面命令
tensorboard --logdir=runs

# 需要多个tensorboard同时保存时，可以自定义查看指定文件夹下内容
tensorboard --logdir=runs/name

# 同时运行多个tensorboard时，可以修改端口
tensorboard --logdir=runs/name --port=6007

# 访问远程服务器tensorboard 简单一点的方法
tensorboard --logdir=runs/name --bind_all
```

![image-20210107175232368](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210107175232.png)

- **图片添加**：代码引自引用2

```python
# 添加图片
writer.add_image('four_fashion_mnist_images', img_grid)
```

![](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210107181204.png)

- **模型添加**：代码引用2

```python
# 查看当前模型，点击模型还可以查看详细结构
writer.add_graph(net, images)
```

![image-20210107181627789](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210107181627.png)

> 对于其他用法官网文档解释的很清晰

**[Reference]**

[1] [HOW TO USE TENSORBOARD WITH PYTORCH](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html)

[2] [VISUALIZING MODELS, DATA, AND TRAINING WITH TENSORBOARD](https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html)

[3] [torch.utils.tensorboard](https://pytorch.org/docs/stable/tensorboard.html)

