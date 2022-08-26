---
title: Mutation Observer
urlname: qv0s9s
date: '2021-12-13 10:17:27 +0800'
tags: []
categories: []
---

## 背景：

dtle 由于客户要求页面不能出现 dtle 字样，预期有一个新需求：需要将文本 dtle 全局替换为 dts，这就需要检测 DOM 变化，一旦监听到 DOM 中有符合条件的文本，就需要执行内容替换，而要实现对 DOM 变化的检测监听并做出相应处理，需要用到 MutationObserver

## 与 Mutation Events 的关系：

MutationObserver 是用来代替已经废弃的 Mutation Events,后者被废弃的主要原因是：

1. 主流浏览器兼容性较差，比如 Webkit 内核不支持 DOMAttrModified 特性

![1640805221(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640805230046-893d29e3-e9d5-4364-a5fb-566ab9583471.png#clientId=u98001344-66f0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=216&id=ueea9c87f&margin=%5Bobject%20Object%5D&name=1640805221%281%29.png&originHeight=432&originWidth=857&originalType=binary∶=1&rotation=0&showTitle=false&size=137865&status=done&style=none&taskId=ua6c26262-00c9-48a8-91af-9aca8532bc6&title=&width=428.5)

2. MutationEvents 每触发一次 dom 变动，就会执行一次 callback;而 MutationObserver 会把所有的 dom 变动存储在一个列表中，结束后统一执行一次回调

```javascript
function add() {
  const ele = document.getElementById("list");
  for (let i = 1; i < 10; i++) {
    let newLi = document.createElement("li");
    newLi.innerHTML = "item-" + i;
    ele.appendChild(newLi);
  }
}
function callbackEvent(content) {
  console.log("执行mutationEvents回调函数", content);
}
function callbackObserver(mutationList) {
  console.log("执行mutationObserver回调函数", mutationList);
}

// mutation events
// 每发生一次dom更改,就执行一次回调，总共执行9次回调
document
  .getElementById("list")
  .addEventListener("DOMNodeInserted", function (e) {
    callbackEvent(e.target.innerHTML);
  });
// mutation observer
// 将变动记录在数组中，总共只执行一次回调
const observer = new MutationObserver(callbackObserver);
observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true,
});
```

## 常用 api:

### 构造函数 MutationObserver(callback):

1.  一旦监听到本次 DOM 全部变动完毕，执行 callback 回调
1.  返回新的 MutationObserver 对象
1.  callback(MutationRecord[],observer)：

![mutationRecord.png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640808659308-b597dc32-85b3-42f3-817d-561a3264f4af.png#clientId=u98001344-66f0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=671&id=ub466da7d&margin=%5Bobject%20Object%5D&name=mutationRecord.png&originHeight=1342&originWidth=2508&originalType=binary∶=1&rotation=0&showTitle=false&size=337937&status=done&style=none&taskId=u0d88b5ed-e5e8-466b-928b-5939ff02c7d&title=&width=1254)

### observe(rootNode,config)：

1. 在 DOM 更改匹配给定的 config 选项时，通过其回调函数开始接收通知，执行操作
1. childList，attributes 或者 characterData 三个属性之中，至少有一个必须为 true，避免抛出 TypeError 异常

![config.png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640811467845-58d18e27-19f0-417d-9796-d1813cfd531d.png#clientId=u98001344-66f0-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=331&id=u8884347e&margin=%5Bobject%20Object%5D&name=config.png&originHeight=662&originWidth=2700&originalType=binary∶=1&rotation=0&showTitle=false&size=190793&status=done&style=none&taskId=u312856a1-5e0b-4a35-afff-e82d570bf1b&title=&width=1350)

### disconnect()：

1. 停止对 DOM 变化的监听，直到重新调用 observe()

### takeRecords()

1. 返回观察者已经检测到但是回调函数还没有处理的列表
1. 使用场景：在停止监听之前立即获取所有未处理的更改记录，以便在停止监听的时候可以处理未处理的更改
1. 一般和 disconenct 方法一起使用

## 实际应用：

### 全局替换指定内容：

```html
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div id="root">
      <script src="./replace.js"></script>
      <div data-role="editor" contenteditable="true">dtle-editor</div>
      <button onclick="restore()">恢复</button>
      <button onclick="ignore()">暂停监听</button>
      <h1>dtle</h1>
      <h2>dtle-subtitle</h2>
      <h3>
        dtle dt-le
        <span>不存在指定字符串dt le</span>
      </h3>
      没有子节点标签包裹的dtle字符串
      <select disabled>
        <option value="dtle-1">dtle-1</option>
        <option value="dtle-2">dtle-2</option>
      </select>
    </div>
  </body>
</html>
```

```javascript
//创建一个MutationObserver实例
const observer = new MutationObserver(callback);
const config = {
  childList: true,
  subtree: true,
  characterData: true,
  characterDataOldValue: true,
};
//指定监控的节点、监控的事件
observer.observe(document.querySelector("#root"), config);
let source = "dtle",
  target = "dts",
  reg = /dtle/gi;
//监听到本次dom变动结束后的回调函数
function callback(mutationList) {
  mutationList.forEach((mutation) => {
    const mutationTarget = mutation.target;
    //根据mutationType做不同的处理
    switch (mutation.type) {
      case "childList":
        if (!!mutation.addedNodes && !!mutation.addedNodes.length) {
          mutation.addedNodes.forEach((node) => {
            if (node.nodeName === "#text" && node.nodeValue.includes(source)) {
              //因为subtree为true,会监听目标节点的子孙节点，所以可以直接用text节点去判断和替换
              node.nodeValue = node.nodeValue.replace(reg, target);
            }
          });
        }
        break;
      case "characterData":
        if (
          !!mutationTarget.nodeValue &&
          !!reg.test(mutationTarget.nodeValue)
        ) {
          mutationTarget.nodeValue = mutationTarget.nodeValue.replace(
            reg,
            target
          );
        }
        break;
    }
  });
}
function ignore() {
  //收集还没处理的mutationRecord并作处理
  const records = observer.takeRecords();
  if (records.length) {
    callback(records);
  }
  //停止监听
  observer.disconnect();
}
function restore() {
  // 重新开始监听
  observer.observe(document.querySelector("#root"), config);
}
```

### 前端水印：

```javascript
function generateMaterMark({
  container = document.body,
  width = "300px",
  height = "200px",
  font = "20px Microsoft Yahei",
  fillStyle = "rgba(184, 184, 184, 0.6)",
  content = "水印",
  rotate = "45",
  zIndex = 10000,
  opacity = 0.3,
}) {
  const svgStr = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${width}">
       <text x="50%" y="50%" dy="12px"
         text-anchor="middle"
         stroke="#000000"
         stroke-width="1"
         stroke-opacity="${opacity}"
         fill="none"
         transform="rotate(-45, 120 120)"
         style="font-size: ${font};">
         ${content}
       </text>
     </svg>`;
  const base64Url = `data:image/svg+xml;base64,${window.btoa(
    unescape(encodeURIComponent(svgStr))
  )}`;
  const __wm = document.querySelector(".__wm");

  const watermarkDiv = __wm || document.createElement("div");

  const styleStr = `
       position:fixed;
       top:0;
       left:0;
       bottom:0;
       right:0;
       width:100%;
       height:100%;
       z-index:${zIndex};
       pointer-events:none;
       background-repeat:repeat;
       background-image:url('${base64Url}')`;

  watermarkDiv.setAttribute("style", styleStr);
  watermarkDiv.classList.add("__wm");

  if (!__wm) {
    container.style.position = "relative";
    container.insertBefore(watermarkDiv, container.firstChild);
  }
}

// 调用生成水印方法
generateMaterMark({
  content: "水印_test",
});
const config = {
  attributes: true,
  childList: true,
  subtree: true,
  attributeOldValue: true,
};
const DEFAULT_STYLE_STRING = `
position:fixed;top:0;
left:0;
bottom:0;
right:0;
width:100%;
height:100%;
z-index:10000;
pointer-events:none;
background-repeat:repeat;
background-image:url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDBweCIgaGVpZ2h0PSIzMDBweCI+CiAgICAgICA8dGV4dCB4PSI1MCUiIHk9IjUwJSIgZHk9IjEycHgiCiAgICAgICAgIHRleHQtYW5jaG9yPSJtaWRkbGUiCiAgICAgICAgIHN0cm9rZT0iIzAwMDAwMCIKICAgICAgICAgc3Ryb2tlLXdpZHRoPSIxIgogICAgICAgICBzdHJva2Utb3BhY2l0eT0iMC4zIgogICAgICAgICBmaWxsPSJub25lIgogICAgICAgICB0cmFuc2Zvcm09InJvdGF0ZSgtNDUsIDEyMCAxMjApIgogICAgICAgICBzdHlsZT0iZm9udC1zaXplOiAyMHB4IE1pY3Jvc29mdCBZYWhlaTsiPgogICAgICAgICDmsLTljbAxMjMKICAgICAgIDwvdGV4dD4KICAgICA8L3N2Zz4=')`;
const targetNode = document.body;
const callback = function (mutationsList, observer) {
  const watermarkClass = "__wm";
  let watermarkDiv = document.querySelector(".__wm");

  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
      mutation.removedNodes.forEach(function (item) {
        //如果检测到水印被移除，则将被移除的节点重新添加到目标节点上
        if (item.className === watermarkClass) {
          document.body.appendChild(item);
        }
      });
    } else if (
      mutation.type === "attributes" &&
      mutation.attributeName === "style" &&
      mutation.oldValue !== watermarkDiv.getAttribute("style")
    ) {
      //如果检测到用户通过开发者工具的display或者其他方式隐藏了水印，则添加默认的水印样式
      watermarkDiv.setAttribute("style", DEFAULT_STYLE_STRING);
    }
  }
};
const observer = new MutationObserver(callback);
observer.observe(targetNode, config);
```

其他应用：
富文本编辑器的过滤关键字，阻止编辑，vue 以前的的$nextTick 中也有用到 MutationObserver

##
