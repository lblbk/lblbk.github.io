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

# MODNet

> 这是一篇效果很不错的扣像论文 地址https://arxiv.org/pdf/2011.11961.pdf

### 简述

这是一篇关于扣像的论文，扣像是一种计算量很高且像素级分割的算法

这篇论文也是和近期几篇扣像论文相同的思路，即采用多个分支分别对边缘和人像细节分别预测，同时为了视频效果更好也提出了两个策略用于优化, 整篇论文的处理流程是这样

![](https://cdn.jsdelivr.net/gh/lblbk/picgo/work/modnetstruct.png)

### 思路

#### 分支

论文将最终蒙版的预测用三个不同的分支分别去预测

- 人像边缘为精细部分，大部分情况下是头发丝或者透明部分，这部分比较难预测，作者使用**encoder- decoder**方式去预测
- 人像整体部分为语义部分，即人像整体部分，这部分语义分割方法就能达到不错的效果，所以相对简单, 为了速度这部分用 `32*32` 去预测，造成了整体效果并不好
- fusion 部分，将上述两部分融合，实现最终的预测效果，用了一个比较特殊的损失函数

<img src="https://cdn.nlark.com/yuque/0/2021/png/1622145/1618388442455-4a5d7466-154d-404e-acac-c2644b6d0a5b.png" alt="img" style="zoom:67%;" />

#### 损失函数

三分支对应各自的损失函数

语义部分损失函数：

$$
L_{s}=\frac{1}{2}||s_{p} - G(\alpha_{g})||_2
$$

G 部分来源于 ground truth 下采样

细节部分损失函数：

$$
L_{d}=m_d||d_p - \alpha_g||_1
$$

合成损失函数：

由两个损失函数构成

$$
L_{\alpha}=||\alpha_p - \alpha_g||_1 + L_{c}
$$

$$
L_c=\sqrt{c^{i}_{p} - c^{i}_{g}+\epsilon^2}
$$

下面损失函数来源于DIM这篇论文，组合损失，它是真实 RGB 颜色与由真实前景、真实背景和预测的 alpha 遮罩合成的预测 RGB 颜色之间的绝对差异。同样，我们通过使用以下损失函数来近似它

### 策略

#### SOC

可以视为微调方法，为了让模型更加适应真实世界，采用无策略监督的方法进行训练

#### OFD

这是一种后处理方法，为了应对后期视频闪烁效果而提出的一种简单而有效的方法

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/modnetofd.png" style="zoom:67%;" />

理解起来也比较简单，中间一帧的相同位置像素值对前后两帧值取平均值

### 结论

论文中的效果很好，实际使用的时候发现有几个问题的，对黑色特别敏感，人像整体部分效果并不好，数据集并没有放出。

人像整体部分可以增大语义部分，但因此也会降低速度

> 暂时总结一下