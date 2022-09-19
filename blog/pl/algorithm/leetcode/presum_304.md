304.二维区域和检索 - 矩阵不可变

**描述**

给定一个二维矩阵，计算其子矩形范围内元素的总和，该子矩阵的左上角为 `(row1, col1)` ，右下角为 `(row2, col2)` 。

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210303173815.png" alt="Range Sum Query 2D" style="zoom:33%;" />

上图子矩阵左上角 (row1, col1) = **(2, 1)** ，右下角(row2, col2) = **(4, 3)，**该子矩形内元素的总和为 8。

**思路**

[如何求二维的前缀和，以及用前缀和求子矩形的面积](https://leetcode-cn.com/problems/range-sum-query-2d-immutable/solution/ru-he-qiu-er-wei-de-qian-zhui-he-yi-ji-y-6c21/)

步骤一：求 preSum
我们先从如何求出二维空间的 preSum[i][j]。

我们定义 preSum[i][j]preSum[i][j] 表示 从 [0,0] 位置到 [i,j] 位置的子矩形所有元素之和。
可以用下图帮助理解：

$S(O, D) = S(O, C) + S(O, B) - S(O, A) + D$

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210303175753.jpeg" alt="304.001.jpeg" style="zoom: 25%;" />

减去 S(O, A) 的原因是 S(O, C) 和 S(O, B)中都有 S(O, A), 即加了两次 S(O, A)，所以需要减去一次 S(O, A)。

如果求 preSum[i][j]preSum[i][j] 表示的话，对应了以下的递推公式：

$preSum[i][j] = preSum[i - 1][j] + preSum[i][j - 1] - preSum[i - 1][j - 1] + matrix[i][j]$

步骤二：根据 preSum 求子矩形面积
前面已经求出了数组中从 [0,0] 位置到 [i,j]位置的 preSum。下面要利用 preSum[i][j]preSum[i][j] 来快速求出任意子矩形的面积。

同样利用一张图来说明：

$S(A, D) = S(O, D) - S(O, E) - S(O, F) + S(O, G)$

<img src="https://gcore.jsdelivr.net/gh/lblbk/picgo/work/20210303175803.jpeg" alt="304.002.jpeg" style="zoom:25%;" />

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

#### 