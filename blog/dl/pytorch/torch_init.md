# Pytorch权重初始化

> 权重初始化的目的是防止在深度神经网络的正向（前向）传播过程中层激活函数的输出损失梯度出现爆炸或消失。如果发生任何一种情况，损失梯度太大或太小，就无法有效地向后传播，并且即便可以向后传播，网络也需要花更长时间来达到收敛。
>
> 矩阵乘法是神经网络的基本数学运算。在多层深度神经网络中，一个正向传播仅需要在每层对该层的输入和权重矩阵执行连续的矩阵乘法。这样每层的乘积成为后续层的输入，依此类推

```python
x = torch.ones(512, 512)
for i in range(100):
    a = torch.randn(512, 512)
    x = a @ x
print(x.mean(), x.std())

# output
tensor(nan) tensor(nan)
```

- **均匀分布**
- **正态分布**
- **常数**
- **单位矩阵**
- **正交**
- **稀疏**
- **计算增益**

- **Xavier初始化**

$\pm\frac{\sqrt{6}}{\sqrt{n_i+n_{i+1}}}$

```python
def tanh(x):
    return torch.tanh(x)

def xavier(m, h):
    return torch.Tensor(m, h).uniform_(-1, 1)*math.sqrt(6./(m+h))
```

```python
x = torch.randn(512)
for i in range(100):
    a = xavier(512, 512)
    x = tanh(a @ x)

print(x.mean(), x.std())

# output
tensor(-0.0012) tensor(0.0935)
```

- **kaiming初始化**

$ \frac{\sqrt{2}}{\sqrt{n}} $

```python
def kaiming(m, h):
	return torch.randn(m. h)*math.sqrt(2./m)

def relu(x):
    return x.clamp_min(0.)
```

```python
x = torch.randn(512)
for i in range(100):
    a = kaiming(512, 512)
    x = relu(a @ x)

print(x.mean(), x.std())

# output
tensor(0.3318) tensor(0.4670)
```

***

[torch.nn.init](https://pytorch.org/docs/stable/nn.init.html)

[神经网络中的权重初始化一览：从基础到Kaiming - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/62850258)

[Weight Initialization in Neural Networks: A Journey From the Basics to Kaiming](https://towardsdatascience.com/weight-initialization-in-neural-networks-a-journey-from-the-basics-to-kaiming-954fb9b47c79)