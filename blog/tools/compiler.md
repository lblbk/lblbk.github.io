# 编译器

>  看了很多文章， `GNU` 和 `LLVM` 感觉也并非并列关系，还是采用了下面的写法感觉更合理一些
>
> 参考wikipedia

传统的编译器通常分为三个部分，前端（frontEnd），优化器（Optimizer）和后端(backEnd)。在编译过程中，前端主要负责词法和语法分析，将源代码转化为抽象语法树；优化器则是在前端的基础上，对得到的中间代码进行优化，使代码更加高效；后端则是将已经优化的中间代码转化为针对各自平台的机器代码。

## GNU and GCC

**GNU**是一个[自由](https://zh.wikipedia.org/wiki/自由軟體)的[操作系统](https://zh.wikipedia.org/wiki/作業系統)，其内容软件完全以[GPL](https://zh.wikipedia.org/wiki/GPL)方式发布。这个操作系统是[GNU计划](https://zh.wikipedia.org/wiki/GNU計劃)的主要目标，名称来自GNU's Not Unix!的[递归缩写](https://zh.wikipedia.org/wiki/遞迴縮寫)，因为GNU的设计类似[Unix](https://zh.wikipedia.org/wiki/Unix)，但它不包含具著作权的Unix代码。GNU的创始人，[理查德·马修·斯托曼](https://zh.wikipedia.org/wiki/理察·馬修·斯托曼)，将GNU视为“达成社会目的技术方法”。

作为操作系统，GNU的发展仍未完成，其中最大的问题是具有完备功能的内核尚未被开发成功。GNU的内核，称为[Hurd](https://zh.wikipedia.org/wiki/GNU_Hurd)，是[自由软件基金会](https://zh.wikipedia.org/wiki/自由軟體基金會)发展的重点，但是其发展尚未成熟。在实际使用上，多半使用[Linux内核](https://zh.wikipedia.org/wiki/Linux內核)、[FreeBSD](https://zh.wikipedia.org/wiki/FreeBSD)等替代方案，作为系统核心，其中主要的操作系统是Linux的发行版。[Linux](https://zh.wikipedia.org/wiki/Linux)操作系统包涵了[Linux内核](https://zh.wikipedia.org/wiki/Linux內核)与其他自由软件项目中的GNU组件和软件，可以被称为[GNU/Linux](https://zh.wikipedia.org/wiki/GNU/Linux)（见[GNU/Linux命名争议](https://zh.wikipedia.org/wiki/GNU/Linux命名爭議)）。

### GCC

GCC 是GNU项目的关键部分，GCC已成为GNU系统的官方编译器（包括GNU/Linux家族），它也成为编译与创建其他操作系统的主要编译器，包括BSD家族、Mac OS X、NeXTSTEP与BeOS。

GCC（特别是其中的C语言编译器）也常被认为是跨平台编译器的事实标准。

GCC原名为GNU C语言编译器（GNU C Compiler），原本用C开发，只能处理C语言。后来因为LLVM、Clang的崛起，令GCC更快将开发语言转换为C++，变得可处理C++。之后也变得可处理Fortran、Pascal、Objective-C、Java、Ada，以及Go与其他语言。

## LLVM and Clang

LLVM（Low Level Virtual Machine）是一个自由软件项目，它是一种编译器基础设施，以C++写成，包含一系列模块化的编译器组件和工具链，用来开发编译器前端和后端。它是为了任意一种编程语言而写成的程序，利用虚拟技术创造出编译时期、链接时期、运行时期以及“闲置时期”的最优化。它最早以C/C++为实现对象，而当前它已支持包括ActionScript、Ada、D语言、Fortran、GLSL、Haskell、Java字节码、Objective-C、Swift、Python、Ruby、Rust、Scala以及C#等语言。也就是说 LLVM 建立的初衷就不是成为操作系统，而是编译器。

整个流程可以简要概括为 Clang对代码进行处理形成中间层作为输出，llvm把CLang的输出作为输入生成机器码。GCC 目前作为跨平台编译器来说它的兼容性无异是最强的，兼容最强肯定是以牺牲一定的性能为基础的，苹果为了提高性能，因此专门针对mac系统开发了专用的编译器Clang与LLVM，Clang用于编译器前端，LLVM用于后端。

### Clang

**Clang**（发音为/ˈklæŋ/类似英文单字*[clang](https://zh.wiktionary.org/wiki/clang)*[[3\]](https://zh.wikipedia.org/wiki/Clang#cite_note-3)） 是一个[C](https://zh.wikipedia.org/wiki/C語言)、[C++](https://zh.wikipedia.org/wiki/C%2B%2B)、[Objective-C](https://zh.wikipedia.org/wiki/Objective-C)和[Objective-C++](https://zh.wikipedia.org/wiki/Objective-C%2B%2B)编程语言的[编译器](https://zh.wikipedia.org/wiki/編譯器)前端。它采用了[LLVM](https://zh.wikipedia.org/wiki/LLVM)作为其后端，由LLVM2.6开始，一起发布新版本。它的目标是提供一个[GNU编译器套装](https://zh.wikipedia.org/wiki/GCC)（GCC）的替代品，支持了GNU编译器大多数的编译设置以及非官方语言的扩展。

Clang是LLVM编译器工具集的前端（front-end），目的是输出代码对应的抽象语法树（Abstract Syntax Tree, AST），并将代码编译成LLVM Bitcode，接着在后端（back-end）使用LLVM编译成平台相关的机器语言。

## 编译过程

编译一般分为四个步骤

`.c` --预处理 gcc-E --> `.i` --编译 gcc-S --> `.s` --汇编 gcc-C --> `.o` --链接 gcc --> `main/a.out`

1. **预处理 Preprocessing**：解析各种预处理命令，包括头文件包含、宏定义的扩展、条件编译的选择等；
2. **编译 Compiling**：对预处理之后的源文件进行翻译转换，产生由机器语言描述的汇编文件；
3. **汇编 Assembly**：将汇编代码转译成为机器码；
4. **链接 Link**：将机器码中的各种符号引用与定义转换为可执行文件内的相应信息（例如虚拟地址）；

## 构建工具

我们的程序**只有一个**源文件时，直接就可以用gcc命令编译它。

如果我们的程序包含很**多个**源文件时，用gcc命令逐个去编译时，就发现很容易混乱而且工作量大，所以出现了下面make工具。

### make

`make`是一款用于解释`makefile`文件当中命令的工具，可以看成是一个智能的**批处理**工具，它本身并没有编译和链接的功能，而是用类似于批处理的方式—通过调用**makefile文件**中用户指定的命令来进行编译和链接的，而`makefile`关系到整个工程的编译规则。许多 IDE 集成开发环境都整合了该命令，例如：Visual C++ 里的**nmake**，Linux 里的 **GNU make**。

### makefile 文件

make工具就根据makefile中的命令进行编译和链接的。makefile命令中就包含了调用gcc（也可以是别的编译器）去编译某个源文件的命令。

makefile在一些简单的工程完全可以人工拿下，但是当工程非常大的时候，手写makefile也是非常麻烦的，如果换了个平台makefile又要重新修改，这时候就出现了下面的Cmake这个工具。

### Cmake

cmake就可以更加简单的生成makefile文件给上面那个make用。当然cmake还有其他更牛X功能，就是可以**跨平台**生成对应平台能用的makefile，我们就不用再自己去修改了。

可是cmake根据什么生成makefile呢？它又要根据一个叫CMakeLists.txt文件（学名：组态档）去生成makefile。

### CMakeLists

这个需要自己手写，有另一篇专门记载 cmake 基本语法。[cmake基本语法](https://lblbk.github.io/lblbk/#/coding/cpp/cmake)

