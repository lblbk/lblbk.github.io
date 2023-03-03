<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>
## yolov3 算法理解

> martin
>
> 2023.02.16

目标检测基本还是面试必备知识，这里简单阅读一下论文，主要以代码为主

### paper

`yolo`是一个系列的算法，从诞生之初就一直在迭代升级，先看一下`yolo`的前辈们

#### yolo

yolo 算法采用一个单独的CNN模型实现end-to-end的目标检测，首先将输入图片resize到448x448，然后送入CNN网络，最后处理网络预测结果得到检测的目标。相比R-CNN算法，其是一个统一的框架，其速度更快，而且 yolo 的训练过程也是end-to-end的

<img src="https://npm.elemecdn.com/lblbk-picgo@latest/image/npm/blog-paper-od-yolov3-2.webp" alt="img" style="zoom: 50%;" />

##### yolo 网络

yolo 采用卷积网络来提取特征，然后使用全连接层来得到预测值。网络结构参考GooLeNet模型，包含24个卷积层和2个全连接层, 采用Leaky ReLU激活函数, 最后一层却采用线性激活函数

检测头就是最后的2个全连接层(Linear in PyTorch)，它们是参数量最大的2个层，也是最值得改进的2个层

##### 输出

经过网络之后输出为7\*7\*30的特征图，也就是有49个30维向量, 可以认为将原图划分为7*7的网格，每一个网格对应一个30维的向量

30维数据的前10维，是两个Anchor box的各自5个信息：框的x坐标，框的y坐标，框的宽，框的高，框中有物体的置信度；剩下20维中的任何1维度，是该网格为中心的2个Anchor里的图像为某一个类别的打分, 一共输出98个框, 大概是这么一回事
$$
grid*grid*(2*(4+1)+20)
$$


> 网格只是物体中心点位置的划分之用，并不是对图片进行切片，不会让网格脱离整体的关系

##### nms

##### 损失函数

<img src="https://unpkg.com/lblbk-picgo@latest/image/npm/blog-paper-od-yolov3-3.webp" style="zoom:67%;" />

为何用根号总方误差来当作宽度和高度的损失函数，20个像素点的偏差，对于800\*600的预测框几乎没有影响，此时的IOU数值还是很大，但是对于30\*40的预测框影响就很大。取根号是为了尽可能的消除大尺寸框与小尺寸框之间的差异

#### yolov2

yolov2 的改进在保持检测速度的同时通过提出几种改进策略来提升 yolo 模型的定位准确度和召回率，从而提高mAP。yolov2 的改进策略如图2所示

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/image/npm/blog-paper-od-yolov3-4.png" alt="image-20230224091621100" style="zoom:50%;" />

##### batch normalization

BN能够给模型收敛带来显著地提升，同时也消除了其他形式正则化的必要。作者在每层卷积层的后面加入BN后，在mAP上提升了2%。BN也有助于正则化模型。有了BN便可以去掉用dropout来避免模型过拟合的操作。BN层的添加直接将mAP硬拔了2个百分点，这一操作在yolo_v3上依然有所保留，BN层从v2开始便成了yolo算法的标配

##### High Resolution

简单说就是在ImageNet数据集（224\*224）上预训练Darknet-19网络之后，将ImageNet的数据resize为448\*448，再次训练Darknet-19网络，然后才进行Fine-tune（在Darknet-19后面接上属于YOLOv2的检测layers），并使用448*448的检测数据集进行训练。这样就不会有分辨率适应的问题了

##### Anchor Boxes

YOLOv1最后采用的是全连接层直接对边界框进行预测，其中边界框的宽与高是相对整张图片大小的，而由于各个图片中存在不同尺度和长宽比（scales and ratios）的物体，YOLOv1在训练过程中学习适应不同物体的形状是比较困难的，这也导致YOLOv1在精确定位方面表现较差

YOLOv2借鉴了Faster R-CNN中RPN网络的先验框（anchor boxes，prior boxes，SSD也采用了先验框）策略。RPN对CNN特征提取器得到的特征图（feature map）进行卷积来预测每个位置的边界框以及置信度（是否含有物体），并且各个位置设置不同尺度和比例的先验框，所以RPN预测的是边界框相对于先验框的offsets值（其实是transform值，详细见[Faster R_CNN论文](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1506.01497)），采用先验框使得模型更容易学习。所以YOLOv2移除了YOLOv1中的全连接层而采用了卷积和anchor boxes来预测边界框。为了使检测所用的特征图分辨率更高，移除其中的一个pool层。yolov1 中使用448\*448输入，yolov2 中将其变为了416\*416然后卷积通过步长为32的卷积运算之后变成了13\*13。 这么做是因为奇数维度使得特征图只有一个中心。对于一些大物体，中心点往往落入图片中心，此时使用特征图的一个中心点去预测这些物体的边界框相对容易些

