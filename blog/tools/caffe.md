<head><style type="text/css">h1:first-child {display:none;}</style></head>

# `Caffe-CPU` 安装

##### 环境准备

```bash
sudo apt-get install  -y libopencv-dev
sudo apt-get install -y build-essential cmake git pkg-config
sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install -y liblapack-dev
sudo apt-get install -y libatlas-base-dev 
sudo apt-get install -y --no-install-recommends libboost-all-dev
sudo apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev
sudo apt-get install -y python-numpy python-scipy
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-numpy python3-scipy
```

##### 下载 `Caffe`

```bash
git clone https://github.com/BVLC/caffe.git
```

##### `Python` 环境准备

```bash
cd caffe/python/
for req in $(cat requirements.txt); do pip3 install $req; done
```

##### 修改配置文件

```bash
cp Makefile.config.example  Makefile.config
vim Makefile.config
```

###### 修改 `Makefile.config`

```bash
# CPU_ONLY := 1

CPU_ONLY := 1

# OPENCV_VERSION := 3

OPENCV_VERSION := 3

# PYTHON_INCLUDE := /usr/include/python2.7 \
                /usr/lib/python2.7/dist-packages/numpy/core/include

PYTHON_LIBRARIES := boost_python3 python3.9
PYTHON_INCLUDE := /usr/include/python3.9 \
                 /usr/lib/python3/dist-packages/numpy/core/include
                 
# WITH_PYTHON_LAYER := 1

WITH_PYTHON_LAYER := 1

 
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib

INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu/hdf5/serial
```

###### 修改 `Makefile`

```bash
# 181
LIBRARIES += glog gflags protobuf boost_system boost_filesystem m 

LIBRARIES += glog gflags protobuf boost_system boost_filesystem m hdf5_serial_hl hdf5_serial
```

##### 编译

###### `make all -j4` 

```bash
/usr/bin/ld: cannot find -lboost_system
/usr/bin/ld: cannot find -lboost_filesystem
/usr/bin/ld: cannot find -lboost_thread
collect2: error: ld returned 1 exit status
make: *** [Makefile:583: .build_release/lib/libcaffe.so.1.0.0] Error 1
make: *** Waiting for unfinished jobs....
```

在文件夹  `/usr/lib/x86_64-linux-gnu/` 搜索一下 `libboost_system.so` 的包，如果可以找到，则执行以下命令，其他几个库同理

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_system.so.1.65.1 /usr/lib/libboost_system.so
```

如果找不到，官方给的脚本安装 `boost` 库是没安装完全的，用下面命令重新安装

```bash
sudo apt-get install libboost-all-dev
```

###### `make pycaffe`

```bash
/usr/bin/ld: cannot find -lboost_python3
/usr/bin/ld: cannot find -lpython2.7
collect2: error: ld returned 1 exit status
make: *** [Makefile:518: python/caffe/_caffe.so] Error 1
```

我第一次提示 `lboost_python3` `lpython2.7` 都不存在，完善很多这行都会注释，打开这行，`lpython2.7` 问题解决

```bash
PYTHON_LIBRARIES := boost_python3 python3.9
```

在caffe编译配置文件 `Makefile.config` 里面的 `PYTHON_LIBRARIES := boost_python3 python3.6m` 一行中，找不到 `boost_python3` 造成的

同理在文件夹  `/usr/lib/x86_64-linux-gnu/` 搜索一下 `libboost_python3.9.so` 文件，如果存在则

```bash
sudo ln -s libboost_python39.so libboost_python3.so
sudo ln -s libboost_python39.a libboost_python3.a
```

如果不存在，需要自己编译一个，给链接自己去编译吧 [教程](https://www.cnblogs.com/chenfeifen/p/13412125.html)

##### 环境变量

具体加在那个配置文件自己决定

```bash
sudo vim ~/.profile
```

合适地方添加，`caffe_path` 就是 `caffe` 在你电脑位置

```bash
export PYTHONPATH=caffe_path/caffe/python:$PYTHONPATH
```

刷新环境变量

```bash
source ~/.profile
```

##### 验证

```bash
python
> import caffe
```
