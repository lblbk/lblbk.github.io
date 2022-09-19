<head>
	<style type="text/css">h1:first-child {display:none;}</style>
	<script type="text/javascript" src="https://gcorejs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-MML-AM_CHTML"></script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            tex2jax: {
            skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
            inlineMath: [['$','$']]
            }
        });
    </script>
</head>

# MobileNetV3

> 轻量级网络的翘楚，第三代虽然是通过网络搜索而来，但带来很多新颖的创新点

### 简述

网络搜索技术现在流行，简单理解就是蛮力实验参数，相对而言 resnet mobilenetv2 的设计更显的思路新颖，设计简洁。但网络搜索得到的网络模型在工程落地时可以很好的work.

 ### v3改进

对耗时层重新设计

使用 h-swish 激活函数

使用了 SE 模块

对于SE模块，不再使用sigmoid，而是采用ReLU6(x + 3) / 6作为近似

### 详解

### 网络结构

### 总结