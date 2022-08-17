---
title: css盒模型
date: 2022-08-17 09:59:18
tags: [css]
categories: CSS
---
## css盒模型
1. content：内容，容纳着元素的”真实“内容，例如文本，图像或是视频播放器
2. padding：内边距
3. border：边框
4. margin：外边距
---
## 两种盒模型的区别：

- W3C 盒模型 box-sizing: content-box
  - W3C 盒模型中，通过 CSS 样式设置的 width 的大小只是 content 的大小

- IE 盒模型 box-sizing: border-box
  - IE 盒模型中，通过 CSS 样式设置的 width 的大小是 content + padding + border 的和
---
## margin/padding 设置百分比是相对谁的
margin/padding 设置百分比都是相对于父盒子的宽度(width 属性)

---

## 