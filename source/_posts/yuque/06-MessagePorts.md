---
title: 06-MessagePorts
urlname: bdpz9i
date: '2022-07-18 22:53:12 +0800'
tags: [electron]
categories: [electron]
---

[MessagePort](https://developer.mozilla.org/en-US/docs/Web/API/MessagePort)s 是一个 web 特性，它可以实现在不同的上下文中传递消息。类似不同 channal 上的的 window.postMessage

```typescript
const channel = new MessageChannel();
// 消息发送到port1将会被port2接收，反之亦然
const port1 = channel.port1;
const port2 = channel.port2;
// 允许在另一端还没有注册监听器的情况下就通过通道向其发送消息
// 消息将排队等待，直到一个监听器注册为止。
port2.postMessage({ answer: 12 });
// 这次我们通过 ipc 向主进程发送 port1 对象。 类似的，
// 我们也可以发送 MessagePorts 到其他 frames, 或发送到 Web Workers, 等.
ipcRenderer.postMessage("port", null, [port1]);
```

```typescript
// 在主进程中，我们接收这个端口对象
ipcMain.on("port", (event) => {
  // 当我们在主进程中接收到 MessagePort 对象, 它就成为了
  // MessagePortMain.
  const port = event.ports[0];
  port.on("message", (event) => {
    // 收到的数据是： { answer: 42 }
    const data = event.data;
  });

  // MessagePortMain 阻塞消息直到 .start() 方法被调用
  port.start();
});
```
