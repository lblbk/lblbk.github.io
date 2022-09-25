# 口罩检测

> 以vlog02形式介绍下自己的工作

## 任务

口罩现在已经成为生活的一部分了，如何利用算法实现大概这种效果

<img src="https://fastly.jsdelivr.net/gh/lblbk/picgo/work/project_maskdemo.jpeg" style="zoom:67%;" />

## 算法

很明显是一个目标检测的算法，选用yolov4-tiny

<img src="https://fastly.jsdelivr.net/gh/lblbk/picgo/work/yolov4-tiny.png" style="zoom: 38%;" />

## 训练

这里是很枯燥的活儿...

## 转换

推理框架框架选择 ncnn，路径 yolo -> onnx -> ncnn

## 移植

代码移植 python -> c++

## 部署

装进安卓app里面！可惜我安卓不好...勉强能用

