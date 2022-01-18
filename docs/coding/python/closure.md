# Trick



### 嵌套函数

**封装 数据隐藏** 保护一部分代码不受函数外部变化的影响，从全局作用域中隐藏起来

```python
def add_one(a):
    def add(b):
        return b + 1
    print(add(a))

    
add_one(1)  # 2
```

**DRY原则** Don’t Repeat Yourself 在程序设计以及计算中避免重复代码

1、以文件对象的方式读取

```python
def read_file_object(f):
    for line in f:
      print(line)
f = open('a.txt', 'r', encoding='utf8')
read_file_object(f)
```

2、以文件名的方式读取

```python
def read_file_name(file_name):
  if isinstance(file_name, str):
    with open(file_name, 'r', encoding='utf8') as f:
      for line in f:
        print(line)
read_file_name('a.txt')
```

这种方式显然不好，不同的读取方式需要调用不同的函数，并且读取文件的代码重复了，显得冗余啰嗦，来看看嵌套函数怎么优雅的实现这个功能吧：

```python
def read_file(file):
  def inner(file_):
    for line in file_:
      print(line, end='')
  if isinstance(file, str):
    with open(file, 'r', encoding='utf8') as f:
      inner(f)
  else:
    inner(file)
read_file("a.txt")
```

### **闭包** 

##### **概念**

当某个**函数**被当成对象返回时，**夹带了外部变量**，就形成了一个闭包

```python
def print_msg():
    # print_msg 是外围函数
    msg = "zen of python"
    def printer():
        # printer 是嵌套函数
        print(msg)
    return printer

another = print_msg()
# 输出 zen of python
another()
```

内部函数 printer 直接作为返回值返回了。一般情况下，函数中的局部变量仅在函数的执行期间可用，一旦 print_msg() 执行过后，我们会认为 msg变量将不再可用。然而，在这里我们发现 print_msg 执行完之后，在调用 another 的时候 msg 变量的值正常输出了，这就是闭包的作用，闭包使得局部变量在函数外被访问成为可能。

看完这个例子，我们再来定义闭包，维基百科上的解释是:

> 在计算机科学中，闭包（Closure）是词法闭包（Lexical Closure）的简称，是引用了自由变量的函数。这个被引用的自由变量将和这个函数一同存在，即使已经离开了创造它的环境也不例外。所以，有另一种说法认为闭包是由函数和与其相关的引用环境组合而成的实体。

这里的 another 就是一个闭包，闭包本质上是一个函数，它有两部分组成，printer 函数和变量 msg。闭包使得这些变量的值始终保存在内存中。

闭包，顾名思义，就是一个封闭的包裹，里面包裹着自由变量，就像在类里面定义的属性值一样，自由变量的可见范围随同包裹，哪里可以访问到这个包裹，哪里就可以访问到这个自由变量。

##### **常见错误**

- 闭包无法修改外部函数的局部变量

```python
def outer():
    num = 10
    def inner():
        num += 1
        # return num可以 在inner()函数里面对num更改会报错
        return num
    return inner

test = outer()
test()
```

> local variable 'num' referenced before assignment，也就是说你在inner内使用num += 1时，相当于num = num + 1，此时对num进行赋值python默认num是局部变量，但是inner内并没有定义num，所以会报错。

当把num改成list类型

```python
def outer():
    num = [10]
    def inner():
        num[0] += 1
        return num[0]
    return inner

test = outer()
test()
```

> 通过运行，我们发现可以得到想要的结果，因为list是可变类型，此时num指向的是自由变量num，并对num中的数据进行了改变。

但是这样每次都把不可变数据转换成可变数据进行传递太麻烦了，所以python3引入了nonlocal声明，作用是把变量标记为自由变量，即使在函数中为变量赋予了新值，也会变成自由变量。

```python
def outer():
    num = 10
    def inner():
        nonlocal num
        num += 1
        return num
    return inner

test = outer()
test()
```

> python2没有nonlocal，所以需要把变量存储为可变变量的元素或属性，并把对象绑定给自由变量

- python循环中不包含域的概念

```python
flist = []
for i in range(3):
    def func(x):
        return x*i
    flist.append(func)

for f in flist:
    print(f(2))  # 4 4 4
```

> 按照大家正常的理解，应该输出的是0, 2, 4对吧？但实际输出的结果是:4, 4, 4. 原因是什么呢？loop在python中是没有域的概念的，flist在向列表中添加func的时候，并没有保存i的值，而是当执行f(2)的时候才去取，这时候循环已经结束，i的值是2，所以结果都是4。

```python
flist = []
for i in range(3):
    def makefunc(i):
        def func(x):
            return x * i
        return func
    flist.append(makefunc(i))

for f in flist:
    print(f(2))
```

> 在func外面再定义一个makefunc函数，func形成闭包，结果就正确了

```python
# 偏函数也可以解决
from functools import partial
flist = []

for i in range(3):
    def func(x, multiplier=None):
        return x * multiplier
    flist.append(partial(func, multiplier=i))
```

有了闭包，我们可以不使用全局变量；还有一个很大的用处，把一些数据和函数联系起来，这大大简化了代码，也提升了可读性。

```python
class Test():
  def __init__(self, a):
    self.a = a
  def add(self, b):
    print(self.a + b)

test = Test(1)
test.add(2)  # 3
test.add(3)  # 4
```

```python
def outer(a):
  def inner(b):
    print(a+b)
  return inner

test = outer(1)
test(2)  # 3
test(3)  # 4
```

所有函数都有一个 __closure__属性，如果这个函数是一个闭包的话，那么它返回的是一个由 cell 对象组成的元组对象。cell 对象的cell_contents 属性就是闭包中的自由变量。

```python
test.__closure__
test.__closure__[0].cell_contents

#  (<cell at 0x000001E8F9755588: int object at 0x00007FFD0AE97100>,)
#  1
```



***

[一步一步教你认识Python闭包 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/26934085)

[这大概是最全面最通俗易懂的python闭包了 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/102462850)

