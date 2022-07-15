## 题目

**描述**

[21. 合并两个有序链表 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/merge-two-sorted-lists/)

**思路**

[合并两个有序链表](https://labuladong.github.io/algo/2/17/16/#合并两个有序链表)

https://leetcode-cn.com/problems/merge-two-sorted-lists/comments/229111

[【链表】 21.合并两个有序链表 一题双解 （C++） - 合并两个有序链表 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/merge-two-sorted-lists/solution/lian-biao-21he-bing-liang-ge-you-xu-lian-24eq/)

```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode *p=list1;
        ListNode *q=list2;
        // //总是指向更小的元素
        //ListNode *prev = new ListNode(0);
        // // 方便结果的返回
        //ListNode *head=prev;
      	// 上面这种方法声明链表不删除的话会造成内存泄漏 这种方法声明更简单
        ListNode prev(0);
        ListNode *head=&prev;
        while (p!=nullptr && q!=nullptr){
            if (p->val > q->val){
                head->next = q;
                q = q->next;
            }
            else{
                head->next = p;
                p = p->next;
            }
            head = head->next;
        }
        if (p != nullptr){
            head->next = p;
        }
        if (q != nullptr){
            head->next = q;
        }
      	// 这里可以有两种写法 下面这种更简单
        // head->next = p ? p : q;
        // return prev->next;
      	// 这里返回也要做相应修改 用.
      	return prev.next;
    }
};
```

Tips: 如果newHead是ListNode类型，那访问他的成员变量(好像是叫这个名字)就用点，newHead.next或者newHead.val，如果newHead是个ListNode*类型的指针，那么访问他的成员变量就要用->，就是newHead->next，或者newHead->val，具体用点还是->就只与newHead的类型有关