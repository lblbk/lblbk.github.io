<head><style type="text/css">h1:first-child {display:none;}</style><link rel="shortcut icon" href="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cola.svg"></head>

# YUV颜色编码论述

> 这里专有名词和说法太多有些说大可能不是很清楚，我也不是专门搞这个，只是记录平常工作常遇到的问题
>
> Martin 7.27.2022
>

## 概念

YUV是一种颜色编码方法。常使用在各个影像处理组件中。 YUV在对照片或视频编码时，考虑到人类的感知能力，允许降低色度的带宽，和它等同的还有RGB颜色编码方法

## RGB颜色编码

三原色光模式（RGB color model），又称RGB颜色模型或红绿蓝颜色模型，是一种加色模型，将红（Red）、绿（Green）、蓝（Blue）三原色的色光以不同的比例相加，以合成产生各种色彩光

这是我们比较熟悉的颜色编码模式，在计算中大概是以这种方式呈现的

```bash
---------------w------------
[255, 255, 255] [255, 255, 255] [255, 255, 255] 
```

每个像素点值是0-255，所以每个像素是24bit, 也就是3个字节，那么一张1280*720的图片也就是1280\*720\*3/1024/1024=2.63MB, 这么大的数据是非常印象传输速度的

## YUV 颜色编码

### 概念

YUV 颜色编码采用的是 **明亮度** 和 **色度** 来指定像素的颜色。

其中 Y 表示明亮度（Luminance、Luma），也就是灰阶值。

U、V 表示色度（Chrominance 或 Chroma），描述的是色调和饱和度。

YCbCr 其实是 YUV 经过缩放和偏移的翻版。其中 Y 与 YUV 中的 Y 含义一致,Cb,Cr 同样都指色彩，只是在表示方法上不同而已。YCbCr 其中 Y 是指亮度分量，Cb 指蓝色色度分量，而 Cr 指红色色度分量

### 优点

和 RGB 表示图像类似，每个像素点都包含 Y、U、V 分量。但是它的 Y 和 UV 分量是可以分离的，如果没有 UV 分量一样可以显示完整的图像，只不过是黑白的。

对于 YUV 图像来说，并不是每个像素点都需要包含了 Y、U、V 三个分量，根据不同的采样格式，可以每个 Y 分量都对应自己的 UV 分量，也可以几个 Y 分量共用 UV 分量。

### YUV 采样格式

YUV 图像的主流采样方式有如下三种：

- YUV 4:4:4 采样
- YUV 4:2:2 采样
- YUV 4:2:0 采样

这里先放一张他们三种的区别

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv.jpeg" style="zoom:67%;" />

#### YUV 4:4:4

YUV 4:4:4 表示 Y、U、V 三分量采样率相同，即每个像素的三分量信息完整，都是 8bit，每个像素占用 3 个字节

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv444.jpeg" style="zoom:67%;" />

```bash
四个像素为： [Y0 U0 V0] [Y1 U1 V1] [Y2 U2 V2] [Y3 U3 V3]
采样的码流为： Y0 U0 V0 Y1 U1 V1 Y2 U2 V2 Y3 U3 V3
映射出的像素点为：[Y0 U0 V0] [Y1 U1 V1] [Y2 U2 V2] [Y3 U3 V3]
```

#### YUV 4:2:2

YUV 4:2:2 表示 UV 分量的采样率是 Y 分量的一半

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv422.jpeg" style="zoom:67%;" />

```bash
四个像素为： [Y0 U0 V0] [Y1 U1 V1] [Y2 U2 V2] [Y3 U3 V3]
采样的码流为： Y0 U0 Y1 V1 Y2 U2 Y3 U3
映射出的像素点为：[Y0 U0 V1]、[Y1 U0 V1]、[Y2 U2 V3]、[Y3 U2 V3]
```

每采样一个像素点，都会采样其 Y 分量，而 U、V 分量都会间隔采集一个，映射为像素点时，第一个像素点和第二个像素点共用了 U0、V1 分量

