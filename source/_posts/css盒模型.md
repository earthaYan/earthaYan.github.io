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
## 清除浮动
### 方法
1. 在需要清除浮动的元素后面添加一个空白标签，设置类名 clear，设置 `clear: both` 
2. 父级元素添加 `overflow: hidden`
3. 父元素 `display：table`
4. 伪元素清除浮动

```css
.clearfix:after {
  /*正常浏览器 清除浮动*/
  content: '';
  display: block;
  height: 0;
  clear: both;
  visibility: hidden;
}
```
### 原理
- clear 属性清除浮动：clear 属性规定元素盒子的边不能和浮动元素相邻。该属性只能影响使用清除的元素本身，不能影响其他元素。换而言之，如果已经存在浮动元素的话，那么该元素就不会像原本元素一样受其影响了。
- 其他的可以归为一类，都是通过触发 BFC 来实现的
