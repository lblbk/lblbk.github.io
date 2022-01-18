# pytorch常用函数

##### nelement()

pytorch中的 nelement() 可以统计 tensor (张量) 的元素的个数

```python
import torch
 
x = torch.tensor([[1.], [2], [3]])
print(x.nelement())  # 3
```

##### 初始化矩阵

```python
# 处理图片普遍都是三维 chw 需要用这个函数打包
t1 = torch.zeros([2, 3, 3])
t2 = torch.ones([2, 3, 3])

# output
tensor([[[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.]],

        [[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.]]])
tensor([[[1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]],

        [[1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]]])
```

##### torch.stack()

```python
torch.stack((t1, t2), dim=0)
torch.stack((t1, t2), dim=0).shape
# output
tensor([[[[0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.]],
         [[0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.]]],

        [[[1., 1., 1.],
          [1., 1., 1.],
          [1., 1., 1.]],
         [[1., 1., 1.],
          [1., 1., 1.],
          [1., 1., 1.]]]])
torch.Size([2, 2, 3, 3])

torch.stack((t1, t2), dim=1)
torch.stack((t1, t2), dim=1).shape
# output
tensor([[[[0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.]],
         [[1., 1., 1.],
          [1., 1., 1.],
          [1., 1., 1.]]],

        [[[0., 0., 0.],
          [0., 0., 0.],
          [0., 0., 0.]],
         [[1., 1., 1.],
          [1., 1., 1.],
          [1., 1., 1.]]]])
torch.Size([2, 2, 3, 3])

torch.stack((t1, t2), dim=2)
torch.stack((t1, t2), dim=2).shape
# output
tensor([[[[0., 0., 0.],
          [1., 1., 1.]],
         [[0., 0., 0.],
          [1., 1., 1.]],
         [[0., 0., 0.],
          [1., 1., 1.]]],

        [[[0., 0., 0.],
          [1., 1., 1.]],
         [[0., 0., 0.],
          [1., 1., 1.]],
         [[0., 0., 0.],
          [1., 1., 1.]]]])
torch.Size([2, 3, 2, 3])
```

##### torch.cat()

```python
torch.cat((t1, t2), dim=0)
torch.cat((t1, t2), dim=0).shape
#output
tensor([[[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.]],
        [[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.]],

        [[1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]],
        [[1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]]])
torch.Size([4, 3, 3])

torch.cat((t1, t2), dim=1)
torch.cat((t1, t2), dim=1).shape
# output
tensor([[[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.],
         [1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]],

        [[0., 0., 0.],
         [0., 0., 0.],
         [0., 0., 0.],
         [1., 1., 1.],
         [1., 1., 1.],
         [1., 1., 1.]]])
torch.Size([2, 6, 3])

torch.cat((t1, t2), dim=2)
torch.cat((t1, t2), dim=2).shape
# output
tensor([[[0., 0., 0., 1., 1., 1.],
         [0., 0., 0., 1., 1., 1.],
         [0., 0., 0., 1., 1., 1.]],

        [[0., 0., 0., 1., 1., 1.],
         [0., 0., 0., 1., 1., 1.],
         [0., 0., 0., 1., 1., 1.]]])
torch.Size([2, 3, 6])
```

> 简单来看 `stack()` 会使得合并矩阵升维，`cat()` 并不会

##### contiguous()

PyTorch 提供了**`is_contiguous`、`contiguous`**(形容词动用)两个方法 ，分别用于判定Tensor是否是 **contiguous** 的，以及保证Tensor是**contiguous**的

**1. `torch.view`**等方法操作需要连续的Tensor。

transpose、permute 操作虽然没有修改底层一维数组，但是新建了一份Tensor元信息，并在新的元信息中的 重新指定 stride。**`torch.view`** 方法约定了不修改数组本身，只是使用新的形状查看数据。如果我们在 transpose、permute 操作后执行 view，Pytorch 会抛出以下错误：

```bash
invalid argument 2: view size is not compatible with input tensor's size and stride (at least one dimension 
spans across two contiguous subspaces). Call .contiguous() before .view(). 
at /Users/soumith/b101_2/2019_02_08/wheel_build_dirs/wheel_3.6/pytorch/aten/src/TH/generic/THTensor.cpp:213
```

```python
>>>t = torch.arange(12).reshape(3,4)
>>>t
tensor([[ 0,  1,  2,  3],
        [ 4,  5,  6,  7],
        [ 8,  9, 10, 11]])
>>>t.stride()
(4, 1)
>>>t2 = t.transpose(0,1)
>>>t2
tensor([[ 0,  4,  8],
        [ 1,  5,  9],
        [ 2,  6, 10],
        [ 3,  7, 11]])
>>>t2.stride()
(1, 4)
>>>t.data_ptr() == t2.data_ptr() # 底层数据是同一个一维数组
True
>>>t.is_contiguous(),t2.is_contiguous() # t连续，t2不连续
(True, False)
```

**view 仅在底层数组上使用指定的形状进行变形**

使用**`contiguous`**方法后返回新Tensor t3，重新开辟了一块内存，并使用照 t2 的按行优先一维展开的顺序存储底层数据。

```python
>>>t3 = t2.contiguous()
>>>t3
tensor([[ 0,  4,  8],
        [ 1,  5,  9],
        [ 2,  6, 10],
        [ 3,  7, 11]])
>>>t3.data_ptr() == t2.data_ptr() # 底层数据不是同一个一维数组
False
```

可以发现 t与t2 底层数据指针一致，t3 与 t2 底层数据指针不一致，说明确实重新开辟了内存空间。

***

[PyTorch中的contiguous - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/64551412)