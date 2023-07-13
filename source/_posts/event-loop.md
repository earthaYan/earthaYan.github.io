---
title: event-loop
date: 2023-07-11 10:35:48
tags: [JavaScript]
categories: 前端
---

画图工具：https://www.liuchengtu.com/charts/

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
6. 得到`multiply`返回值，将`multiply`推出栈
7. 依次执行并将函数推出栈

{% asset_img stack.png 栈过程示意图%}
如果我们在 `multiply`中使用 throw 抛出错误，则控制台会出现：

```javascript
preview-9c596f222c88a.js:2 Error: 报错信息
    at multiply (script.js:2:11)
    at square (script.js:5:12)
    at printSquare (script.js:8:19)
    at script.js:11:1
```

典型场景：内存溢出
{%asset_img overflow.jpg 栈溢出%}
报错信息：

```javascript
RangeError: Maximum call stack size exceeded
    at foo (script.js:12:5)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
    at foo (script.js:12:12)
```

#### 阻塞

定义：没有严格定义，仅仅指的是代码运行的很慢，即在栈里表现很慢的东西都叫阻塞

```javascript
var foo = fetch('//foo.com');
var boo = fetch('//boo.com');
var coo = fetch('//coo.com');
console.log(foo);
console.log(boo);
console.log(coo);
```

{% asset_img fetch.png 网络请求导致的阻塞%}
如上所示：当上面所有的代码都跑一遍，栈才会被清空。而 JS 是单线程语言，所以我们如果请求一个资源，就只能等着请求完成。
导致的问题：代码需要在浏览器上运行，请求期间不能做其他任何操作，导致页面卡住运行不流畅

### V8 运行环境

{% asset_img js.png 运行环境示意图 %}

#### V8 引擎【V8 chrome 中的运行环境】

- 堆 heap:记录内存分配
- 栈 stack: 存储执行上下文

#### V8 外部【浏览器提供】

- WebAPI
- Ajax
- SetTimeout
- Callback queue
- event loop

## 阻塞的解决方法

### 提供异步回调函数

前提：浏览器和 node 中几乎没有阻塞的函数,都是非同步（异步）的

#### setTimeout
