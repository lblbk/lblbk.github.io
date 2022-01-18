# 剑指Offer

来源：[《剑指 Offer（第 2 版）》](https://leetcode-cn.com/problemset/lcof/)

### <span id="jz02">JZ02.单例模式</span>

**描述**

设计一个类，只能生成该类的一个实例

**思路**

- 函数装饰器

  ```python
  def singleton(cls):
      _instance = {}
  
      def inner():
          if cls not in _instance:
              _instance[cls] = cls()
          return _instance[cls]
      return inner
  
  
  @singleton
  class Cls:
      def __init__(self):
          pass
  
  
  cls1 = Cls()
  cls2 = Cls()
  print(id(cls1) == id(cls2))
  ```

- 类装饰器

  ```python
  class Singleton:
      def __init__(self, cls):
          self._cls = cls
          self._instance = {}
  
      def __call__(self, *args, **kwargs):
          if self._cls not in self._instance:
              self._instance[self._cls] = self._cls()
          return self._instance[self._cls]
  
  
  @Singleton
  class Cls:
      def __init__(self):
          pass
  
  
  cls1 = Cls()
  cls2 = Cls()
  print(id(cls1) == id(cls2))
  ```

- `__new__` 关键字

  **元类**(**metaclass**) 可以通过方法 **__metaclass__** 创造了**类(class)**，而**类(class)**通过方法 **__new__** 创造了**实例(instance)**

  ```python
  class Singleton:
      _instance = None
  
      def __new__(cls, *args, **kwargs):
          if cls._instance is None:
              cls._instance = object.__new__(cls, *args, **kwargs)
          return cls._instance
  
      def __init__(self):
          pass
  
  
  cls1 = Singleton()
  cls2 = Singleton()
  print(id(cls1) == id(cls2))
  ```

- `__metaclass__` 

  使用 `type` 创造类

  ```python
  def func(self):
      print("do sth")
      
  C = type("C", (), {"func": func})
  c = C()
  c.func()
  ```

   mataclass 实现单例

  ```python
  class Singleton(type):
      _instances = {}
      def __call__(cls, *args, **kwargs):
          if cls not in cls._instances:
              cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
          return cls._instances[cls]
  
  class Cls4(metaclass=Singleton):
      pass
  
  cls1 = Cls4()
  cls2 = Cls4()
  print(id(cls1) == id(cls2))
  ```

### <span id="jz03">JZ03.数组中的重复数字</span>

**描述**

找出数组中重复的数字。

在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

**思路**

- 最先想到的是哈希表 创建空字典，未出现添加到字典中，出现的便返回

  ```python
  class Solution:
      def findRepeatNumber(self, nums: List[int]) -> int:
          repeatDict = {}
          for num in nums:
              if num not in repeatDict:
                  repeatDict[num] = 1
              else:
                  return num
  ```

- 原地置换 [原地交换（以交换萝卜比喻） - 数组中重复的数字 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/solution/yuan-di-jiao-huan-yi-jiao-huan-luo-bu-bi-gh5c/)

  ```python
  class Solution:
      def findRepeatNumber(self, nums: List[int]) -> int:
          for idx in range(len(nums)):
              while nums[idx] != idx:
                  if nums[idx] == nums[nums[idx]]:
                      return nums[idx]
                  nums[nums[idx]], nums[idx] = nums[idx], nums[nums[idx]]
  ```

### <span id="jz04">JZ04.二维数组中的查找</span>

**描述**

在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个高效的函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。

**思路**

右上角 二叉查找树

- [循环遍历](https://leetcode-cn.com/problems/er-wei-shu-zu-zhong-de-cha-zhao-lcof/solution/mian-shi-ti-04-er-wei-shu-zu-zhong-de-cha-zhao-zuo/)

  ```python
  class Solution:
      def findNumberIn2DArray(self, matrix, target: int) -> bool:
          row, col = len(matrix)-1, 0
          while row>0 and j<len(matrix[0]):
              if matrix[row][col] > target: i-=1
              elif matrix[i][j] < target: j+=1
              else: return True
          return False
  ```
  
- 递归

  ```python
  class Solution:
      def findNumberIn2DArray(self, mat, tar: int) -> bool:
          if not mat:
              return False
          self.res = False
          self.target = tar
          self.helper(0, len(mat[0])-1, mat)
          return self.res
  
      def helper(self, i, j, matrix):
          if i<len(matrix) and j >= 0:
              if matrix[i][j]==self.target:
                  self.res = True
              if matrix[i][j] >self.target:
                  self.helper(i, j-1, matrix)
              else:
                  self.helper(i+1, j, matrix)
  ```

### <span id="jz05">JZ05.替换空格</span>

**描述**

请实现一个函数，把字符串 `s` 中的每个空格替换成"%20"

**思路**

- 列表推导式

  ```python
  class Solution:
      def replaceSpace(self, s: str) -> str:
          return ''.join(['%20' if c == ' ' else c for c in s])
  ```

- 循环

  ```python
  class Solution:
      def replaceSpace(self, s: str) -> str:
          res = ''
          for i in s:
              if i == ' ':
                  res += '%20'
              else:
                  res += i
          return res
  ```

### <span id="jz06">JZ06.从尾到头打印指针</span>

**描述**

输入一个链表的头节点，从尾到头反过来返回每个节点的值（用数组返回）。

**思路**

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def reversePrint(self, head: ListNode) -> List[int]:
        res = []
        while head:
            res.append(head.val)
            head = head.next
          return res[::-1]
```

### <span id="jz07">JZ07.重建二叉树</span>

**描述**

输入某二叉树的前序遍历和中序遍历的结果，请重建该二叉树。假设输入的前序遍历和中序遍历的结果中都不含重复的数字

**思路**

- 树的操作基本都是递归

  知识点：

  - 前序遍历列表：第一个元素永远是 【根节点 (root)】
  - 中序遍历列表：根节点 (root)【左边】的所有元素都在根节点的【左分支】，【右边】的所有元素都在根节点的【右分支】

  算法思路：

  1. 通过【前序遍历列表】确定【根节点 (root)】
  2. 将【中序遍历列表】的节点分割成【左分支节点】和【右分支节点】
  3. 递归寻找【左分支节点】中的【根节点 (left child)】和 【右分支节点】中的【根节点 (right child)】

  ```python
  # Definition for a binary tree node.
  # class TreeNode:
  #     def __init__(self, x):
  #         self.val = x
  #         self.left = None
  #         self.right = None
  
  class Solution:
      def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
          if not preorder:
              return None
          loc = inorder.index(preorder[0])
          root = TreeNode(preorder[0])
          root.left = self.buildTree(preorder[1: loc+1], inorder[:loc])
          root.right = self.buildTree(preorder[loc+1:], inorder[loc+1:])
          return root
  ```

### <span id="jz08">JZ08.用两个栈实现队列</span>

**描述**

用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 appendTail 和 deleteHead ，分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，deleteHead 操作返回 -1 )

**思路**

只使用一个栈 stack1 当作队列，另一个栈 stack2 用来辅助操作。

要想将新加入的元素出现栈底，需要先将 stack1 的元素转移到 stack2，将元素入栈 stack1，最后将 stack2 的元素全部回到 stack1。

```python
class CQueue:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []
       
    def appendTail(self, value: int) -> None:
        while self.stack1:
            self.stack2.append(self.stack1.pop())
        self.stack1.appen(value)
        while self.stack2:
            self.stack1.append(self.stack2.pop())
            
    def deleteHead(self) -> int:
        if not self.stack1:
            return -1
        return self.stack1.pop()
```

也可以反过来

```python
class CQueue:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []
       
    def appendTail(self, value: int) -> None:
        self.stack1.append(value)

    def deleteHead(self) -> int:
        if self.stack2: return self.stack2.pop()
        if not self.stck1:
            return -1
        while self.stack1:
            self.stack2.append(self.stack1.pop())
           return self.stack2.pop()
```
### <span id="jz10">JZ10-Ⅰ.斐波那契数列</span>

**描述**

写一个函数，输入 n ，求斐波那契（Fibonacci）数列的第 n 项（即 F(N)）。斐波那契数列的定义如下：

F(0) = 0,   F(1) = 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
斐波那契数列由 0 和 1 开始，之后的斐波那契数就是由之前的两数相加而得出。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

**思路**

[面试题10- I. 斐波那契数列（动态规划，清晰图解） - 斐波那契数列](https://leetcode-cn.com/problems/fei-bo-na-qi-shu-lie-lcof/solution/mian-shi-ti-10-i-fei-bo-na-qi-shu-lie-dong-tai-gui/)

递归法：
原理： 把 f(n)f(n) 问题的计算拆分成 f(n-1)f(n−1) 和 f(n-2)f(n−2) 两个子问题的计算，并递归，以 f(0)f(0) 和 f(1)f(1) 为终止条件。
缺点： 大量重复的递归计算，例如 f(n)f(n) 和 f(n - 1)f(n−1) 两者向下递归需要 各自计算 f(n - 2)f(n−2) 的值。
记忆化递归法：
原理： 在递归法的基础上，新建一个长度为 nn 的数组，用于在递归时存储 f(0)f(0) 至 f(n)f(n) 的数字值，重复遇到某数字则直接从数组取用，避免了重复的递归计算。
缺点： 记忆化存储需要使用 O(N)O(N) 的额外空间。

```python
class Solution:
    def fib(self, n: int) -> int:
        res = [0, 1]
        for i in range(2, n+1):
            res.append(res[i-2]+res[i-1])
        return res[n]%1000000007
```

动态规划：
原理： 以斐波那契数列性质 f(n + 1) = f(n) + f(n - 1)f(n+1)=f(n)+f(n−1) 为转移方程。
从计算效率、空间复杂度上看，动态规划是本题的最佳解法。

```python
class Solution:
    def fib(self, n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, b+a
        return a%1000000007
```

### <span id="jz10-1">JZ10-Ⅱ.青蛙跳台阶问题</span>

**描述**

一只青蛙一次可以跳上1级台阶，也可以跳上2级台阶。求该青蛙跳上一个 n 级的台阶总共有多少种跳法。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

**思路**

- 设跳上 nn 级台阶有 f(n)f(n) 种跳法。在所有跳法中，青蛙的最后一步只有两种情况： 跳上 11 级或 22 级台阶。
  当为 1 级台阶： 剩 n−1 个台阶，此情况共有 f(n-1) 种跳法；
  当为 2 级台阶： 剩 n−2 个台阶，此情况共有 f(n-2) 种跳法。
- f(n) 为以上两种情况之和，即 f(n)=f(n-1)+f(n-2) ，以上递推性质为斐波那契数列。本题可转化为 求斐波那契数列第 nn 项的值 ，与 面试题10- I. 斐波那契数列 等价，唯一的不同在于起始数字不同。
  - 青蛙跳台阶问题： f(0)=1, f(1)=1, f(2)=2；
  - 斐波那契数列问题：f(0)=0, f(1)=1, f(2)=2。

```python
class Solution:
    def numWays(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a+b
        return a%1000000007
```

### <span id="jz11">JZ11.旋转数组的最小数字</span>

**描述**

把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。输入一个递增排序的数组的一个旋转，输出旋转数组的最小元素。例如，数组 [3,4,5,1,2] 为 [1,2,3,4,5] 的一个旋转，该数组的最小值为1。  

**思路**

二分法

```python
class Solution:
    def minArrary(self, numbers: [int]) -> int:
        i, j = 0, len(numbers)-1
        while i<j:
            if numbers[m] > numbers[j]: j=m+1
            elif numbers[m] < numbers[j]: i=m
            else: j-=1
        return numbers[i]
```

### <span id="jz12">[JZ12.矩阵中的路径](https://leetcode-cn.com/problems/ju-zhen-zhong-de-lu-jing-lcof/)</span>

**描述**

请设计一个函数，用来判断在一个矩阵中是否存在一条包含某字符串所有字符的路径。路径可以从矩阵中的任意一格开始，每一步可以在矩阵中向左、右、上、下移动一格。如果一条路径经过了矩阵的某一格，那么该路径不能再次进入该格子。例如，在下面的3×4的矩阵中包含一条字符串“bfce”的路径（路径中的字母用加粗标出）。

[["a","b","c","e"],
["s","f","c","s"],
["a","d","e","e"]]

但矩阵中不包含字符串“abfb”的路径，因为字符串的第一个字符b占据了矩阵中的第一行第二个格子之后，路径不能再次进入这个格子。

**思路**

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def dfs(i, j, k):
            if not 0<=i<len(board) or 0<=j<len(board[0]) or board[i][j]!= word[k]: return False
            if k==len(word) - 1: return True
            board[i][j] = ''
            res = dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or dfs(i, j-1, k+1) or dfs(i, j+1, k+1)
            board[i][j] = word[k]
            return res
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if dfs(i, j, 0): return True
        return False
```



### <span id="jz15">JZ15.二进制中1的个数</span>

**描述**

请实现一个函数，输入一个整数（以二进制串形式），输出该数二进制表示中 1 的个数。例如，把 9 表示成二进制是 1001，有 2 位是 1。因此，如果输入 9，则该函数输出 2。

**思路**

[循环判断](https://leetcode-cn.com/problems/er-jin-zhi-zhong-1de-ge-shu-lcof/solution/mian-shi-ti-15-er-jin-zhi-zhong-1de-ge-shu-wei-yun/)

根据 与运算 定义，设二进制数字 nn ，则有：
若 n \& 1 = 0，则 n 二进制 最右一位 为 0 ；
若 n&1=1 ，则 n 二进制 最右一位 为 1 。
根据以上特点，考虑以下 循环判断 ：
判断 n 最右一位是否为 1，根据结果计数。
将 nn 右移一位

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            res += n&1
            n >>= 1
        return res
```

n&(n+1)​

(n−1) 解析： 二进制数字 n 最右边的 1 变成 0 ，此 1 右边的 0 都变成 1 。
n \& (n - 1) 解析： 二进制数字 n 最右边的 1 变成 0 ，其余不变

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210327193950.png" style="zoom:40%">

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            res += 1
            n &= n-1
        return res
```



***

[Reference]

[Python单例模式(Singleton)的N种实现 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/37534850)