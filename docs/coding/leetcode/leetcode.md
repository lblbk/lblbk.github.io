### 索引

数组

查找

排序

动态规划

[preSum（前缀和）](#presum)

[连通域](#connected_component)

### 数据结构

#### 数组

[26. 删除有序数组中的重复项 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/)

循环读取，遇到不同的就替换下来

```c++
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        if(nums.empty()){
            return 0;
        }
        int index = nums.size();
        int sum=1;
        int t=1;
        for(int i=0;i<index-1;i++){
            if(nums[i+1]==nums[i]){
                continue;
            }
            else{
                nums[t] = nums[i+1];
                t++;
                sum++;
            }
        }
        return sum;
    }
};
```



### 算法

#### 查找

#### 排序

#### 动态规划

##### [509. 斐波那契数](https://leetcode-cn.com/problems/fibonacci-number/)

**描述**

斐波那契数，通常用 F(n) 表示，形成的序列称为 斐波那契数列 。该数列由 0 和 1 开始，后面的每一项数字都是前面两项数字的和。也就是：

```
F(0) = 0，F(1) = 1
F(n) = F(n - 1) + F(n - 2)，其中 n > 1
```

给你 n ，请计算 F(n) 。

**思路**

```c++
class Solution {
public:
    int fib(int n) {
        if (n<2) return n;
        int prev = 0, curr = 1;
        for (int i=0; i<n-1; i++){
            int sum = prev + curr;
            prev = curr;
            curr = sum;
        }
        return curr;
    }
};
```

具体很多思路源于此篇文章 [动态规划详解 (qq.com)](https://mp.weixin.qq.com/s/1V3aHVonWBEXlNUvK3S28w)

###### [322. 零钱兑换](https://leetcode-cn.com/problems/coin-change/)

**描述**

给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount ，表示总金额。

计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 -1 。

你可以认为每种硬币的数量是无限的。

**思路**

```c++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount+1, amount+1);
        dp[0] = 0;
        for (int i=0; i<dp.size(); i++){
            for (int coin: coins){
                if (i-coin<0) continue;
                dp[i] = min(dp[i], 1+dp[i-coin]);
            }
        }
        return dp[amount] == amount+1 ? -1 : dp[amount];
    }
};
```



#### <span id="presum">preSum（前缀和）</span>

303.区域和检索-数组不可变

**描述**

给定一个整数数组  nums，求出数组从索引 i 到 j（i ≤ j）范围内元素的总和，包含 i、j 两点。

实现 NumArray 类：

NumArray(int[] nums) 使用数组 nums 初始化对象
int sumRange(int i, int j) 返回数组 nums 从索引 i 到 j（i ≤ j）范围内元素的总和，包含 i、j 两点（也就是 sum(nums[i], nums[i + 1], ... , nums[j])）

**思路**

[preSum（前缀和）](https://leetcode-cn.com/problems/range-sum-query-immutable/solution/presum-qian-zhui-he-xiang-xi-jiang-jie-b-nh23/)

求一个区间 [i, j] 内的和，求区间和可以用 preSum 来做。

preSum 方法能快速计算指定区间段 i - ji−j 的元素之和。它的计算方法是从左向右遍历数组，当遍历到数组的 ii 位置时，preSum 表示 ii 位置左边的元素之和。

假设数组长度为 NN，我们定义一个长度为 N+1N+1 的 preSum 数组，preSum[i] 表示该元素左边所有元素之和（不包含 i 元素）。然后遍历一次数组，累加区间 [0, i)[0,i) 范围内的元素，可以得到 preSum 数组。

求 preSum 的代码如下：

```python
N = len(nums)
preSum = range(N + 1)
for i in range(N):
    preSum[i + 1] = preSum[i] + nums[i]
print(preSum)
```

利用 preSum 数组，可以在 O(1) 的时间内快速求出 nums 任意区间 [i, j] (两端都包含) 的各元素之和。

sum(i, j) = preSum[j + 1] - preSum[i]

对于本题，可以在 NumArray 类的构造函数的里面，求数组每个位置的 preSum；当计算sumRange(i, j)的时候直接返回 preSum[j + 1] - preSum[i] 可以得到区间和。

```python
class Solution:
    def __init__(self, nums: List[int]):
        N = len(nums)
        self.preSum = [0] * (N+1)
        for i in range(N):
            self.preSum[i+1] = self.preSum[i] + nums[i]
            
     def sumRange(self, i: int, j: int)->int:
        return self.preSum[j+1] - self.preSum[i]
```

304.二维区域和检索 - 矩阵不可变

**描述**

给定一个二维矩阵，计算其子矩形范围内元素的总和，该子矩阵的左上角为 `(row1, col1)` ，右下角为 `(row2, col2)` 。

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210303173815.png" alt="Range Sum Query 2D" style="zoom:33%;" />

上图子矩阵左上角 (row1, col1) = **(2, 1)** ，右下角(row2, col2) = **(4, 3)，**该子矩形内元素的总和为 8。

**思路**

[如何求二维的前缀和，以及用前缀和求子矩形的面积](https://leetcode-cn.com/problems/range-sum-query-2d-immutable/solution/ru-he-qiu-er-wei-de-qian-zhui-he-yi-ji-y-6c21/)

步骤一：求 preSum
我们先从如何求出二维空间的 preSum[i][j]。

我们定义 preSum[i][j]preSum[i][j] 表示 从 [0,0] 位置到 [i,j] 位置的子矩形所有元素之和。
可以用下图帮助理解：

$S(O, D) = S(O, C) + S(O, B) - S(O, A) + D$

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210303175753.jpeg" alt="304.001.jpeg" style="zoom: 25%;" />

减去 S(O, A) 的原因是 S(O, C) 和 S(O, B)中都有 S(O, A), 即加了两次 S(O, A)，所以需要减去一次 S(O, A)。

如果求 preSum[i][j]preSum[i][j] 表示的话，对应了以下的递推公式：

$preSum[i][j] = preSum[i - 1][j] + preSum[i][j - 1] - preSum[i - 1][j - 1] + matrix[i][j]$

步骤二：根据 preSum 求子矩形面积
前面已经求出了数组中从 [0,0] 位置到 [i,j]位置的 preSum。下面要利用 preSum[i][j]preSum[i][j] 来快速求出任意子矩形的面积。

同样利用一张图来说明：

$S(A, D) = S(O, D) - S(O, E) - S(O, F) + S(O, G)$

<img src="https://cdn.jsdelivr.net/gh/lblbk/picgo/work/20210303175803.jpeg" alt="304.002.jpeg" style="zoom:25%;" />

加上子矩形 S(O, G) 面积的原因是 S(O, E) 和 S(O, F) 中都有 S(O, G)，即减了两次 S(O, G)，所以需要加上一次 S(O, G)。

如果要求 [row1, col1]到 [row2, col2] 的子矩形的面积的话，用 preSum 对应了以下的递推公式：

$preSum[row2][col2] - preSum[row2][col1 - 1] - preSum[row1 - 1][col2] + preSum[row1 - 1][col1 - 1]$

```python
class NumMatrix:
    def __inint__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            M, N = 0, 0
        else:
            M, N = len(matrix), len(matrix[0])
        self.preSum = [[0]*(N+1) for _ in range(M+1)]
        for i in range(M):
            for j in range(N):
                self.preSum[i+1][j+1] = self.preSum[i][j+1] + self.preSum[i+1][j] - self.preSum[i][j] + matrix[i][j]
    
    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.preSum[row2+1][col2+1] - self.preSum[row2+1][col1] - self.preSum[row1][col2+1] + self.preSum[row1][col1]
```

##### <span id="connected_component">连通域</span>

[200. 岛屿数量](https://leetcode-cn.com/problems/number-of-islands/)

**描述**

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

**思路**

*   目标是找到矩阵中 “岛屿的数量” ，上下左右相连的 `1` 都被认为是连续岛屿。
*   **dfs方法：**  设目前指针指向一个岛屿中的某一点 `(i, j)`，寻找包括此点的岛屿边界。
    *   从 `(i, j)` 向此点的上下左右 `(i+1,j)`,`(i-1,j)`,`(i,j+1)`,`(i,j-1)` 做深度搜索。
    *   终止条件：
        *   `(i, j)` 越过矩阵边界;
        *   `grid[i][j] == 0`，代表此分支已越过岛屿边界。
    *   搜索岛屿的同时，执行 `grid[i][j] = '0'`，即将岛屿所有节点删除，以免之后重复搜索相同岛屿。
*   **主循环：** 
    *   遍历整个矩阵，当遇到 `grid[i][j] == '1'` 时，从此点开始做深度优先搜索 `dfs`，岛屿数 `count + 1` 且在深度优先搜索中删除此岛屿。
*   最终返回岛屿数 `count` 即可。

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(grid, i, j):
            if not 0 <= i < len(grid) or not 0 <= j < len(grid[0]) or grid[i][j] == '0': return
            grid[i][j] = '0'
            dfs(grid, i+1, j)
            dfs(grid, i-1, j)
            dfs(grid, i, j+1)
            dfs(grid, i, j-1)
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    dfs(grid, i, j)
                    count += 1
        return count
```

[463. 岛屿的周长](https://leetcode-cn.com/problems/island-perimeter/)

**描述**

给定一个 `row x col` 的二维网格地图 `grid` ，其中：`grid[i][j] = 1` 表示陆地， `grid[i][j] = 0` 表示水域。

网格中的格子 **水平和垂直** 方向相连（对角线方向不相连）。整个网格被水完全包围，但其中恰好有一个岛屿（或者说，一个或多个表示陆地的格子相连组成的岛屿）。

岛屿中没有“湖”（“湖” 指水域在岛屿内部且不和岛屿周围的水相连）。格子是边长为 1 的正方形。网格为长方形，且宽度和高度均不超过 100 。计算这个岛屿的周长。

[695. 岛屿的最大面积](https://leetcode-cn.com/problems/max-area-of-island/)

**描述**

给定一个包含了一些 `0` 和 `1` 的非空二维数组 `grid` 。

一个 **岛屿** 是由一些相邻的 `1` (代表土地) 构成的组合，这里的「相邻」要求两个 `1` 必须在水平或者竖直方向上相邻。你可以假设 `grid` 的四个边缘都被 `0`（代表水）包围着。

找到给定的二维数组中最大的岛屿面积。(如果没有岛屿，则返回面积为 `0` 。)



[12. 整数转罗马数字](https://leetcode-cn.com/problems/integer-to-roman/)

**描述**

罗马数字包含以下七种字符： I， V， X， L，C，D 和 M。

字符          数值
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
例如， 罗马数字 2 写做 II ，即为两个并列的 1。12 写做 XII ，即为 X + II 。 27 写做  XXVII, 即为 XX + V + II 。

通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，例如 4 不写做 IIII，而是 IV。数字 1 在数字 5 的左边，所表示的数等于大数 5 减小数 1 得到的数值 4 。同样地，数字 9 表示为 IX。这个特殊的规则只适用于以下六种情况：

I 可以放在 V (5) 和 X (10) 的左边，来表示 4 和 9。
X 可以放在 L (50) 和 C (100) 的左边，来表示 40 和 90。 
C 可以放在 D (500) 和 M (1000) 的左边，来表示 400 和 900。
给你一个整数，将其转为罗马数字。

**题解**

对应方式写出来，解题就简单了，哈希表和两个列表都可实现

```python
class Solution:
    def intToRoman(self, num: int) -> str:
      # 使用哈希表，按照从大到小顺序排列
        hashmap = {1000:'M', 900:'CM', 500:'D', 400:'CD', 100:'C', 90:'XC', 50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
        res = ''
        for key in hashmap:
          if num // key != 0:
            count = num // key
            res += hashmap[key]*count
            num %= key
        return res
      
class Solution:
    def intToRoman(self, num: int) -> str:
        list1=[1000,900,500,400,100,90,50,40,10,9,5,4,1]
        list2=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I']
        result=""
        for i in range(len(list1)):
            while num>=list1[i]:
                result+=list2[i]
                num-=list1[i]
        return result
```



