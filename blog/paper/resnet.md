<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-MML-AM_CHTML"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>

# ResNet

*2021.07.08*

> ResNet网络是在2015年由微软实验室提出，斩获当年ImageNet竞赛中分类任务第一名，目标检测第一名。获得COCO数据集中目标检测第一名，图像分割第一名。总之就是一篇很厉害的论文
>
> 链接 [[1512.03385\] Deep Residual Learning for Image Recognition (arxiv.org)](https://arxiv.org/abs/1512.03385)

## 1 问题

传统的卷积神经网络都是通过将一系列卷积层与下采样层进行堆叠得到的。但是当堆叠到一定网络深度时，就会出现两个问题。1）梯度消失或梯度爆炸。 2）退化问题(degradation problem)

梯度消失或梯度爆炸问题，可以引入BN解决，退化问题也就是本文最大的亮点。

### 1.1 退化问题

原文中描述的退化问题

> When  deeper  networks  are  able  to  start  converging,  adegradationproblem has been exposed:  with the networkdepth increasing, accuracy gets saturated (which might beunsurprising)  and  then  degrades  rapidly.Unexpectedly,such degradation isnot caused by overfitting,  and addingmore layers to a suitably deep model leads tohigher train-ing error, as reported in [11, 42] and thoroughly verified byour experiments. Fig. 1 shows a typical example

网络深度增加时，网络准确度出现饱和，甚至出现下降。这个现象可以在下图中直观看出来：56层的网络比20层网络效果还要差。这不会是过拟合问题，因为56层网络的训练误差同样高。我们知道深层网络存在着梯度消失或者爆炸的问题，这使得深度学习模型很难训练。但是现在已经存在一些技术手段如BatchNorm来缓解这个问题。因此，出现深度网络的退化问题是非常令人诧异的。

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/resnet_fig1.png" style="zoom:50%;" />

## 2 残差



<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/resnet_residual.png" style="zoom:50%;" />

## 3 网络结构



<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/resnet_arch.png" style="zoom:50%;" />

其他层数的完整参数可以参考下图

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/resnet_params.png" style="zoom:50%;" />

