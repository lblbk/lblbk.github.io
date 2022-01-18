# 装饰器

### 1 装饰器

装饰器的使用方法很固定

- 先定义一个装饰器（帽子）
- 再定义你的业务函数或者类（人）
- 最后把这装饰器（帽子）扣在这个函数（人）头上

就像下面这样子

```
def decorator(func):
    def wrapper(*args, **kw):
        return func()
    return wrapper

@decorator
def function():
    print("hello, decorator")
```

实际上，装饰器并不是编码必须性，意思就是说，你不使用装饰器完全可以，它的出现，应该是使我们的代码

- 更加优雅，代码结构更加清晰
- 将实现特定的功能代码封装成装饰器，提高代码复用率，增强代码可读性

### 2 日志打印

- 打印前通知
- 打印后通知

```
# 这是装饰器函数，参数 func 是被装饰的函数
def logger(func):
    def wrapper(*args, **kw):
        print('主人，我准备开始执行：{} 函数了:'.format(func.name))
        # 真正执行的是这行。
        func(*args, **kw)
        print('主人，我执行完啦。')
return wrapper

# 主函数
@logger
def add(x, y):
    print('{} + {} = {}'.format(x, y, x+y))
    
add(200, 50)

# 输出
主人，我准备开始执行：add 函数了:
200 + 50 = 250
主人，我执行完啦。
```

### 3 时间计时器

计算函数执行时长

```
# 装饰器函数
def timer(func):
    def wrapper(*args, **kw):
        t1 = time.time()
        func(*args, **kw)
        t2 = time.time()
        
        cost_time = t2 - t1
        print('花费时间:{}秒'.format(cost_time))
    return wrapper

# 睡眠10秒
import time
@timer
def want_sleep(sleep_time):
    time.sleep(sleep_time)
want_sleep(10)

# 输出
花费时间：10.0073800086975098秒
```

### 4 带参数的函数装饰器

###### 装饰器传参

```
def say_hello(contry):
    def wrapper(func):
        def deco(*args, **kw):
            if contry == 'china':
                print('你好')
            elif contry == 'america':
                print('hello')
            else:
                return
            
            func(*args, **kw)
        return deco
    return wrapper
# 小明，中国人
@say_hello("china")
def xiaoming():
    pass

# jack，美国人
@say_hello("america")
def jack():
    pass

# 输出
xiaoming()
print("------------")
jack()
```

### 5 不带参数的类装饰器

基于类装饰器的实现，必须实现 `__call__` 和 `__init__`两个内置函数。 `__init__` ：接收被装饰函数 `__call__` ：实现装饰逻辑。

还是以日志打印这个简单的例子为例

```
class logger:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kw):
        print("[INFO]: the func {func}() is running..."\
            .format(func=self.func.__name__))
        return self.func(*args, **kw)

@logger
def say(sth):
    print("say {}!".format(sth))

say("hello")
```

执行一下，看看输出

```
[INFO]: the function say() is running...
say hello!
```

### 6 带参数的类装饰器

不带参数的例子只能打印`INFO`级别的日志，正常情况下，我们还需要打印`DEBUG` `WARNING`等级别的日志。 这就需要给类装饰器传入参数，给这个函数指定级别了。

带参数和不带参数的类装饰器有很大的不同。

`__init__` ：不再接收被装饰函数，而是接收传入参数。 `__call__` ：接收被装饰函数，实现装饰逻辑。

```
class para_logger:
    def __init__(self, level='INFO'):
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kw):
            print("[{level}]: the function {func}() is running..."\
                .format(level=self.level, func=func.__name__))
            func(*args, **kw)
        return wrapper

@para_logger(level='WARNING')
def say(something):
    print("say {}!".format(something))

say("hello")
```

我们指定`WARNING`级别，运行一下，来看看输出。

```
[WARNING]: the function say() is running...
say hello!
```

### 7 使用偏函数与类实现装饰器

绝大多数装饰器都是基于函数和闭包实现的，但这并非制造装饰器的唯一方式。

事实上，Python 对某个对象是否能通过装饰器（ `@decorator`）形式使用只有一个要求：**decorator 必须是一个“可被调用（callable）的对象**。

对于这个 callable 对象，我们最熟悉的就是函数了。

除函数之外，类也可以是 callable 对象，只要实现了`__call__` 函数（上面几个例子已经接触过了）。

还有容易被人忽略的偏函数其实也是 callable 对象。

接下来就来说说，如何使用 类和偏函数结合实现一个与众不同的装饰器。

如下所示，DelayFunc 是一个实现了 `__call__` 的类，delay 返回一个偏函数，在这里 delay 就可以做为一个装饰器。

```
import time
import functools
class DelayFunc:
    def __init__(self,  duration, func):
        self.duration = duration
        self.func = func
    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} seconds...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)
    def eager_call(self, *args, **kwargs):
        print('Call without delay')
        return self.func(*args, **kwargs)
def delay(duration):
    """
    装饰器：推迟某个函数的执行。
    同时提供 .eager_call 方法立即执行
    """
    # 此处为了避免定义额外函数，
    # 直接使用 functools.partial 帮助构造 DelayFunc 实例
    return functools.partial(DelayFunc, duration)
```

我们的业务函数很简单，就是相加

```
@delay(duration=2)
def add(a, b):
    return a+b
```

来看一下执行过程

```
>>> add    # 可见 add 变成了 Delay 的实例
<__main__.DelayFunc object at 0x107bd0be0>
>>> 
>>> add(3,5)  # 直接调用实例，进入 __call__
Wait for 2 seconds...
8
>>> 
>>> add.func # 实现实例方法
<function add at 0x107bef1e0>
```

### 8 装饰类的装饰器

用 Python 写单例模式的时候，常用的有三种写法。其中一种，是用装饰器来实现的。

以下便是我自己写的装饰器版的单例写法。

```
instances = {}

def singleton(cls):
    def get_instance(*args, **kw):
        cls_name = cls.__name__
        print('=====1====')
        if not cls_name in instances:
            print('====2====')
            instance = cls(*args, **kw)
            instances[cls_name] = instance
        return instances[cls_name]
    return get_instance


@singleton
class User:
    _instance = None

    def __init__(self, name):
        print('====3====')
        self.name = name


u1 = User('xiaoming')
u1.age = 20

u2 = User('xiaowang')
print(u2.age)
print(u1 is u2)
# 输出
=====1====
====2====
====3====
=====1====
20
True
```