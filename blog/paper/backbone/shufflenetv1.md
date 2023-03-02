<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
  <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$', '$'], ['\\(', '\\)']]
            }
        });
  </script>
</head>

# ShuffleNetV1

> 轻量级网络的翘楚，与MobileNet系列并处双雄，旷世家出的
>
> https://arxiv.org/pdf/1707.01083.pdf

## 1 简介

神经网络的精度越来越高，而推理性能也在逐渐变慢，在实际应用中不得不在性能与准确率间进行折中。为此，论文对小网络的耗时进行分析，提出了ShuffleNet。论文首先介绍了ShuffleNet的核心操作Channel Shuffle以及Group Convolutions，然后再介绍Shuffle unit的结构，最后介绍ShuffleNet的架构

## 2 亮点

### 2.1 组卷积

组卷积的概念首先在 AlexNet[21] 中引入，用于将模型分布在两个 GPU 上，在 ResNeXt [40] 中已经很好地证明了它的有效性。 Xception [3] 中提出的深度可分离卷积概括了 Inception 系列 [34, 32] 中可分离卷积的思想。 最近，MobileNet [12] 利用深度可分离卷积并在轻量级模型中获得最先进的结果.我们的工作以一种新颖的形式概括了群卷积和深度可分离卷积

> 后续会补充组卷积基本知识

### 2.2 Channel Shuffle Operation

在目前的一些主流网络中，通常使用pointwise卷积进行维度的降低，从而降低网络的复杂度，但由于输入维度较高，pointwise卷积的开销是十分巨大的。对于小网络而言，昂贵的pointwise卷积会带来明显的性能下降，比如在ResNext unit中，pointwise卷积占据了93.4%的计算量。为此，论文引入了分组卷积，首先探讨了两种ShuffleNet的实现：

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-fig1.png" style="zoom:50%;" />

- 图1a是最直接的方法，将所有的操作进行了绝对的维度隔离，但这会导致特定的输出仅关联了很小一部分的输入，阻隔了组间的信息流，降低了表达能力。
- 图1b对输出的维度进行重新分配，首先将每个组的输出分成多个子组，然后将每个子组输入到不同的组中，能够很好地保留组间的信息流。

  图1b的思想可以简单地用channel shuffle操作进行实现，如图1c所示，假设包含$g$组的卷积层输出为$g\times n$维，首先将输出reshape()为$(g, n)$，然后进行transpose()，最后再flatten()回$g\times n$维

### 2.3 ShuffleNet Units

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-fig2.png" style="zoom:50%;" />

基于channel shuffle操作，论文提出了两种ShuffleNet unit，从图2a的基础残差结构开始，中间包含一个$3\times 3$深度卷积进行特征提取：

- 图2b为特征图大小不变的ShuffeNet unit，将开始的$1\times 1$卷积层替换成pointwise分组卷积+channel shuffle操作，第二个pointwise分组卷积的作用是为了恢复到unit的输入维度，方便与shortcut进行element-wise addition。后面的两个卷积操作根据可分离深度卷积论文的建议只接了BN，没有接BN+ReLU。论文尝试了在第二个pointwise分组卷积后面再接一次channel shuffle操作，但并没有提高很多精度。
- 图2c为特征图大小减半的ShuffleNet unit，可用于block间的特征下采样。主要在shortcut中添加$3\times 3$平均池化以及将最后的element-wise addition替换为channel concatenation，增加输出维度且不会带来太多的计算量。

  Shuffle unit的计算是比较高效的，对于$c\times h\times w$的输入，bottleneck的中间维度为$m$，ResNet unit的计算量为$hw(2cm + 9m^2)$FLOPs，ResNeXt unit的计算量为$hw(2cm+9m^2/g)$FLOPs，ShuffleNet unit的计算量为$hw(2cm/g + 9m)$，$g$为卷积的分组数。在同等计算资源情况下，计算量的减少意味着ShuffeNet可以使用维度更多的特征图，这在小网络中十分重要。
  需要注意的是，尽管深度卷积通常有较低的理论复杂度，但在实现时的效率是不高的。为此，ShuffleNet仅对bottleneck中的特征(维度较低)使用深度卷积

## 3 网络结构

ShuffleNet的结构如表1所示，3个不同的stage由ShuffleNet unit堆叠而成，每个stage的首个ShuffleNet unit比较特殊，使用图2c的stride=2结构，特征图大小缩小一倍，channel数增大一倍。其它的ShuffleNet unit使用图2b的结构，bootlneck的维度设定为输出的$1/4$。表1中设计不同分组数的网络，并修改了对应的输出维度，模型大小整体保持在140MFLOPs左右，网络的分组数越大，可设置维度也越大。

网络的设计原则有两个，1）给定计算预算，ShuffleNet 可以使用更广泛的特征图。我们发现这对于小型网络至关重要，因为小型网络通常没有足够数量的通道来处理信息。2）此外，在 ShuffleNet 中，深度卷积仅在瓶颈特征图上执行。尽管深度卷积通常具有非常低的理论复杂度，但我们发现它很难在低功耗移动设备上有效实现，这可能是由于与其他密集操作相比更差的计算/内存访问率。 [3] 中也提到了这样的缺点，它有一个基于 TensorFlow [1] 的运行时库。在 ShuffleNetunits 中，我们有意仅在瓶颈上使用深度卷积，以尽可能地防止开销

分组卷积可以让网络获得更多的通道信息，同时计算量并不会增大太多；相反深度可分离卷积却耗时更长，因此网络只在瓶颈上使用深度可分离卷积。

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-tab1.png" style="zoom:50%;" />

## 4 实验

为了设定不同的网络复杂度，对表1的网络层维度加一个缩放因子$s$，比如ShuffleNet 0.5X为表1的所有层输出维度减少一倍。

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-tab2.png" style="zoom:50%;" />

不同scale的分组和性能，分组越大信息获取也就越完善

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-tab3.png" style="zoom:50%;" />

对比同复杂度的MobileNet性能。

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-tab5.png" style="zoom:50%;" />

对比主流网络的性能

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/shufflenetv1-tab6.png" style="zoom:50%;" />

## 5 结论

ShuffleNet的核心在于使用channel shuffle操作弥补分组间的信息交流，使得网络可以尽情使用pointwise分组卷积，不仅可以减少主要的网络计算量，也可以增加卷积的维度，从实验来看，是个很不错的work。

读相关文档的时候，我突然想到，其实shuffle是对原有可分离卷积的改进而已。MobileNet使用可分离卷积在理论上有较低的计算量和不错的效果，但实际在移动设备没有达到理想的速度。channel shuffle代替非必要的分组卷积，增加了速度，也并没有折损效果。

论文是很早的了，我的文笔也写不那么好，只是在原有博主基础上做了增添而已，但理解起来还是比较简单的。

[ShuffleNetV1/V2简述 轻量级网络 - 晓飞的算法工程笔记 - 博客园 (cnblogs.com)](https://www.cnblogs.com/VincentLee/p/13253536.html)