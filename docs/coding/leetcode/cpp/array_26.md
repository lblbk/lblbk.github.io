## 题目

**描述**

[26. 删除有序数组中的重复项 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/)

**思路**

循环读取，遇到不同的就替换下来

```cpp
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

