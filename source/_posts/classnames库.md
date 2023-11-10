---
title: classnames库
date: 2023-11-10 15:54:36
tags: [css, javascript]
categories: javascript
---

在看以前的代码中，经常看到类似`classnames`或者`className`这种函数,大概知道和 css 中的类名有关，但是具体的用法以及原理并不了解，这次正好借助项目中使用的[`classnames`库](https://www.npmjs.com/package/classnames)了解一下。

库更新日志:[changeLog](https://github.com/JedWatson/classnames/blob/main/HISTORY.md)

## classname 类函数的主要作用

通常用于动态地构建一个包含多个类名的字符串，然后将其应用于 HTML 元素的 class 属性。

## 安装和使用

### 在项目中添加 `classnames` 库

代码：`yarn add classnames`

### 导入和使用

- 在 Node.js, Browserify, 或者 webpack 中:

```js
const classNames = require("classnames");
classNames("foo", "bar");
// => 'foo bar'
```

- 在 React 组件中：

```js
import classNames from "classnames";
classNames("foo", "bar");
// => 'foo bar'
```

## 日常使用

### 基本用法

#### 参数类型：string 或者 object,可以传入多个参数

```js
classNames("foo");
classNames({
  foo: true,
});
```

上面这两种方式的效果是一样的，前者可以看作是后者的缩写形式。如果传入对象的 key 对应的 value 是 Falsy 值,则最终生成的 html 元素的 class 字符串中不包含这个 class。

```js
classNames("foo", { bar: true, duck: false }, "baz", { quux: true }); // => 'foo bar baz quux'
classNames("bar", 0, 1, { baz: null }, ""); // => 'bar 1'
```

> 1. 非 falsy 的 number 会被自动转换为 string,成为类名之一

#### 参数中包含数组

处理方法：会按照上述规则递归展平

```js
const arr = ["b", { c: true, d: false }];
classNames("a", arr); // => 'a b c'
```

### 使用 ES2015（即 ES6）的语法和特性时，如何实现动态的类名设置

```js
let buttonType = "primary";
classNames({ [`btn-${buttonType}`]: true });
```

### React 中的用法

#### 使用场景

使动态类名和条件类名使用起来更简单

以生成 button 的 className prop 为例

```js
// 原写法:字符串拼接
import React, { useState } from "react";
export default function Button(props) {
  const [isPressed, setIsPressed] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  let btnClass = "btn";
  if (isPressed) btnClass += " btn-pressed";
  else if (isHovered) btnClass += " btn-over";
  return (
    <button
      className={btnClass}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {props.label}
    </button>
  );
}
```

借助 classnames 库的 object 参数类型使用会更简单

```js
import React, { useState } from "react";
import classNames from "classnames";
export default function Button(props) {
  const [isPressed, setIsPressed] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const btnClass = classNames({
    btn: true,
    "btn-pressed": isPressed,
    "btn-over": !isPressed && isHovered,
  });
  return (
    <button
      className={btnClass}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {props.label}
    </button>
  );
}
```

### `dedupe` 版本

作用：类名去重
缺陷：功能更完善，但运行速度大概慢了 5 倍
引入：

```js
const classNames = require("classnames/dedupe");
classNames("foo", "foo", "bar"); // => 'foo bar'
classNames("foo", { foo: false, bar: true }); // => 'bar'
```

> 注意：如果有重复的类名，后者的状态会覆盖前者

### `bind`版本

作用：对于 css-module 特别有用，将抽象的类名绑定到实际的 className 输出
css modules 缺陷：
使用 CSS Modules 时，类名经常被转换为哈希值或者其他形式的独一无二的标识符，以确保全局唯一性。然而，当需要将这些抽象的类名应用于实际的 DOM 元素时，就需要将它们与实际的 className 值进行绑定。

```js
const classNames = require("classnames/bind");
const styles = {
  foo: "abc",
  bar: "def",
  baz: "xyz",
};
const cx = classNames.bind(styles);
const className = cx("foo", ["bar"], { baz: true }); // => 'abc def xyz'
```

实际例子：

```css
/* styles.module.css */
.button {
  background-color: red;
}

.link {
  color: blue;
}
```

```js
import classNames from "classnames/bind";
import styles from "./styles.module.css";

const bindClassNames = classNames.bind(styles);

const buttonClass = bindClassNames("button");
const linkClass = bindClassNames("link");

// 使用生成的类名
return (
  <div>
    <button className={buttonClass}>Click me</button>
    <a href="#" className={linkClass}>
      Link
    </a>
  </div>
);
```
