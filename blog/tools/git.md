<head><style type="text/css">h1:first-child {display:none;}</style></head>

# Git使用

### 创建新仓库

  创建新文件夹，打开，然后执行 

  `git init`
  以创建新的 git 仓库。

### 检出仓库

执行如下命令以创建一个本地仓库的克隆版本：
`git clone /path/to/repository` 
如果是远端服务器上的仓库，你的命令会是这个样子：
`git clone username@host:/path/to/repository`

### 工作流

你的本地仓库由 git 维护的三棵“树”组成。第一个是你的 `工作目录`，它持有实际文件；第二个是 `暂存区（Index）`，它像个缓存区域，临时保存你的改动；最后是 `HEAD`，它指向你最后一次提交的结果。

![](https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210210181347.png)

### 添加和提交

你可以提出更改（把它们添加到暂存区），使用如下命令：
`git add <filename>`
`git add *`
这是 git 基本工作流程的第一步；使用如下命令以实际提交改动：
`git commit -m "代码提交信息"`
现在，你的改动已经提交到了 **HEAD**，但是还没到你的远端仓库。

### 高级文件添加

还有一些更高级的方法可以将文件添加到 Git 中，从而使你的工作流程更高效。我们可以执行以下操作，而不是试图查找所有有更改的文件并逐个添加它们：

```
# 逐个添加文件
git add filename

# 添加当前目录中的所有文件
git add -A

# 添加当前目录中的所有文件更改
git add .

# 选择要添加的更改（你可以 Y 或 N 完成所有更改）
git add -p
```

### 高级提交

我们可以使用 `git commit -m '提交信息'` 来将文件提交到 Git。对于提交简短消息来说，这一切都很好，但是如果你想做一些更精细的事情，你需要来学习更多的操作:

```
### 提交暂存文件，通常用于较短的提交消息
git commit -m 'commit message'

### 添加文件并提交一次
git commit filename -m 'commit message'

### 添加文件并提交暂存文件
git commit -am 'insert commit message'

### 更改你的最新提交消息
git commit --amend 'new commit message' 

# 将一系列提交合并为一个提交，你可能会用它来组织混乱的提交历史记录
git rebase -i
### 这将为你提供核心编辑器上的界面：
# Commands:
#  p, pick = use commit
#  r, reword = use commit, but edit the commit message
#  e, edit = use commit, but stop for amending
#  s, squash = use commit, but meld into previous commit
#  f, fixup = like "squash", but discard this commit's log message
#  x, exec = run command (the rest of the line) using shell
```

### 推送改动

你的改动现在已经在本地仓库的 **HEAD** 中了。执行如下命令：
`git push origin master` 可以将这些改动提交到远端仓库，可以把 *master* 换成你想要推送的任何分支。 
`git remote add origin <server>` 如果你还没有克隆现有仓库，并欲将你的仓库连接到某个远程服务器，这个命令可以添加远程服务器。
如此你就能够将你的改动推送到所添加的服务器上去了。

`git remote rm origin` 删除远程服务器
`git remote -v`  查看可以使用的远程服务器 

### 状态检查

git status 命令用于确定哪些文件处于哪种状态，它使你可以查看哪些文件已提交，哪些文件尚未提交。如果在所有文件都已提交并推送后运行此命令，则应该看到类似以下内容：

