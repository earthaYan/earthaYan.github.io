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

#### 阻塞:

定义：没有严格定义，仅仅指的是代码运行的很慢，即在栈里表现很慢的东西都叫阻塞

```javascript
var foo = fetch("//foo.com");
var boo = fetch("//boo.com");
var coo = fetch("//coo.com");
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

- webAPI
  - DOM
  - Ajax
  - SetTimeout
- Callback queue
- event loop

## 阻塞的解决方法

### 提供回调函数

前提：浏览器和 node 中几乎没有阻塞的函数,都是非同步（异步）的

```javascript
console.log("hi");
setTimeout(() => {
  console.log("there");
}, 5000);
console.log("end");
```

{% asset_img timout.png setTimeout的栈 %}
为什么呢？原因是一次做一件事情指的是 js Runtime 只能同时做一件事，但浏览器不止有 RuntTime，还提供了其他的东西。所以我们可以同时做多件事,ajax 请求等其他 webAPI 同理
{% asset_img loop.png %}
注意：任务队列中的回调函数必须等 stack 中清空了才能入栈执行。

### Promise

宏任务：setTimeout/setInterval,回调函数将在下一个事件循环中执行
微任务：Promise,回调函数将会在下一个事件循环之前执行,作为本次事件循环的 task queue 的附加

### asyn...await

简化使用和编写链式 promise 的过程，返回值为 promise
多个请求写法：

```javascript
async function getAdd() {
  let [street, city, state] = await Promise.all([getStreet, getCity, getState]);
}
```

## async 函数返回值

根据返回值的类型，V8 引擎对返回值的处理方式也不一样
结论：async 函数在抛出返回值时，会根据**返回值类型**开启**不同数目的微任务**

### thenable

是一个对象或者函数
判断标准：某个对象或者函数是否具有 then(...)方法来判断

```javascript
if (
  p !== null &&
  (typeof p === "object" || typeof p === "function") &&
  typeof p.then === "function"
) {
  //thenable
} else {
  //非thenable
}
```

- 非 thenable，非 promise：不等待

```js
async function testA() {
  return 1;
}
testA().then(() => console.log(1));
Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));
// (不等待)最终结果👉: 1 2 3
```

- thenable：等待 1 个 then 的时间

```javascript
async function testB () {
     return {
         then (cb) {
             cb();
         }
     };
 }
 testB().then(() => console.log(1));
 Promise.resolve()
     .then(() => console.log(2))
     .then(() => console.log(3));
// (等待一个then)最终结果👉: 2 1 3
```

- promise:等待 2 个 then 的时间
```javascript
async function testC () {
    return new Promise((resolve, reject) => {
        resolve()
    })
}
testC().then(() => console.log(1));
Promise.resolve()
    .then(() => console.log(2))
    .then(() => console.log(3));
// (等待两个then)最终结果👉: 2 3 1
```


