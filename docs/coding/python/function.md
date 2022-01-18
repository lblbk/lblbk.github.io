# Python常用函数

> 记录一些python常用的函数api，以及日常使用小技巧

### 迭代器、生成器

##### 可迭代对象

可以利用 for 循环的对象，都叫可迭代对象，实现有两种方式

```python
# 对象内部实现 __iter__()方法
class myList:
    mylist = [0,1,2]

    # 返回迭代器类的实例
    def __iter__(self):
        return iter(self.mylist)

# 得到可迭代对象
my_list = myList()
print(isinstance(my_list, Iterable)) # True
for i in my_list:
    print(i)

    
# 实现 __getitem()__方法
class myList:
    mylist = [0,1,2]

    def __getitem__(self, item):
        return self.mylist[item]

# 得到一个可迭代对象
my_list = myList()
print(isinstance(my_list, Iterable)) # False isinstance 这种方法就是检查对象是否有 __iter__ 方法
for i in my_list:
    print(i)
```

##### 迭代器

对可迭代对象使用 `iter()` 函数后，返回一个迭代器对象，可使用 `next()` 去元素，全部获取完毕，会抛出 `StopIteration `提示无元素可取

迭代器实现在可迭代对象基础上实现  `__next__()` 函数，

```python
>>> list = [0, 1, 2, 3]
>>> gen = iter(list)
>>> next(gen)
0
>>> next(gen)
1
>>> next(gen)
2
>>> next(gen)
3
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

```python
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
        
>>> rev = iter(Reverse('spam'))
>>> for char in rev:
...     print(char)
...
m
a
p
s
```

**生成器**

一个可以像迭代器那样使用for循环来获取元素的函数, 生成器的出现（Python 2.2 +），实现了延时计算，从而缓解了在大量数据下内存消耗过猛的问题, 会自动创建 `__iter__()`和`__next__()`方法

- 创建

```python
# 列表推导式正常使用
>>> l1 = [i for i in rage(5)]
>>> l1
[0, 1, 2, 3, 4]

# generator 
>>> gen = (i for i in range(5))
>>> gen
<generator object <genexpr> at 0x000002835B6DC648>

# yield()
# 当一个函数运行到 yield 后，函数的运行会暂停，并且会把 yield 后的值返回出去。
# 若 yield 没有接任何值，则返回 None
# yield 虽然返回了，但是函数并没有结束
>>> def gen_func(top=5):
...     index=0
...     while index < top:
...             print(index)
...             index += 1
...             yield index
...     raise StopIteration
...
>>> gen = gen_func()
>>> gen
<generator object gen_func at 0x000002835B8E2848>
```

- 使用

```python
# next()
>>> gen = (i for i in range(3))
>>> gen
<generator object gen_func at 0x000002835B8E2848>
>>> next(gen)
0
>>> next(gen)
1
>>> next(gen)
2
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

# for
>>> gen = (x for x in range(3))
>>> for i in gen:
...     print(i)
...
0
1
2
```

- 激活：生成器对象，在创建后，并不会执行任何的代码逻辑，想要从生成器对象中获取元素，那么第一步要触发其运行，在这里称之为激活

```python
# next()

# generator.send(None) 相当于 next(gen)
def generator_factory(top=5):
     index = 0
     while index < top:
         index = index + 1
         yield index
     raise StopIteration

>>> gen = generator_factory()
>>> gen.send(None)
1
>>> gen.send(None)
2
```

- 状态

```python
# GEN_CREATED # 生成器已创建，还未被激活
# GEN_RUNNING # 解释器正在执行（只有在多线程应用中才能看到这个状态）
# GEN_SUSPENDED # 在 yield 表达式处暂停
# GEN_CLOSED # 生成器执行结束
# inspect包可检测
from inspect import getgeneratorstate
```

### `zip()` `*zip()` `zip(*zipped)`

创建一个聚合了来自每个可迭代对象中的元素的迭代器

`zip()` 与 `*` 运算符相结合可以用来拆解一个列表, 如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同

```python
# zip() *zip()
>>> a = ['a', 'b']
>>> b = [0, 1, 2]
>>> z = zip(a, b)
>>> z
<zip object at 0x00000133FC0F5208>
>>> list(z)
[('a', 0), ('b', 1)]
>>> x, y = zip(*zip(a, b))
>>> x
('a', 'b')
>>> y
(0, 1)
```

```python
# zip(*zipped)  *zipped:可以list, 元组，也可以是zip()函数返回的对象
>>> nums = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
>>> iters = zip(*nums)
>>> iters
<zip object at 0x000002583AF7A688>
>>> list(iters)
[('a1', 'b1'), ('a2', 'b2'), ('a3', 'b3')]
```

### `map()` `reduce()` `sorted()`

```python
# reduce源码 function是将要进行的操作
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value

# reduce(function, iterable[, initializer])
# example
from functools import reduce 
reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
reduce(lambda x, y: x*y, [1, 2, 3, 4, 5])

# output
15
120
```

```python
# map(function_to_apply, list_of_inputs)  返回迭代器
list(map(lambda x: x**2, [1, 2, 3]))
# output [1, 4, 9]
```

### 偏函数 `filter()`

```python
# functools.partial(func, *args, **keywords)
from functools import partial

