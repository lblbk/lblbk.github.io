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

# 量化

> 最近的工作一直在量化上，所以这里先写一篇关于量化的文章，仅作一份自我学习笔记，如果仔细写的话这块儿内容也是非常多

**目录**

- 量化原理
- 量化方法
- Pytorch量化
- GPU量化

## 量化原理

> 咱也不是为了搞学术研究，所以也就不会讲的太深，了解最基本数学公式以及推导，后续会看情况进行更新

刚接触量化通常是在模型部署时遇到的问题，部署模型的优化方法什么蒸馏 剪枝 量化，我在目前遇到的也就是量化。

首先要知道什么是量化，通俗说就是以往用32位 float 类型去表达的数据现在用8位 int 类型去表达。量化我们在做图像处理时也会用到一部分，`uint8 -> float32` 进而再把数据归一化到 0-1 , 这是反量化。而反过来的操作，当把预测的 0-1 的值映射回一张图片时就是量化了。

### 量化公式

这里就借用网上大佬写好的公式了, 这里 r 是浮点数，q 是量化后的定点整数，S 是 scale, 表示实数和整数之间的比例关系, Z 是 zero point, 表示实数中的 0 经过量化后对应的整数, 后面两个是可以根据数据计算出来的

$$
r = S(q-Z)\\
q=round(\frac{r}{S}+Z) \\
S = \frac{r_{max}-r_{min}}{q_{max}-q_{min}} \\
Z = round(q_{max}-\frac{r_{max}}{S})
$$

### 量化操作

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/quantization-proc.jpg" style="zoom: 67%;" />

### 对称量化与非对称量化

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/quantization-mapping.png" style="zoom:50%;" />

### 卷积量化

## 量化方法

> 这里主要讲一些量化的时候常见的方法

## Pytorch量化

> 我用它是最多的，目前也是用它的量化方法来的，所以只能先讲它了

## 代码

这一部分放在另一篇，后续会更新🔗链接

***

[Reference]

[神经网络量化入门--基本原理 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/149659607)

[部署系列——神经网络INT8量化教程第一讲！ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/405571578)

[从TensorRT与ncnn看卷积网络int8量化 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/387072703)