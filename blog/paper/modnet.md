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

# MODNet

> 这是一篇效果很不错的扣像论文 地址https://arxiv.org/pdf/2011.11961.pdf

### 简述

这是一篇关于扣像的论文，扣像是一种计算量很高且像素级分割的算法

这篇论文也是和近期几篇扣像论文相同的思路，即采用多个分支分别对边缘和人像细节分别预测，同时为了视频效果更好也提出了两个策略用于优化, 整篇论文的处理流程是这样

![](https://gcore.jsdelivr.net/gh/lblbk/picgo/work/modnetstruct.png)

### 思路

#### 分支

论文将最终蒙版的预测用三个不同的分支分别去预测

- 人像边缘为精细部分, 论文中定义为 D(detail) 分支，大部分情况下是头发丝或者透明部分，这部分比较难预测，作者使用**encoder- decoder**方式去预测
- 人像整体部分为语义部分, 定义为 S(semantic) 分支，即人像整体部分，这部分语义分割方法就能达到不错的效果，所以相对简单, 为了速度这部分用 `32*32` 去预测，造成了整体效果并不好
- F(fusion) 部分，将上述两部分融合，实现最终的预测效果，用了一个比较特殊的损失函数

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/modnet_net.png" style="zoom:80%;" />

#### 损失函数

三分支对应各自的损失函数

S语义部分损失函数, G 部分来源于 ground truth 下采样：

$$
L_{s}=\frac{1}{2}||s_{p} - G(\alpha_{g})||_2
$$

D 细节部分损失函数, $m_d$ 可以理解为 trimap, 不同的是它只有两个值，为了减少计算量，并且增加先验知识：

$$
m_d=dilate(\alpha_p)-erode(\alpha) \\
L_{d}=m_d||d_p - \alpha_g||_1
$$

F 合成损失函数：

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

soc 在 MODNet 中用于 transfer learning 的一种自监督学习策略，主要用在将原模型迁移到一个没有 label 的 domin 时。

具体操作是这样

原模型有三个输出值，利用这三个值来做约束

$$
\tilde{s_p}, \tilde{d_p}, \tilde{\alpha_p} = M(\bar{I})
$$

细节方面

$$
\tilde{m_d}=dilate(\tilde{\alpha_p})-erode(\tilde{\alpha}) \\
loos_1 = \tilde{m_d}*||\tilde{\alpha_p}-\tilde{d_p}||_1
$$

人像整体部分

$$
loss_2 = \frac{1}{2}||Gaussblur(downsample(\tilde{\alpha_p}))-\tilde{s_p}||_2
$$

对于 loss2 , 作者在论文中说会使得 $\tilde{\alpha_p}$ 变模糊，进而使得D分支的 $\alpha$ 也会模糊， 所以在实际训练时先用 M 复制一份 M1 ，并且固定 M1 参数，记 M1 输出 $\tilde{d_p}_1$ ,在原来基础上再加一个约束

$$
L_{dd} = \tilde{m_d}*||\tilde{d_p}_1-\tilde{d_p}||
$$



把上面的三个loss相加也就是我们时所用的所有约束了。

soc 可以视为微调方法，为了让模型更加适应真实世界，在一定程度上可能会增加模型准确度，但跟数据集也有很大关系。

#### OFD

OFD策略是MODNet提出的针对video matting时可能会存在的'闪烁'现象，对于场景变化较慢的视频可以利用前后帧对应位置像素值的平均值作为'闪烁点'的新的像素取值，但是对于场景变化较快的视频，该策略可能会达到适得其反的作用。

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/modnetofd.png" style="zoom:67%;" />

理解起来也比较简单，中间一帧的相同位置像素值对前后两帧值取平均值

### 结论

论文中的效果很好，实际使用的时候发现有几个问题的，对黑色特别敏感，人像整体部分效果并不好，数据集并没有放出。

人像整体部分可以增大语义部分，但因此也会降低速度

> 暂时总结一下