int2 = partial(int, base=2)
res = int2('10000')
print(res) # 16
```

### 星号 `*` 用法 （一直困扰我）

**乘法运算符** 基本用法

```python
1 * 1
```

**收集列表中多余的值**

```python
a, b, *c = [1, 2, 3, 4]
# a是1，b是2，c是[3, 4] 列表
```

**函数** 用于收集参数或者分配参数

- 定义函数 * 代表收集参数，** 代表收集关键字参数

  - `*` 情况

    ```python
    def myprint(*params):
        print(params)

    myprint(1, 2, 3)  # (1, 2, 3) 作用是将调用时提供的所有值，放在一个元组里
    ```
    
    **跟上面收集多余的值里的有所区别，上面是收集列表中多余的参数，而这里是收集好参数，一起放进元组里面。**
    
    这种情况下，在函数定义时的形参里的 `*params` 后面，就最好不要再加入别的形参了
    
    ```python
    def myprint(*params,x)
    	print(params)
        
    myprint(1, 2, 3)
    
    ###
    Traceback (most recent call last):
      File "F:/MODNet/test.py", line 54, in <module>
        myprint(1, 2, 3)
    TypeError: myprint() missing 1 required keyword-only argument: 'x'
            
    # 解决        
    myprint(1, 2, x=3)  # (1, 2)
    ```
    
    因为这样python分不清哪个数据是给params的。如果你非要这么定义也行，不过在调用的时候，必须显示的指出哪个值是给x的
    
  - `**` 情况

    对于之前参数是*params的情况，myprint并不能传入关键字参数。啥意思呢，就是仍然采取这种方式定义时：

    ```python
    def myprint1(*params):
        print(params)
    ```

    ```python
    >>> myprint1(x=1,y=2,z=3)  #会报错
    ```

    因为*号并不会收集关键字参数。所以需要如下方式修改，采用两个星号：

    ```python
    def myprint2(**params):
        print(params)
    ```

    这样调用myprint2就不会有问题：

    ```python
    >>> myprint2(x=1,y=2,z=3)
    ```

    ```python
    {'z'=3,'x'=1,'y'=2}  # 得到一个**字典**。字典中元素的先后顺序取决于你的环境
    ```

- 调用函数 *和**都是分配参数

  - `*`

    例如，还是刚刚那个print函数

    ```python
    def myprint(x,y):
        print(x)
        print(y)
    ```

    这下形参有两个了，但是我能不能只传入一个形参？

    对，**“调用函数时分配参数”**跟**“定义函数时收集参数”**，**反过来了！**

    假设你还有一个**元组：**

    ```
    params=(1,2)
    ```

    可以通过如下方式调用myprint函数：

    ```python
    >>> myprint(*params)
    # 输出
    1
    2
    ```

    > 搭建网络经常会碰到传入参数 `nn.Sequential(*layers)` , 通过debug查看 `layers` 中的值
    >
    > ![image-20210221131418699](https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210221131425.png) 
    >
    > 
    >
    > 经过 `nn.Sequential(*layers)` 后，`res` 变成了下图![image-20210221131609015](https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210221131609.png)
    >
    > 返回 `vgg11` 的网络

    源码如下：

    ```python
    def make_layers(cfg: list):
        layers = []
        in_channels = 3
        for v in cfg:
            if v == 'M':
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            else:
                conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
                layers += [conv2d, nn.ReLU(True)]
                in_channels = v
        res = nn.Sequential(*layers)
        return res
    
    
    cfgs = {
        'vgg11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
        'vgg13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
        'vgg16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
        'vgg19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
    }
    
    make_layers(cfgs['vgg11'])
    ```

  - `**`

    这回params是一个字典了：

    ```
    params={'x':1,'y':2}
    ```

    可以通过如下方式调用myprint函数：

    ```python
    >>> myprint(**params)
    ```

    就可以输出：

    ```
    1
    2
    ```

### 字典

```python
for k, v in dict.items():
    print(k, v)
dict.get(key, default=None)
```

key -- 字典中要查找的键。

default -- 如果指定键的值不存在时，返回该默认值

### 位运算符

Python 的位运算符共 6 个

| 运算符 | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| &      | 按位“与”运算符：参与运算的两个值，如果两个相应位都为 1，则结果为 1，否则为 0 |
| \|     | 按位“或”运算符：只要对应的两个二进制位有一个为 1 时，结果就为 1 |
| ^      | 按位“异或”运算符：当两对应的二进制位相异时，结果为 1         |
| ~      | 按位“取反”运算符：对数据的每个二进制位取反，即把 1 变为 0，把 0 变为 1 |
| <<     | “左移动”运算符：运算数的各二进制位全部左移若干位，由“<<”右边的数指定移动的位数，高位丢弃， 低位补 0 |
| >>     | “右移动”运算符：运算数的各二进制位全部右移若干位，由“>>”右边的数指定移动的位数 |

```python
>>> a=55  #a=0011 0111
>>> b=11  #b=0000 1011
>>> print(a&b)
3
>>> print(a|b)
63
>>> print(a^b)
60
>>> print(~a)
-56
>>> print(a<<3)
440
>>> print(a>>3)
6
```



***

[Reference]

[iter_generator](https://docs.python.org/zh-cn/3/tutorial/classes.html#iterators)

[3.5 【基础】迭代器](http://python.iswbm.com/en/latest/c03/c03_05.html)

[3.6 【基础】生成器)](http://python.iswbm.com/en/latest/c03/c03_06.html#)

[Python中的*（星号）和**(双星号）完全详解](https://blog.csdn.net/zkk9527/article/details/88675129)