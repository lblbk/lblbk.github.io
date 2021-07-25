# Ubuntu 安装 opencv

#### **版本**

> ubuntu21
>
> opencv 3.4.14
>
> shell zsh

#### 环境准备

**cmake**

```bash
sudo apt-get install cmake
```

**依赖环境**

```bash
sudo apt install  build-essential
 
sudo apt install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev  
 
sudo apt install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
```

> 这里我遇到两个错误
>
> `python-dev` `python-numpy`包找不到，改成`python3-dev` `python3-numpy`
>
> 
>
> 无法定位软件包libjasper-dev 的错误提示
>
> ```bash
> sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
> sudo apt update
> sudo apt upgrade
> sudo apt install libjasper1 libjasper-dev
> ```
>
> 这里可能加的源显示 `由于没有公钥，无法验证以下签名` ,是这执行以下命令 最后面那串是在命令中有提示的
>
> ```bash
> sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 76F1A20FF987672F
> ```

**下载源码**

可以自行去opencv官网下载自己想要的压缩包

**解压**

有命令行，有gui，用文档管理器吧

```bash
unzip /path/to/opencv/opencv-3.4.14.zip
```

**cmake 和 make**

创建个文件夹build，乱七八糟的文件放在里面

```bash
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_TIFF=ON ..
sudo make -j4
sudo make install
```

`cmake` 的时候还有些参数，我是直接默认的，因为是cpu, 后续遇到会继续更新

`sudo make -j4` 就是多线程处理，会更快一点

**配置环境**

```bash
# 首先将OpenCV的库添加到路径
sudo vim /etc/ld.so.conf
# 在文件末尾添加
include /usr/loacal/lib
# 保存退出后让刚才的配置路径生效
sudo ldconfig
# 配置环境变量，看你用什么shell, 我是zsh, 所以放在系统变量profile下面
sudo vim /etc/profile
# 在打开的文件的末尾添加如下内容
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
export PKG_CONFIG_PATH
# 保存之后，执行如下命令是的配置生效
source /etc/profile
```

**查看版本**

```bash
pkg-config opencv --modversion
```

**测试样例**

进入opencv-3.4.14/samples/cpp/example_cmake目录下，执行命令：

```bash
cmake .
make
./opencv_example
```

