<head><style type="text/css">h1:first-child {display:none;}</style></head>

# CV中Attention机制

- ### Attention机制

> 通俗一点就是，跟人的视觉系统一样，看到一样东西，会有选择的去关注所有信息中的一部分

**传统卷积**
卷积核作为卷积神经网络的核心，通常被看做是在局部感受野上，将空间上（spatial）的信息和特征维度上（channel-wise）的信息进行聚合的信息聚合体。卷积神经网络由一系列卷积层、非线性层和下采样层构成，这样它们能够从全局感受野上去捕获图像的特征来进行图像的描述。

**空间维度**
很多工作被提出来从空间维度层面来提升网络的性能，如Inception结构中嵌入了多尺度信息，聚合多种不同感受野上的特征来获得性能增益；在Inside-Outside网络中考虑了空间中的上下文信息；还有将Attention机制引入到空间维度上等等

- ### SE-Block

**特征通道**
**Squeeze-and-Excitation Networks**（简称**SENet**）。在我们提出的结构中，Squeeze和Excitation是两个非常关键的操作，所以我们以此来命名。我们的动机是希望显式地建模特征通道之间的相互依赖关系。另外，我们并不打算引入一个新的空间维度来进行特征通道间的融合，而是采用了一种全新的“特征重标定”策略。具体来说，就是通过学习的方式来自动获取到每个特征通道的重要程度，然后依照这个重要程度去提升有用的特征并抑制对当前任务用处不大的特征

![image-20210106190713287](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210106190713.png)

> **Sequeeze** ：对各个 `feature map` 进行处理，由 `C*H*W`得到一个 `1*1*C` 的一维向量
>
> **Excitation** ：使用全连接神经网络， 对Sequeeze之后的结果做一个非线性变换。(reduction为缩放参数，可以降低计算量)
>
> **特征重标定**：使用Excitation 得到的结果作为权重，乘到输入特征上

```python
# 源码
class SEBlock(nn.Module):
    """ SE Block Proposed in https://arxiv.org/pdf/1709.01507.pdf 
    """

    def __init__(self, in_channels, out_channels, reduction=1):
        super(SEBlock, self).__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, int(in_channels // reduction), bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(int(in_channels // reduction), out_channels, bias=False),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        b, c, _, _ = x.size()
        w = self.pool(x).view(b, c)
        w = self.fc(w).view(b, c, 1, 1)

        return x * w.expand_as(x)
```

**使用**
![image-20210106191147233](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210106191147.png)

> 个人理解就是对个通道间的权重进行一次再分配，强调有效信息，抑制无效信息

- ### SKNet

*待续*

***

[Reference]

[ImageNet冠军模型SE-Net详解 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/32733549)

[【CV中的Attention机制】最简单最易实现的SE模块 - pprp - 博客园 (cnblogs.com)](https://www.cnblogs.com/pprp/p/12128520.html)

[SKNet(arxiv.org)](https://arxiv.org/pdf/1903.06586.pdf)

[SKNet——SENet孪生兄弟篇 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/59690223)

[SENet和SKNet(附代码) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/76033612)