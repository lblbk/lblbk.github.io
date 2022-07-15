<head><style type="text/css">h1:first-child {display:none;}</style></head>

# Pytorch 训练模型

### 定义模型

自定义自己的模型

### 模型信息

查看模型里面的一些信息

### 模型加载

训练的时候需要准备模型，通常情况下是常见 Backbone + 自定义模型，根据任务不同添加不同的自定义模型，但 Backbone 是常见的模型，如 ResNet、VGG、GoogLeNet。

现在训练通常采用迁移学习，在别人训练好的基础上加载模型权重训练自己的任务，这里 Backbone 通常是自己写或者加载 Pytorch 已经写好的模型。

加载完成后，还有个问题，通常最后一层是分类层，或者还需要跟深层次的定制化，这时候就需要对模型更改

代码来自 [RobustVideoMatting/mobilenetv3.py at master · PeterL1n/RobustVideoMatting (github.com)](https://github.com/PeterL1n/RobustVideoMatting/blob/master/model/mobilenetv3.py)

**Pytorch原模型**

```python
class MobileNetV3(nn.Module):
    def __init__(
            self,
            inverted_residual_setting: List[InvertedResidualConfig],
            last_channel: int,
            num_classes: int = 1000,
            block: Optional[Callable[..., nn.Module]] = None,
            norm_layer: Optional[Callable[..., nn.Module]] = None,
            **kwargs: Any
    ) -> None:
        """
        MobileNet V3 main class

        Args:
            inverted_residual_setting (List[InvertedResidualConfig]): Network structure
            last_channel (int): The number of channels on the penultimate layer
            num_classes (int): Number of classes
            block (Optional[Callable[..., nn.Module]]): Module specifying inverted residual building block for mobilenet
            norm_layer (Optional[Callable[..., nn.Module]]): Module specifying the normalization layer to use
        """
# 原模型解释的很清楚了 继承这个类只需要传入两个必要参数inverted_residual_setting last_channel
```

**继承**

```python
# 其实就是基本的类继承
class MobileNetV3LargeEncoder(MobileNetV3):
    def __init__(self, pretrained: bool = False):
      # 在这里可以传入需要的参数
        super().__init__(
            inverted_residual_setting=[
                InvertedResidualConfig(16, 3, 16, 16, False, "RE", 1, 1, 1),
                InvertedResidualConfig(16, 3, 64, 24, False, "RE", 2, 1, 1),  # C1
                InvertedResidualConfig(24, 3, 72, 24, False, "RE", 1, 1, 1),
                InvertedResidualConfig(24, 5, 72, 40, True, "RE", 2, 1, 1),  # C2
                InvertedResidualConfig(40, 5, 120, 40, True, "RE", 1, 1, 1),
                InvertedResidualConfig(40, 5, 120, 40, True, "RE", 1, 1, 1),
                InvertedResidualConfig(40, 3, 240, 80, False, "HS", 2, 1, 1),  # C3
                InvertedResidualConfig(80, 3, 200, 80, False, "HS", 1, 1, 1),
                InvertedResidualConfig(80, 3, 184, 80, False, "HS", 1, 1, 1),
                InvertedResidualConfig(80, 3, 184, 80, False, "HS", 1, 1, 1),
                InvertedResidualConfig(80, 3, 480, 112, True, "HS", 1, 1, 1),
                InvertedResidualConfig(112, 3, 672, 112, True, "HS", 1, 1, 1),
                InvertedResidualConfig(112, 5, 672, 160, True, "HS", 2, 2, 1),  # C4
                InvertedResidualConfig(160, 5, 960, 160, True, "HS", 1, 2, 1),
                InvertedResidualConfig(160, 5, 960, 160, True, "HS", 1, 2, 1),
            ],
            last_channel=1280
        )
				
        # 这里就可以加载与训练模型
        if pretrained:
            self.load_state_dict(load_state_dict_from_url(
                'https://download.pytorch.org/models/mobilenet_v3_large-8738ca79.pth'))
            
				# 删除不需要的层
        del self.avgpool
        del self.classifier
```

**前向**

```python
    def forward_single_frame(self, x):
    		# 模型中的部分层可以通过索引获取 可以直接返回自己想要的层
        x = self.features[0](x)
        x = self.features[1](x)
        f1 = x
        x = self.features[2](x)
        x = self.features[3](x)
        f2 = x
        x = self.features[4](x)
        x = self.features[5](x)
        x = self.features[6](x)
        f3 = x
        x = self.features[7](x)
        x = self.features[8](x)
        x = self.features[9](x)
        x = self.features[10](x)
        x = self.features[11](x)
        x = self.features[12](x)
        x = self.features[13](x)
        x = self.features[14](x)
        x = self.features[15](x)
        x = self.features[16](x)
        f4 = x
        return [f1, f2, f3, f4]
```

**模型打印**

如果模型打印出来大概是这种形式，并没有贴全

```
 MobileNetV3LargeEncoder(
  (features): Sequential(
    (0): ConvBNActivation(
      (0): Conv2d(3, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
      (1): BatchNorm2d(16, eps=0.001, momentum=0.01, affine=True, track_running_stats=True)
      (2): Hardswish()
    )
    (1): InvertedResidual(
      (block): Sequential(
        (0): ConvBNActivation(
          (0): Conv2d(16, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), groups=16, bias=False)
          (1): BatchNorm2d(16, eps=0.001, momentum=0.01, affine=True, track_running_stats=True)
          (2): ReLU(inplace=True)
        )
        (1): ConvBNActivation(
          (0): Conv2d(16, 16, kernel_size=(1, 1), stride=(1, 1), bias=False)
          (1): BatchNorm2d(16, eps=0.001, momentum=0.01, affine=True, track_running_stats=True)
          (2): Identity()
        )
      )
    )
    ...
```

