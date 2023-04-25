---
title: React的createPortal
date: 2023-04-25 10:12:22
tags: [react, 前端]
categories: 前端
---

# React.createPortal()

作用：把部分子组件渲染到不同于父组件 DOM 节点的指定 DOM 节点

使用：
`React.createPortal(children,domNode)`

## 基本使用

```javascript
import { createPortal } from 'react-dom';
<div>
  <p>This child is placed in the parent div.</p>
  {createPortal(
    <p>This child is placed in the document body.</p>,
    document.body
  )}
</div>;
```

## 限制

portal 只会改变 DOM 节点的物理位置，但是渲染成 portal 的 JSX 仍然是渲染 JSX 的 React 组件的子节点。

- 子组件仍然可以访问父组件树提供的上下文
- 事件根据 React 树从子级冒泡到父级

## 函数

### 入参

1. children:可以使用 React 渲染的：JSX 片段，<></>,字符串，数字，或者一组这些元素
2. domNode:已经存在的 DOM 节点，在更新期间传不同的 DOM 节点会导致不断重建 portal 内容

### 返回值

返回一个可以包含在 JSX 中或者可以从 React 组件返回的 React 节点

### 注意点

- 来自 portal 的事件是根据 React 树传播而不是 DOM 树。

```html
<div id="root"></div>
<div id="name">111</div>
<script>
  //点击Demo组件portal组件中的p时，点击事件不会冒泡到dom树的节点，这里不会执行
  document.getElementById('name').onclick = function () {
    console.log('hello world');
  };
</script>
```

```jsx
import { createPortal } from 'react-dom';

const Demo = () => {
  return (
    // 点击Demo组件portal组件中的p时，这里的onClick会执行，因为React组件树的事件冒泡
    <div style={{ border: '2px solid black' }} onClick={()=>console.log("root div click")}>
      <p>This child is placed in the parent div.</p>
      {createPortal(
        <p onClick={() => console.log('portal click')}>
          This child is placed in the name
        </p>,
        document.getElementById('name') as Element
      )}
    </div>
  );
};
```

- 挂载节点必须是已经存在的节点，不可以是当前 JSX 片段中的 dom 节点

```jsx
// 正常展示
const App1 = () => {
  const [popupContainer, setPopupContainer] = React.useState(null);

  React.useEffect(() => {
    const popupDiv = document.getElementById('sister');
    setPopupContainer(popupDiv);
  }, []);
  return (
    <React.Fragment>
      <div id="sister">外部兄弟</div>
      <div id="container">
        <div id="inner">内部兄弟</div>
        {/* 正常展示1 */}
        {!!popupContainer && createPortal(<p>portal内容</p>, popupContainer)}
        {/* 正常展示2 */}
        {document.getElementById('sister') &&
          createPortal(<p>portal内容</p>, document.getElementById('sister'))}
        {/* 报错:Target container is not a DOM element. */}
        {createPortal(<p>portal内容</p>, document.getElementById('sister'))}
      </div>
    </React.Fragment>
  );
};
export default App1;
```

## 使用

### 创建 portal

```jsx
import { createPortal } from 'react-dom';
export default function MyComponent() {
  return (
    <div style={{ border: '2px solid black' }}>
      <p>This child is placed in the parent div.</p>
      {createPortal(
        <p>This child is placed in the document body.</p>,
        document.body
      )}
    </div>
  );
}
```

{% asset_img portal1.jpg %}

### 使用 portal 渲染对话框弹窗

可以避免调用在对话框的组件使用了 overflow:hidden 或者其他样式的情况下，不能展示悬浮对话框

### 将 React 组件渲染为非 React 服务端页面标记

React root 如果是非 React 构建的静态页面或者服务端渲染页面的一部分，就可以利用 portals 在静态区域创建交互区域，比如 sideBars

与多 React root 的区别：

- 即使内部渲染成 DOM 的不同部分，portal 也可以将这个应用作为一个<font color="red">状态共享</font>的 React 树去对待

### 将 React 组件渲染成非 React 的 DOM 节点

用 portal 管理 React 外部的 DOM 节点的内容。

```jsx
const App = () => {
  // 1. 定义状态变量popupContainer存储要渲染的目标节点
  const [popupContainer, setPopupContainer] = useState(null);
  useEffect(() => {
    if (mapRef.current === null) {
      const map = createMapWidget(containerRef.current);
      mapRef.current = map;
      // 2. 当创建第三方组件时，存储组件返回的DOM 节点，这样你可以将内容渲染到这个DOM节点
      const popupDiv = addPopupToMapWidget(map);
      setPopupContainer(popupDiv);
    }
  }, []);
  return (
    <div style={{ width: 250, height: 250 }} ref={containerRef}>
      {/* 一旦popupContainer变成可访问状态，
    使用createPortal渲染React内容到popupContainer容器中 */}
      {popupContainer !== null &&
        createPortal(<p>Hello from React!</p>, popupContainer)}
    </div>
  );
};
```

完整例子见：https://stackblitz.com/edit/react-ts-cwfhhp?file=App.tsx

```jsx
// 核心代码
export default function App() {
  const containerRef = React.useRef(null);
  const mapRef = React.useRef(null);
  const [popupContainer, setPopupContainer] = React.useState(null);
  React.useEffect(() => {
    if (mapRef.current === null) {
      const map = createMapWidget(containerRef.current);
      mapRef.current = map;
      const popupDiv = addPopupToMapWidget(map);
      setPopupContainer(popupDiv);
    }
  }, []);
  return (
    <div style={{ width: 250, height: 250 }} ref={containerRef}>
      {popupContainer !== null &&
        createPortal(<p>Hello from React!</p>, popupContainer)}
    </div>
  );
}
```
