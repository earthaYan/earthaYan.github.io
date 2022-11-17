---
title: Tree-树结构2
date: 2022-11-07 23:48:09
tags: [算法, 树结构, LeetCode]
categories: 算法
mathjax: true
---

## 学习目标

1. <font color=red>准确描述</font>前/中/后序三种递归的遍历<font color=red>算法思想</font>
2. <font color=red>编程实现</font>三种遍历算法
3. 对于给定二叉树,能够<font color=red>图示</font>递归遍历过程中<font color=red>栈</font>的变化

## 二叉树遍历

指的是按照一定的规律 <font color=red>访问 </font>二叉树的每个节点,且只访问一次
结果：二叉树【非线性】->线性表

- 先根遍历 DLR
  - 思想：先访问二叉树的根,然后访问二叉树的左子树,再访问二叉树的右子树
  - 本质：递归遍历,对二叉树的左右子树的访问也是先根遍历
- 中根遍历 LDR
  - 思想：先访问二叉树的左子树，再访问二叉树的根，最后访问二叉树的右子树
  - 本质：递归遍历,对二叉树的左右子树的访问也是中根遍历
- 后根遍历 LRD
  - 思想：先访问二叉树的左子树，再访问访问二叉树的右子树，最后二叉树的根
  - 本质：递归遍历,对二叉树的左右子树的访问也是后根遍历
  - 最后一个节点是根节点

### 步骤

1. 确定二叉树的存储方式
   常用的为双链表结构【待学章节：链表】
2.

### 先根遍历 DLR

1. 如果当前二叉树(包括子树)为空,则什么也不做
2. 否则进行先序遍历
   a. 访问该二叉树的根节点
   b. 递归地先根遍历该二叉树的左子树
   c. 递归地先根遍历该二叉树的右子树
3. 递归算法结束条件就是树为空

#### 编程实现

1. 确定二叉树的存储方式——定义双链表结构

```go
type TreeNode struct{
  data int
  leftSon *TreeNode
  rightSon *TreeNode
}
func visit(tree){
  fmt.Printf("%v ",tree.data)
}
func preOrder(tree) {
  if(tree ==nil){
    return
  }
  visit(tree)
  preOrder(tree.leftSon)
  preOrder(tree.rightSon)
}
func main(){
  preOrder(rootNode)
}
```

### 中根遍历 LDR

遍历顺序：左子树-根节点-右子树

### 后根遍历 LRD

遍历顺序：左子树-右子树-根节点
