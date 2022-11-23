---
title: 翻译-slice-length-vs-capacity-in-go
date: 2022-11-25 16:43:54
tags: [翻译, Go]
categories: 翻译
---

待完成
https://teivah.medium.com/slice-length-vs-capacity-in-go-af71a754b7d8

# Go 语言中的切片 length 和 capacity

<b>长文预警,慎入 </b>:切片长度是指切片中可访问元素的数量,而切片容量是指从切片第一个元素开始,数组中元素的数量。

---

对于 Go 开发者来说,混淆或者没有完全理解切片 length 和 slice 的概念是很普遍的。理解这两个概念对于高效处理类似切片初始化,使用 append 添加元素,复制,切片这样的核心操作是非常重要的。这种错误理解会导致非最优的使用切片甚至是内存泄漏。

在 Go 语言中,
