# `Cmake` 简单使用

cmake 是一个跨平台、开源的构建系统。它是一个集软件构建、测试、打包于一身的软件。它使用与平台和编译器独立的配置文件来对软件编译过程进行控制

## 命令介绍

#### cmake 最小版本

这行命令是可选的，我们可以不写这句话，但在有些情况下，如果 CMakeLists.txt 文件中使用了一些高版本 cmake 特有的一些命令的时候，就需要加上这样一行，提醒用户升级到该版本之后再执行 cmake

```bash
cmake_minimum_required(VERSION 3.4.1)
```

#### 设置项目名称

```bash
project(demo)
```

这个命令不是强制性的，但最好都加上。它会引入两个变量 demo_BINARY_DIR 和 demo_SOURCE_DIR，同时，cmake 自动定义了两个等价的变量 PROJECT_BINARY_DIR 和 PROJECT_SOURCE_DIR

#### 设置编译类型

```bash
add_executable(demo demo.cpp) # 生成可执行文件
add_library(common STATIC util.cpp) # 生成静态库
add_library(common SHARED util.cpp) # 生成动态库或共享库
```

- 在 Linux 下是：
  demo
  libcommon.a
  libcommon.so
- 在 Windows 下是：
  demo.exe
  common.lib
  common.dll

#### 指定编译包含文件

**明确指定**

```bash
add_library(demo, demo.cpp test.cpp util.cpp)
```

**搜索所有的cpp文件**

```bash
aux_source_directory(. SRC_LIST) # 搜索当前文件夹下所有.cpp文件
```

**自定义规则**

```bash

file(GLOB SRC_LIST "*.cpp" "protocol/*.cpp")
add_library(demo ${SRC_LIST})
# 或者
file(GLOB SRC_LIST "*.cpp")
file(GLOB SRC_PROTOCOL_LIST "protocol/*.cpp")
add_library(demo ${SRC_LIST} ${SRC_PROTOCOL_LIST})
# 或者
aux_source_directory(. SRC_LIST)
aux_source_directory(protocol SRC_PROTOCOL_LIST)
add_library(demo ${SRC_LIST} ${SRC_PROTOCOL_LIST})
```

#### 查找指定库文件

`find_library(VAR name path)` 查找到指定的预编译库，并将它的路径存储在变量中, 类似的命令还有 `find_file()、find_path()、find_program()、find_package()`
默认的搜索路径为 cmake 包含的系统库，因此如果是 NDK 的公共库只需要指定库的 name 即可。

```bash
find_library( # Sets the name of the path variable.
              log-lib
 
              # Specifies the name of the NDK library that
              # you want CMake to locate.
              log )
```

#### 设置包含目录

```bash
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_BINARY_DIR})

# linux还有这种方式
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -I${CMAKE_CURRENT_SOURCE_DIR}")
```

#### 设置链接库目录

```bash
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/libs)

# linux 还可以通过
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -L${CMAKE_CURRENT_SOURCE_DIR}/libs")
```

#### 设置 target 需要链接库

在 Windows 下，系统会根据链接库目录，搜索xxx.lib 文件，Linux 下会搜索 xxx.so 或者 xxx.a 文件，如果都存在会优先链接动态库（so 后缀）

```bash
target_link_libraries( # 目标库
                       demo
 
                       # 目标库需要链接的库
                       # log-lib 是上面 find_library 指定的变量名
                       ${log-lib} )
```

**指定链接动态库或静态库**

```bash
target_link_libraries(demo libface.a) # 链接libface.a
target_link_libraries(demo libface.so) # 链接libface.so
```

**指定全路径**

```bash
target_link_libraries(demo ${CMAKE_CURRENT_SOURCE_DIR}/libs/libface.a)
target_link_libraries(demo ${CMAKE_CURRENT_SOURCE_DIR}/libs/libface.so)
```

**链接多个库**

```bash
target_link_libraries(demo ${CMAKE_CURRENT_SOURCE_DIR}/libs/libface.a boost_system.a)
```

#### 设置变量

**set 直接设置**

```bssh
set(SRC_LIST main.cpp test.cpp)
add_executable(demo ${SRC_LIST})
```

**set 追加设置变量的值**

```bash
set(SRC_LIST main.cpp)
set(SRC_LIST ${SRC_LIST} test.cpp)
add_executable(demo ${SRC_LIST})
```

**list 追加或者删除变量的值**

```bash
set(SRC_LIST main.cpp)
list(APPEND SRC_LIST test.cpp)
list(REMOVE_ITEM SRC_LIST main.cpp)
add_executable(demo ${SRC_LIST})
```

#### 条件控制

#### 打印信息

```bash
message(${PROJECT_SOURCE_DIR})
message("build with debug mode")
message(WARNING "this is warnning message")
message(FATAL_ERROR "this build has many error") # FATAL_ERROR 会导致编译失败
```

#### 包含其他 cmake 文件

```bash
include(./common.cmake) # 指定包含文件的全路径
include(def) # 在搜索路径中搜索def.cmake文件
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake) # 设置include的搜索路径
```

## 常用变量

#### 预定义变量

PROJECT_SOURCE_DIR：工程的根目录
PROJECT_BINARY_DIR：运行 cmake 命令的目录，通常是 ${PROJECT_SOURCE_DIR}/build
PROJECT_NAME：返回通过 project 命令定义的项目名称
CMAKE_CURRENT_SOURCE_DIR：当前处理的 CMakeLists.txt 所在的路径
CMAKE_CURRENT_BINARY_DIR：target 编译目录
CMAKE_CURRENT_LIST_DIR：CMakeLists.txt 的完整路径
CMAKE_CURRENT_LIST_LINE：当前所在的行
CMAKE_MODULE_PATH：定义自己的 cmake 模块所在的路径，SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)，然后可以用INCLUDE命令来调用自己的模块
EXECUTABLE_OUTPUT_PATH：重新定义目标二进制可执行文件的存放位置
LIBRARY_OUTPUT_PATH：重新定义目标链接库文件的存放位置

## 项目实例

#### 简单 HELLO 项目实例

**main.c 文件**

```c
#include <stdio.h>
int main(){
    printf("Hellow world!\n");
    return 0;
}
```

**CMakeLists.txt**

```bash
project(HELLO)
add_executable(hello main.c)
```

**编译运行**

```bash
# 创建 build 文件夹 防止生成的文件污染根目录
mkdir build & cd build

# ..代表的上级目录
cmake ..

# 这时候可以看到文件夹下生成 hello 可执行文件
make
```

#### 复杂项目



---

[Reference]

[CMakeLists.txt 语法介绍与实例演练](https://blog.csdn.net/afei__/article/details/81201039)