yolov2 对每一个3\*3的窗口选取多个（比如9个）Anchor Box，对每个Anchor Box单独进行分类和位置预测。输出组成包括 $13*13*(1+4+20)*9$，其中9是多少个Anchor Boxes，总数增加为13\*13\*9=1521个Boxes，而YOLOv1中仅为7\*7\*2=98个Boxes。yolov1 中每个cell只预测一套分类概率值（class predictions，其实是置信度下的条件概率值）,供2个boxes共享。YOLOv2使用了anchor boxes之后，每个位置的各个anchor box都单独预测一套分类概率值，这和SSD比较类似（但SSD没有预测置信度，而是把background作为一个类别来处理）

<img src="https://unpkg.com/lblbk-picgo@0.0.5/image/npm/blog-paper-od-yolov3-5.webp" alt="img" style="zoom: 67%;" />

##### Dimension Clusters

Faster RCNN里使用的Anchor Box的高宽是手动设置的先验框，所以不一定能够很好地符合Ground Truth, 在正式进行YOLOv2检测网络进行训练之前对训练集里的所有Ground Truth使用的是[K-means](https://dorianzi.github.io/2019/04/20/K-means/)进行了聚类。距离指标就是box与聚类中心box之间的IOU值：
$$
d(box,centroid) = 1-IOU(box,centroid)
$$
经过作者在COCO和VOC数据集上的实验，最终选取5个聚类中心作为先验框

> 这里具体怎么做的后续可以继续更近一下...挖个坑🐦

##### Direct location prediction

YOLOv2借鉴RPN网络使用anchor boxes来预测边界框相对先验框的offsets，边界框的实际中心位置$(x, y)$需要根据预测的坐标偏移值 $(t_x, t_y)$ 先验框的尺度$(w_a, h_a)$以及中心坐标$(x_a, y_a)$ (特征图每个位置的中心点) 来计算
$$
x = (t_x*w_a)-x_a \\
y = (t_y*h_a)-y_a
$$
但是上面的公式是无约束的，预测的边界框很容易向任何方向偏移，如当 $t_x=1$ 时边界框将向右偏移先验框的一个宽度大小，而当 $t_x=−1$ 时边界框将向左偏移先验框的一个宽度大小，因此每个位置预测的边界框可以落在图片任何位置，这导致模型的不稳定性，在训练时需要很长时间来预测出正确的offsets

YOLOv2弃用了这种预测方式，而是沿用YOLOv1的方法，就是预测边界框中心点相对于对应cell左上角位置的相对偏移值，为了将边界框中心点约束在当前cell中，使用sigmoid函数处理偏移值，这样预测的偏移值在(0,1)范围内（每个cell的尺度看做1）。总结来看，根据边界框预测的4个offsets $t_x$ $t_y$ $t_w$ $t_h$，可以按如下公式计算出边界框实际位置和大小
$$
b_x = \sigma(t_x)+c_x \\
b_y = \sigma(t_y)+c_y \\
b_w = p_w*e^{t_w} \\
b_h = p_h*e^{t_h}
$$
其中 $(c_x, c_y)$ 为cell的左上角坐标，如图5所示，在计算时每个cell的尺度为1，所以当前cell的左上角坐标为 (1,1) 。由于sigmoid函数的处理，边界框的中心位置会约束在当前cell内部，防止偏移过多。而 $p_w$ 和 $p_h$ 是先验框的宽度与长度，前面说过它们的值也是相对于特征图大小的，在特征图中每个cell的长和宽均为1。这里记特征图的大小为 $(W, H)$ （在文中是 (13,13) )，这样我们可以将边界框相对于整张图片的位置和大小计算出来 (4个值均在0和1之间)
$$
b_x = (\sigma(t_x)+c_x)/W \\
b_y = (\sigma(t_y)+c_y)/H \\
b_w = (p_w*e^{t_w})/W \\
b_h = (p_h*e^{t_h})/H
$$
如果再将上面的4个值分别乘以图片的宽度和长度（像素点值）就可以得到边界框的最终位置和大小了。这就是YOLOv2边界框的整个解码过程

<img src="https://pic3.zhimg.com/80/v2-7fee941c2e347efc2a3b19702a4acd8e_1440w.webp" alt="img" style="zoom:67%;" />

##### Darknet-19

