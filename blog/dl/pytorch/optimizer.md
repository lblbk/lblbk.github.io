# Optimizer

- **`optimizer.zero_grad()`, `loss.backward()`, `optimizer.step()`**

> 训练模型是通常会调用这三个函数

```python
model = Net()
loss_func = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=1e-4)

for epoch in range(1, epochs):
    for step, (inputs, labels) in enumerate(train_loader):
        outputs = model(inputs)
        loss = loss_func(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

- `optimizer.zero_grad()`

`param_groups` : `optimizer` 类初始化时侯创建的一个列表，通常包含 `['params', 'lr', 'momentum', 'dampening', 'weight_decay', 'nesterov']` 这六个键值对

`param_groups['params']` : 模型参数组成的列表，每个参数都是 `torch.nn.parameter.Parameter` 对象

```python
def zero_grad(self, set_to_none: bool = False):
    # Sets the gradients of all optimized :class:`torch.Tensor` s to zero.
	for group in self.param_groups:
            for p in group['params']:
                if p.grad is not None:
                    if set_to_none:
                        p.grad = None
                    else:
                        if p.grad.grad_fn is not None:
                            p.grad.detach_()
                        else:
                            p.grad.requires_grad_(False)
                        p.grad.zero_()
```

> `zero_grad()` 遍历当前传入模型数据的参数，通过 `p.grad.detech_()` 阶段反向传播梯度流，`p.grad.zero_()` 将每个参数的梯度设为0，即清空上一次梯度
>
> 训练通常使用mini-batch方法，梯度不清零的话会与上一批次产生联系，应该写在反向传播和梯度下降之前

- `loss.backward()`

> 计算梯度

- `optimizer.step()`

> 通过梯度下降算法更新参数的值，梯度下降基于梯度，`optimizer.step()` 函数应在 `loss.backward()` 函数之后执行
>
> optimizer只是更新梯度参数，梯度是 `backward()` 方法产生的

***

[1] [Automatic differentiation package - torch.autograd — PyTorch 1.7.0 documentation](https://pytorch.org/docs/stable/autograd.html?highlight=backward#torch.autograd.backward)

