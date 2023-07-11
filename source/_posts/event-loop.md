---
title: event-loop
date: 2023-07-11 10:35:48
tags: [JavaScript]
categories: 前端
---

### 术语解释

#### 单线程：

单线程==有且仅有一个调用栈==一次做一件事情==程序每次只可以运行一段代码

#### 调用栈：

记录当前程序所在位置的数据结构。如果当前进入了某个函数，这个函数就会被放入栈中，如果当前离开了某个函数，这个函数就会被弹出栈外

```javascript
function multiply(a, b) {
  return a * b;
}
function square(n) {
  return multiply(n, n);
}
function printSquare(n) {
  var squared = square(n);
  console.log(squared);
}
printSquare(4);
```

1. main():指代文件自身，放入栈中
2. 从上到下查看声明的函数，最后是`printSquare`，最终是其被调用
3. 将`printSquare`推入栈中，`printSquare`调用了`square`
4. 将`square`推入栈中，`square`调用了`multiply`
5. 将`multiply`推入栈中
6. 得到`multiply`返回值


### V8 运行环境

{% asset_img js.png 运行环境示意图 %}

#### V8 引擎【V8 运行环境】

- 堆 heap:记录内存分配
- 栈 stack: 存储执行上下文

#### V8 外部【浏览器提供】

- WebAPI
- Ajax
- SetTimeout
- Callback queue
- event loop
