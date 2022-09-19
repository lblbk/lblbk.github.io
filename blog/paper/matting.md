<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script id="MathJax-script" async src="https://gcore.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>

# Matting

> 深度学习在扣像领域的应用近几年也很火，并且出现了几篇不错的 SOTA 论文，这里简述一下扣像的基础知识。

## 简介

扣像算是一个计算机视觉领域，主要服务于图像和视频。目前的主流视频扣像方法是采用图像的逐帧扣取方法，但随着前段时间 RVM 论文的发布，相信针对视频扣像越来越多的方法。

### 定义

扣像主要在做什么？这里借用 paper with code 的描述的一段话

> **Image Matting** is the process of accurately estimating the foreground object in images and videos. It is a very important technique in image and video editing applications, particularly in film production for creating visual effects. In case of image segmentation, we segment the image into foreground and background by labeling the pixels. Image segmentation generates a binary image, in which a pixel either belongs to foreground or background. However, Image Matting is different from the image segmentation, where in ==some pixels may belong to foreground as well as background, such pixels are called partial or mixed pixels. In order to fully separate the foreground from the background in an image, accurate estimation of the alpha values for partial or mixed pixels is necessary.==

正如标亮部分所说，扣像和图像分割最大的区别在于边缘部分的处理。举个简单的例子就是图像分割的值只有0和1，而扣像的值是0-1, 这里放出两张照片看一下。

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/matting_image.jpg" style="zoom:50%;" />

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/matting_seg.png" style="zoom: 50%;" />

### 原理

$$
I=\alpha F + (1 - \alpha)B
$$

扣像算法的本质都是来源于这个公式，alpha 代表透明度，F 和 B 分别代表前景和背景。

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/matting_3.png" style="zoom: 50%;" />

## 分类

首先，先介绍一个网站 [alpha Matting Evaluation Website](http://www.alphamatting.com/) ，这个网站几乎所有的 SOTA 的 Image Matting 算法

从技术角度来讲，抠图有传统方法和深度学习方法两种；从交互方式来看，抠图包括有交互和无交互两种，有交互的抠图通常需要用户手动提供一个草图（Scratch）或者一个三元图（Trimap）

这里主要讲解传统方法和深度学习的大概区别，讲解之前呢，先讲解一下什么事三元图

### 传统算法

如上图所示，我们的 Input image 想要直接区分前背景是非常复杂的，通常需要一张额外的输入 Trimap ，是我们手工绘制并且预先提供的约束条件，越精确，未知区域内的点就越少，更多前景和背景信息就更容易利用；除此之外还可以减少大量的计算量，真正需要计算的也就是边缘部分。

生成三元图的方法很简单，手绘。

这里可以拿出两篇比较典型的简单介绍一下

#### Poisson Matting

https://www.cs.jhu.edu/~misha/Fall07/Papers/Sun04.pdf

$$
\nabla I=(F-B)\nabla \alpha+\alpha \nabla F + (1-\alpha)\alpha B
$$

in situations in which foreground F and background B are smooth, 也就是前景和背景平滑的时候， $\nabla F$ 和 $\nabla B$ 是趋近于0的。

$$
\nabla \alpha = \frac{1}{F-B} \nabla I
$$

接下来就很简单了，我们能得到一个公式。想办法去最小化这个公式就可以得到答案了。

$$
{\alpha}^*=arg min_{\alpha} \int \int_{p \in \Omega}||\nabla \alpha - \frac{1}{F-B} \nabla I||^2 dp
$$

### 深度学习

近几年 CNN 的急速发展，也让很多人把 CNN 带到了 Image matting 领域，这里就说一下大概思路以及列出几篇论文

#### 老路新用

这是我自己给这类方法的总结，这类方法把传统方法所用的 trimap 直接拿到 CNN 中，利用 CNN 强大的能力直接预测结果。这里就包括

[[1809.01354\] Semantic Human Matting (arxiv.org)](https://arxiv.org/abs/1809.01354)

#### 魔改创新

U2Net

BackgroundMatting V1 V2

MODNet

RVM

