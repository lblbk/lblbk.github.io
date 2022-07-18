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