一张1280\*720图片所占用空间，(1280\*720\*8 + 1280\*720\*8\*0.5\*2)/8/1024/1024=1.75MB

#### YUV 4:2:0

YUV 4:2:0 指的是对每条扫描线来说，只有一种色度分量以 2:1 的采样率存储，相邻的扫描行存储不同的色度分量。也就是说，如果第一行是 4:2:0，下一行就是 4:0:2，在下一行就是 4:2:0，以此类推

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv420.jpeg" style="zoom:67%;" />

```bash
图像像素为：
[Y0 U0 V0]、[Y1 U1 V1]、 [Y2 U2 V2]、 [Y3 U3 V3]
[Y5 U5 V5]、[Y6 U6 V6]、 [Y7 U7 V7] 、[Y8 U8 V8]

采样的码流为：
Y0 U0 Y1 Y2 U2 Y3 
Y5 V5 Y6 Y7 V7 Y8

映射出的像素点为：
[Y0 U0 V5]、[Y1 U0 V5]、[Y2 U2 V7]、[Y3 U2 V7]
[Y5 U0 V5]、[Y6 U0 V5]、[Y7 U2 V7]、[Y8 U2 V7]
```

其中，每采样一个像素点，都会采样 Y 分量，而 U、V 分量都会隔行按照 2:1 进行采样

一张1280\*720图片所占用空间，(1280\*720\*8 + 1280\*720\*8\*0.25\*2)/8/1024/1024=1.315MB

### YUV 存储格式

YUV 数据有两种存储格式：

- 平面格式 planar format：先连续存储所有像素点的 Y，紧接着存储所有像素点的 U，随后是所有像素点的 V
- 打包格式 packed format：每个像素点的 Y、U、V 是连续交错存储的

不同的采样方式和存储格式，就会产生多种 YUV 存储方式，这里只介绍基于 YUV422 和 YUV420 的存储方式

#### YUYV

YUYV 格式属于 YUV422，采用打包格式进行存储，Y 和 UV 分量按照 2:1 比例采样，每个像素都采集 Y 分量，每隔一个像素采集它的 UV 分量。

> Y0 U0 Y1 V0 Y2 U2 Y3 V2

Y0 和 Y1 共用 U0 V0 分量，Y2 和 Y3 共用 U2 V2 分量。

#### UYUV

UYVY 也是 YUV422 采样的存储格式中的一种，只不过与 YUYV 排列顺序相反。

> U0 Y0 V0 Y1 U2 Y2 V2 Y3

#### YUV422P

YUV422P 属于 YUV422 的一种，它是一种 planer 模式，即 Y、U、V 分别存储。

#### YUV420P YUV420SP

YUV420P 是基于 planar 平面模式进行存储，先存储所有的 Y 分量，然后存储所有的 U 分量或者 V 分量

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv420p.png" style="zoom:75%;" />

同样，YUV420SP 也是基于 planar 平面模式存储，与 YUV420P 的区别在于它的 U、V 分量是按照 UV 或者 VU 交替顺序进行存储

<img src="https://cdn.jsdelivr.net/npm/lblbk-picgo@latest/work/cv-yuv-yuv420sp.png" style="zoom:75%;" />

#### YU12 YU21

YU12 和 YV12 格式都属于 YUV 420P 类型，即先存储 Y 分量，再存储 U、V 分量，区别在于：YU12 是先 Y 再 U 后 V，而 YV12 是先 Y 再 V 后 U 

#### NV21 NV21

NV12 和 NV21 格式都属于 YUV420SP 类型。它也是先存储了 Y 分量，但接下来并不是再存储所有的 U 或者 V 分量，而是把 UV 分量交替连续存储。

NV12 是 IOS 中有的模式，它的存储顺序是先存 Y 分量，再 UV 进行交替存储。

NV21 是 安卓 中有的模式，它的存储顺序是先存 Y 分量，在 VU 交替存储。

## YUV 与 RBG 转换

后续更新