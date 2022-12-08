---
title: 翻译-slice-length-vs-capacity-in-go
date: 2022-11-25 16:43:54
tags: [翻译, Go]
categories: 翻译
---

待完成
https://teivah.medium.com/slice-length-vs-capacity-in-go-af71a754b7d8

# Go 语言中的切片 length 和 capacity

<b>长话短说</b>:切片长度是指切片中可访问元素的数量,而切片容量是指从切片第一个元素开始,数组中元素的数量。

---

Go 开发者混淆或者没有完全理解切片 length 和 capacity 的现象非常普遍。理解这两个概念有利于高效地处理一些核心操作,比如初始化切片,使用 append 添加元素,复制,截取。而这种错误理解会导致切片滥用甚至内存泄漏。

在 Go 语言中, slice 是由数组返回的。这意味着切片的数据是持久化的存在一个数组形式的数据结构中。如果数组已经满了，切片可以处理添加元素的逻辑,或者如果数组几乎是空的话,切片也可以处理缩小数组的逻辑。

在计算机内部, 切片包含一个指向数组的指针,一个 length 属性和一个 capacity 属性。length 是切片包含的元素个数,而 capacity 是从切片第一个元素开始计算的背后数组的元素个数。让我们通过一些例子来让事情更清晰一些。首先通过给定的length和 capacity初始化切片：

```go
s := make([]int, 3, 6)  /// length 3, 容量 6 的切片
```

代表length的第一个参数是必须的，但是代表capacity的第二个参数是可选参数。图1展示了这段代码在内存中的执行结果。


