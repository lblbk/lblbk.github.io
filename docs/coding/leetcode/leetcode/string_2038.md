# 题目

**描述**

#### 2038. 如果相邻两个颜色均相同则删除当前颜色

**思路**

这个思路也是直接暴力循环，不过这里两个判断采用一个变量维护

这里要注意字符串的格式化输出，以及但双引号的区别

```cc
class Solution {
public:
    bool winnerOfGame(string colors) {
        int count = 0;
        for (int i=1; i<colors.size(); i++)
        {
            if (colors[i-1]=='A'&&colors[i]=='A'&&colors[i+1]=='A')
                count++;
            if (colors[i-1]=='B'&&colors[i]=='B'&&colors[i+1]=='B')
                count--;
        }
        return count>0;
    }
};
```

