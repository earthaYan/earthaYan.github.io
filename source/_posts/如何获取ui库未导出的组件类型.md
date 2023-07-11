---
title: 如何获取ui库未导出的组件类型
date: 2023-03-09 20:20:24
tags: [TypeScript]
categories: 前端
---

antd有一些组件的props属性并没有导出，但是项目里又需要用到，可以用下面这个方法来获取

```TypeScript
type SelectProps = React.ComponentProps<typeof Select>;
```