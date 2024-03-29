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

# U-Net

> 原文链接 [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)
>
> 简洁对称的网络结构，效果很不错

#### Introduction

Unet 的初衷是为了解决生物医学图像方面的问题，由于效果确实很好后来现在被广泛的应用在语义分割的各个方向，比如卫星图像分割，工业瑕疵检测等。

#### 网络结构

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/20210808151732.png" alt="unet" style="zoom: 40%;" />