YOLOv2采用了一个新的基础模型（特征提取器），称为Darknet-19，包括19个卷积层和5个maxpooling层。Darknet-19与VGG16模型设计原则是一致的，主要采用 3×3 卷积，采用 2×2 的maxpooling层之后，特征图维度降低2倍，而同时将特征图的channles增加两倍。Darknet-19最终采用global avgpooling做预测，并且在 3×3 卷积之间使用 1×1 卷积来压缩特征图channles以降低模型计算量和参数。Darknet-19每个卷积层后面同样使用了batch norm层以加快收敛速度，降低模型过拟合

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/raw/blog-paper-od-yolov3-5.webp" alt="img" style="zoom:67%;" />

##### Fine-Grained Features

SSD使用了多尺度的特征图来分别检测不同大小的物体，前面更精细的特征图可以用来预测小物体。YOLOv2提出了一种passthrough层来利用更精细的特征图

passthrough也就是从原特征图中抽取元素，输出尺寸为1/2倍，通道数为4倍的特征图。4\*4\*1特征图经过passthrough之后变成了2\*2\*4特征图，而非4个2\*2\*1特征图

> 其实就是 torch 中的` pixelshuffle`

对于YOLOv2来说26\*26\*512通过passthrough之后，变成了13\*13\*2048 （尺寸为1/2,通道数为4倍）, 接下来将它（13\*13\*2048的特征）与回到主网络Darknet-19（主网络经过最后一个maxpooling已经得到了13\*13\*1024）汇合，于是输出最终的13\*13\*3072特征图。在这个特征图上，进行预测操作

<img src="https://pic3.zhimg.com/80/v2-c94c787a81c1216d8963f7c173c6f086_1440w.webp" alt="img" style="zoom: 67%;" />

##### Multi-Scale Training

由于YOLOv2模型中只有卷积层和池化层，所以YOLOv2的输入大小可以不作限制，为了增强模型的鲁棒性，YOLOv2采用了多尺度输入训练策略，具体来说就是在训练过程中每间隔一定的iterations之后改变模型的输入图片大小，然后只需要修改对最后检测层的处理就可以重新训练。

##### 损失函数

论文中好像没给出，这里找到第三方实现

https://github.com/thtrieu/darkflow/blob/master/darkflow/net/yolov2/train.py

https://www.cnblogs.com/YiXiaoZhou/p/7429481.html

#### Yolov3

##### Darknet-53

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/image/npm/blog-paper-od-yolov3-7.png" alt="image-20230222234928570" style="zoom:50%;" />

DarkNet53网络使用了更多的卷积——53层卷积, 并添加了残差网络中的残差连结结构，以提升网络的性能的降采样操作，没有使用Maxpooling层，而是由stride=2的卷积来实现。卷积层仍旧是**线性卷积、BN层以及LeakyReLU激活函数**的串联组合，借用网友绘制的图片https://www.cnblogs.com/chenhuabin/p/13908615.html

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/raw/blog-paper-od-yolov3-6.png" style="zoom: 80%;" />

在上述过程中，两次用到上采样和特征堆叠，其中上采用是将小尺寸特征图通过插值等方法，生成大尺寸图像。例如使用最近邻插值算法，将8\*8的图像变换为16\*16，注意，上采样层不改变特征图的通道数。而特征堆叠是指的是concat操作，源于DenseNet网络的设计思路，将特征图按照通道维度直接进行拼接，例如8\*8\*16的特征图与8\*8\*16的特征图拼接后生成8\*8\*32的特征图。

总结而言，经过上述主干网络后，将输出以下三种不同大小的特征图：

- 13×13×75
- 26×26×75
- 52×52×75

##### predictions across scales

借鉴了FPN(feature pyramid networks)，采用多尺度来对不同size的目标进行检测，越精细的grid cell就可以检测出越精细的物体。y1,y2和y3的深度都是255，边长的规律是13:26:52

COCO类别而言，有80个种类。输出是三个分支，所以每个分支输出大概是 $grid*grid*(1+4+80)*3$

##### Bounding Box Prediction

##### 损失函数

### Code

#### darknet

这是一个纯`C`的深度学习框架，精巧好用，简单看过源码

作者关于模型的原版配置文件都是通过`cfg`的文件给出的，就是一个简单的`json`文件，`python`读取后按照指定的规则就可以用`pytorch`创建模型了

---

Reference:

https://zhuanlan.zhihu.com/p/32525231

https://dorianzi.github.io/2019/06/07/YOLO/

https://blog.csdn.net/leviopku/article/details/82660381
