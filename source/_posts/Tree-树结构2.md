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
type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func preorderTraversal(root *TreeNode) []int {
	var nodes = make([]int, 0)
	//DLR
	if root == nil {
		return nodes
	}
	nodes = append(nodes, root.Val)
	if root.Left != nil {
		nodes = append(nodes, preorderTraversal(root.Left)...)
	}
	if root.Right != nil {
		nodes = append(nodes, preorderTraversal(root.Right)...)
	}
	return nodes
}
```

### 中根遍历 LDR

遍历顺序：左子树-根节点-右子树

```go
func inorderTraversal(root *TreeNode) []int {
	nodes := make([]int, 0)
	// LDR
	if root == nil {
		return nodes
	}
	if root.Left != nil {
		nodes = append(nodes, inorderTraversal(root.Left)...)
	}
	nodes = append(nodes, root.Val)
	if root.Right != nil {
		nodes = append(nodes, inorderTraversal(root.Right)...)
	}
	return nodes
}
```

### 后根遍历 LRD

遍历顺序：左子树-右子树-根节点

```go
func postorderTraversal(root *TreeNode) []int {
	// LRD
	var nodes = make([]int, 0)
	if root == nil {
		return nodes
	}
	if root.Left != nil {
		nodes = append(nodes, inorderTraversal(root.Left)...)
	}
	if root.Right != nil {
		nodes = append(nodes, inorderTraversal(root.Right)...)
	}
	nodes = append(nodes, root.Val)
	return nodes
}
```

## 二叉树的实际应用

1. 求二叉树各个节点的层数
   节点的层数是父节点的层数+1，故可以先求父亲节点的层数，即先序遍历

2. 求二叉树各个节点的高度
   从下而上，即后序遍历
3. 求给定节点的所有子孙节点,结合先序遍历和后序遍历
