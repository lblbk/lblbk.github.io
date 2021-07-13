<head><style type="text/css">h1:first-child {display:none;}</style></head>

# Linux命令收集

> 记录日常使用 ubuntu 遇到的问题和解决方法

### Ubuntu

#### 包管理

- apt命令

  `apt list --installed`

  `apt list --install | grep program_name #利用grep进行过滤`

- dpkg - apt 与apt-get基于dpkg

  `dpkg-query -l`

- 列出系统snap已安装软件包

  `snap list`

- 列出系统flatpak已安装软件包

  `flatpak list`

##### 列出最近安装软件包

Linux 系统保存了所有发生事件的日志。你可以参考最近安装软件包的日志。有两个方法可以来做。用 `dpkg` 命令的日志或者 `apt` 命令的日志。

你仅仅需要用 `grep` 命令过滤已经安装的软件包日志

- 用 `grep` 命令过滤已经安装的软件包日志

  `grep 'install ' /var/log/dpkg.log`

- 查看 `apt` 历史命令日志。这个仅会显示用 `apt` 命令安装的的程序

  `grep " install " /var/log/apt/history.log`
  
  

#### 权限管理

- `sudo su`



#### 安装 `node`

下载好之后，在文件中切换到刚才的下载目录（我的浏览器将node包下载到了 /download 文件夹）

```bash
$ tar -xvJf node-v14.15.1-linux-x64.tar.xz

// 移动解压的包到usr/local/share
$ sudo mv ./node-v14.15.1-linux-x64 /usr/local/share
```


下载的tar.xz包是已经编译好的，可以直接使用

但是为了方便我们需要给 ./bin 目录内的node,npm,npx 分别创建一个软连接 (ln)，linux下的软连接就有点像window系统下的快捷方式

```bash
$ sudo ln -s /usr/local/share/node-v14.15.1-linux-x64/bin/node /usr/local/bin/node

$ sudo ln -s /usr/local/share/node-v14.15.1-linux-x64/bin/npm /usr/local/bin/npm

$ sudo ln -s /usr/local/share/node-v14.15.1-linux-x64/bin/npx /usr/local/bin/npx
```

『Ctrl + Alt + T』快捷键打开终端

```bash
$ node -v
$ npm -v
$ npx -v
```


若以上三个命令都成功，则node 和npm已经安装成功

3.安装cnpm
因为某些原因，国外的npm始终不太好用（速度太慢），所以国内就有了npm 淘宝镜像 cnpm

```bash
$ sudo npm install cnpm -g --registry=https://registry.npm.taobao.org
```

// 创建软连接

```bash
$ sudo ln -s usr/local/share/node-v14.15.1-linux-x64/lib/node_modules/cnpm/bin /usr/local/bin/cnpm
```

运行cnpm

```
$cnpm
```



### QA

##### GPU

- 训练时脚本停止了，gpu显存仍然被占用

  `ps aux|grep user_name|grep python` 查看当前用户所有程序，并过滤python

  `kill -s 9 pid` 杀掉指定进程

  命令解释一下：[kill 与 kill -9 的区别 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/143635282)

  > 其实用 nvidia-smi 查看后就能看到python脚本的pid, 直接杀掉就可以

