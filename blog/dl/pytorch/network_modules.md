# Pytorch模型层次结构

> 待重写

### 定义模型

```python
# pytorch官网demo
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
# 实例化
net = Net()
```

### `Module` 类方法

> 带 `name` 的方法返回时多返回一个方法的名字

**`print(net)` 打印模型层次结构 **

```
Net(
  (conv1): Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))
  (conv2): Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=576, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=84, bias=True)
  (fc3): Linear(in_features=84, out_features=10, bias=True)
)
```

**` net.parameters()` 生成器 Returns an iterator over module parameters**

```
# 参数太多 只打印最后一层打印为最后一层参数数值 输出10维
tensor([ 0.0272, -0.0695,  0.0083, -0.0723, -0.0363, -0.0846,  0.0661, -0.0256, 0.0371,  0.0893], requires_grad=True)]
```

**`net.named_parameters()` Returns an iterator over module parameters, yielding both the name of the parameter as well as the parameter itself**

```python
# 与上面的不同在于会多返回一个当前层的名字
('fc3.bias', Parameter containing:
tensor([-0.0598, -0.0401,  0.0233,  0.0968, -0.0460, -0.0998, -0.0466,  0.0392, -0.0838,  0.0012], requires_grad=True)

# 常用的写法
for k, v in net.named_parameters():
    print(k, v)
    
# output 只复制了最后一层 k当前层为名字 v为当前层的参数
fc3.bias Parameter containing:
tensor([ 0.0873, -0.0127, -0.0249, -0.0233,  0.0607,  0.1018,  0.1065, -0.0324, -0.0871, -0.0172], requires_grad=True)

# k为每一层参数 打印更加详细
conv1.weight
conv1.bias
conv2.weight
conv2.bias
fc1.weight
fc1.bias
fc2.weight
fc2.bias
fc3.weight
fc3.bias
```

**` net.modules()` Returns an iterator over all modules in the network**

```python
# 转成list
[Net(
  (conv1): Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))
  (conv2): Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=576, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=84, bias=True)
  (fc3): Linear(in_features=84, out_features=10, bias=True)
  ), 
  Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1)), 
  Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1)), 
  Linear(in_features=576, out_features=120, bias=True), 
  Linear(in_features=120, out_features=84, bias=True), 
  Linear(in_features=84, out_features=10, bias=True)]
  
# net.modules() 获取各个层级模块的其他信息
list(net.modules())[1]
# out 取0的时候为全部层 1的时候为第一层
Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))

# 通过 stride, kernel_size 获取具体参数
list(net.modules())[1].kernel_size
# out
(3, 3)

list(net.modules())[1].stride
# out
(1, 1)
```

**` net.named_modules()`** Returns an iterator over all modules in the network, yielding both the name of the module as well as the module itself

```
[('', Net(
  (conv1): Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))
  (conv2): Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1))
  (fc1): Linear(in_features=576, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=84, bias=True)
  (fc3): Linear(in_features=84, out_features=10, bias=True)
)), 
('conv1', Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))), 
('conv2', Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1))), 
('fc1', Linear(in_features=576, out_features=120, bias=True)), 
('fc2', Linear(in_features=120, out_features=84, bias=True)), 
('fc3', Linear(in_features=84, out_features=10, bias=True))]
```

>  与上面一种相同使用方式 不同则是 多了一维 因为名字占了一维

**`net._modules` 返回一个字典** 个人一般不用

```
OrderedDict([
('conv1', Conv2d(1, 6, kernel_size=(3, 3), stride=(1, 1))), 
('conv2', Conv2d(6, 16, kernel_size=(3, 3), stride=(1, 1))), 
('fc1', Linear(in_features=576, out_features=120, bias=True)), 
('fc2', Linear(in_features=120, out_features=84, bias=True)), 
('fc3', Linear(in_features=84, out_features=10, bias=True))])
```

**`net.children()` 生成器，模块下所有子模块**

```
[Conv2d(1, 6, kernel_size=(5, 5), stride=(1, 1)), 
MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False), 
Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1)), 
Linear(in_features=256, out_features=120, bias=True), 
Linear(in_features=120, out_features=84, bias=True), 
Linear(in_features=84, out_features=10, bias=True)]
```

**`net.named_children()` 生成器， 所有子模块， 包括名字**

```
[('conv1', Conv2d(1, 6, kernel_size=(5, 5), stride=(1, 1))), 
('pool', MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)), 
('conv2', Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1))), 
('fc1', Linear(in_features=256, out_features=120, bias=True)), 
('fc2', Linear(in_features=120, out_features=84, bias=True)), 
('fc3', Linear(in_features=84, out_features=10, bias=True))]
```

> 返回生成器的时候可以转换为 ` list` 打印出来



***

[Module — PyTorch 1.7.0 documentation](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)