```
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

如果你将新文件添加到项目中，而该文件之前不存在，则在运行 `git status` 时，你应该看到未跟踪的文件，如下所示：

```
$ git status
# On branch master
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#   README
nothing added to commit but untracked files present (use "git add" to track)
```

使用 `git status` 对于快速检查你已经备份的内容和你仅在本地拥有的内容非常有用。

### 分支

分支是用来将特性开发绝缘开来的。在你创建仓库的时候，*master* 是“默认的”分支。在其他分支上进行开发，完成后再将它们合并到主分支上。![](https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210210181428.png)

创建一个叫做“feature_x”的分支，并切换过去：
`git checkout -b feature_x`
切换回主分支：
`git checkout master`
再把新建的分支删掉：
`git branch -d feature_x`
除非你将分支推送到远端仓库，不然该分支就是 *不为他人所见的*：
`git push origin <branch>`

### 更新与合并

要更新你的本地仓库至最新改动，执行：
`git pull`
以在你的工作目录中 *获取（fetch）* 并 *合并（merge）* 远端的改动。
要合并其他分支到你的当前分支（例如 master），执行：
`git merge <branch>`
在这两种情况下，git 都会尝试去自动合并改动。遗憾的是，这可能并非每次都成功，并可能出现*冲突（conflicts）*。 这时候就需要你修改这些文件来手动合并这些*冲突（conflicts）*。改完之后，你需要执行如下命令以将它们标记为合并成功：
`git add <filename>`
在合并改动之前，你可以使用如下命令预览差异：
`git diff <source_branch> <target_branch>`

### 标签

为软件发布创建标签是推荐的。这个概念早已存在，在 SVN 中也有。你可以执行如下命令创建一个叫做 *1.0.0* 的标签：
`git tag 1.0.0 1b2e1d63ff`
*1b2e1d63ff* 是你想要标记的提交 ID 的前 10 位字符。可以使用下列命令获取提交 ID：
`git log`
你也可以使用少一点的提交 ID 前几位，只要它的指向具有唯一性。

### log

如果你想了解本地仓库的历史记录，最简单的命令就是使用: 
`git log`
你可以添加一些参数来修改他的输出，从而得到自己想要的结果。 只看某一个人的提交记录:
`git log --author=bob`
一个压缩后的每一条提交记录只占一行的输出:
`git log --pretty=oneline`
或者你想通过 ASCII 艺术的树形结构来展示所有的分支, 每个分支都标示了他的名字和标签: 
`git log --graph --oneline --decorate --all`
看看哪些文件改变了: 
`git log --name-status`
这些只是你可以使用的参数中很小的一部分。更多的信息，参考：
`git log --help`

### 替换本地改动

假如你操作失误（当然，这最好永远不要发生），你可以使用如下命令替换掉本地改动：
`git checkout -- <filename>`
此命令会使用 HEAD 中的最新内容替换掉你的工作目录中的文件。已添加到暂存区的改动以及新文件都不会受到影响。

假如你想丢弃你在本地的所有改动与提交，可以到服务器上获取最新的版本历史，并将你本地主分支指向它：
`git fetch origin`
`git reset --hard origin/master`

### 修复错误和回溯

发生错误……它们经常在编码中发生！重要的是我们能够修复它们。

不要慌！Git 提供了你所需的一切，以防你在所推送的代码中犯错，改写某些内容或者只是想对所推送的内容进行更正。

```
### 切换到最新提交的代码版本
git reset HEAD 
git reset HEAD -- filename # for a specific file
### 切换到最新提交之前的代码版本
git reset HEAD^ -- filename
git reset HEAD^ -- filename # for a specific file
### 切换回3或5次提交
git reset HEAD~3 -- filename
git reset HEAD~3 -- filename # for a specific file
git reset HEAD~5 -- filename
git reset HEAD~5 -- filename # for a specific file
### 切换回特定的提交，其中 0766c053 为提交 ID
git reset 0766c053 -- filename
git reset 0766c053 -- filename # for a specific file
### 先前的命令是所谓的软重置。 你的代码已重置，但是git仍会保留其他代码的副本，以备你需要时使用。 另一方面，--hard 标志告诉Git覆盖工作目录中的所有更改。
git reset --hard 0766c053
```

### 实用小贴士

内建的图形化 git：
`gitk`
彩色的 git 输出：
`git config color.ui true`
显示历史记录时，每个提交的信息只显示一行：
`git config format.pretty oneline`
交互式添加文件到暂存区：
`git add -i`

### 搜索

```
### 搜索目录中的字符串部分
git grep 'project'

### 在目录中搜索部分字符串，-n 打印出 git 找到匹配项的行号
git grep -n 'project'

### git grep -C <行数> 'something' 搜索带有某些上下文的字符串部分（某些行在我们正在寻找的字符串之前和之后）
git grep -C<number of lines> 'project'

### 搜索字符串的一部分，并在字符串之前显示行
git grep -B<number of lines> 'project'

### 搜索字符串的一部分，并在字符串之后显示行
git grep -A<number of lines> 'something'
```

### 看谁写了什么

```
### 显示带有作者姓名的文件的更改历史记录
git blame 'filename'

### 显示带有作者姓名和 git commit ID 的文件的更改历史记录
git blame 'filename' -l
```

### Bugs

##### 下载仓库问题

```bash
fatal: unable to access 'https://github.com/path/to/repo.git/': gnutls_handshake() failed: Error in the pull function.
```

重新编译太麻烦，找到下面方法

```bash
apt-get -y install build-essential nghttp2 libnghttp2-dev libssl-dev
```

[stackoverflow问题链接](https://stackoverflow.com/questions/52379234/git-gnutls-handshake-failed-error-in-the-pull-function)