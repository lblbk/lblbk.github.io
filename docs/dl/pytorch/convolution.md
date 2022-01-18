# Convolution

### Conv2d

```python
class torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)
```

##### **假设** 

Conv2d 的输入 input 尺寸为 $(N, C_{in}, H_{in}, W_{in})$，输出 output 尺寸为 $(N, C_{out}, H_{out}, W_{out})$，有: 

$out(N_i, C_{out_j}) = bias(C_{out_j}) + \sum _{k=0}^{C_{in} - 1} weight(C_{out_j}, k) * input(N_i, k)$ 

其中，$*$ 是 [2D cross-correlation](https://en.wikipedia.org/wiki/Cross-correlation) 操作. $N$ - batch size, $C$ - channels 数, $H$ - Hight, $W$ - Width.

##### **in_channels** 

输入的四维张量 `[N, C, H, W]` 中的 `C` 了，**即输入张量的channels数**。这个形参是确定权重等可学习参数的shape所必需的

##### **out_channels** 

期望的四维输出张量的channels数

##### **kernel_size** 

卷积核的大小, 一般我们会使用5x5、3x3这种左右两个数相同的卷积核，因此这种情况只需要写`kernel_size = 5`这样的就行了。如果左右两个数不同，比如3x5的卷积核，那么写作`kernel_size = (3, 5)`，注意需要写一个tuple，而不能写一个列表(list)

##### **stride=1** 

卷积核在图像窗口上每次平移的间隔，即所谓的**步长**

##### **padding=0** 

Pytorch与Tensorflow在卷积层实现上最大的差别就在于padding上
`Padding`即所谓的图像填充，后面的int型常数代表填充的多少（行数、列数），默认为0。**需要注意的是这里的填充包括图像的上下左右**，以`padding = 1`为例，若原始图像大小为`32x32`，那么padding后的图像大小就变成了`34x34`，而不是`33x33`。
Pytorch不同于Tensorflow的地方在于，**Tensorflow**提供的是`padding`的模式，比如`same、valid`，且**不同模式对应了不同的输出图像尺寸计算公式**。而Pytorch则需要手动输入`padding`的数量，当然，**Pytorch这种实现好处就在于输出图像尺寸计算公式是唯一的**

##### **dilation=1** 

是否采用空洞卷积, 默认为1(不采用). 从中文上来讲，这个参数的意义**从卷积核上的一个参数到另一个参数需要走过的距离**，那当然默认是1了，毕竟不可能两个不同的参数占同一个地方吧(为0).
了解更多[Dilated convolution animations](https://github.com/vdumoulin/conv_arithmetic/blob/master/README.md)。

##### **groups** 

控制 inputs 和 outputs 间的关联性(分组). 其中，要求 `in_channels` 和 `out_channels` 必须都可以被 `groups` 整除.

group是用做分组卷积，但是现在用的比较多的是groups = in_channel。当groups = in_channel时，是在做的depth-wise conv.

##### **bias = True**

即是否要添加偏置参数作为可学习参数的一个，默认为True。

##### **padding_mode = ‘zeros’**

即`padding`的模式，默认采用零填充

##### **输出channel公式**


$H_{out} = \frac{H_{in} + 2\times padding[0] - dilation[0] \times (kernel\_size[0] - 1) - 1}{stride[0]} + 1$

$W_{out} = \frac{W_{in} + 2\times padding[1] - dilation[1] \times (kernel\_size[1] - 1) - 1}{stride[1]} + 1$

```python
# input [1, 3, 12, 12] output [1, 8, 8, 256]
x = torch.ones([1, 3, 12, 12])
conv1 = torch.nn.Conv2d(3, 256, 5)
y = conv1(x)  # y [1, 256, 8, 8]

dw = torch.nn.Conv2d(3, 3, 5, groups=3)
pw = torch.nn.Conv2d(3, 256, 1)
z = dw(x)  # [1, 3, 8, 8]
z = pw(z)  # [1, 256, 8, 8]
```



***

[Reference]

[Pytorch的nn.Conv2d（）详解_风雪夜归人o的博客-CSDN博客](https://blog.csdn.net/qq_42079689/article/details/102642610)

[A Basic Introduction to Separable Convolutions](https://towardsdatascience.com/a-basic-introduction-to-separable-convolutions-b99ec3102728)

