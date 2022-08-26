---
title: 04-进程间通信-ipc
urlname: xy40g8
date: '2022-07-05 12:49:42 +0800'
tags: [electron]
categories: [electron]
---

IPC 是执行许多常规任务的唯一途径，如从 ui 或者调用 native API 或者从本地菜单触发 web 内容更改

### electron 进程通信实现原理：

进程通过 ipcMain 和 ipcRender 模块中开发者定义的"channal"传递信息进行通信
原则：使用预加载脚本在渲染器进程导入 Node.js 和 Electron 模块

## renderer->main:

### 单向：

#### 发送消息 ipcRenderer.send，接收消息 ipcMain.on,从 web 内容调用主进程 API

```typescript
//main.ts 主进程设置事件监听
app.whenReady().then(() => {
  // 使用ipcMain.on监听事件window.并设置响应的事件处理程序
  ipcMain.on("set-title", handleSetTitle);
  createWindow();
});
// preload.js   看上去是一个中介的角色?
contextBridge.exposeInMainWorld("electronAPI", {
  // 暴露接口：使用ipcRenderer发送消息
  setTitle: (title: string) => ipcRenderer.send("set-title", title),
});
//renderer.ts
window.electronAPI.setTitle(title);
```

### 双向：

定义：从渲染器进程调用主进程模块后等待结果
常用场景：从渲染器进程中调用主进程模块，等待结果。
实现：ipcRender.invoke +ipcMain.handle

```typescript
//main.ts
async function handleFileOpen() {
  const { canceled, filePaths } = await dialog.showOpenDialog({});
  if (canceled) {
    return;
  } else {
    return filePaths[0];
  }
}
app.whenReady().then(() => {
  // 使用ipcMain.handle设置事件处理器
  ipcMain.handle("dialog:openFile", handleFileOpen);
  createWindow();
});
//preload.ts
contextBridge.exposeInMainWorld("electronAPI", {
  // // renderer->main双向发送
  openFile: () => ipcRenderer.invoke("dialog:openFile"),
});
//renderer.ts
const fileButton = document.getElementById("openFile");
const filePathElement = document.getElementById("filePath");
fileButton.addEventListener("click", async () => {
  const filePath = await window.electronAPI.openFile();
  filePathElement.innerText = filePath;
});
```

## main->renderer:

前提：需要指定哪一个渲染器进程在接收消息
实现：通过包含 send 方法的 WebContent 实例实现

```typescript
//main.ts
const menu = Menu.buildFromTemplate([
  {
    label: app.name,
    submenu: [
      {
        click: () => mainWindow.webContents.send("update-counter", 1),
        label: "Increment",
      },
      {
        click: () => mainWindow.webContents.send("update-counter", -1),
        label: "Decrement",
      },
    ],
  },
]);
Menu.setApplicationMenu(menu);
//preload.ts
contextBridge.exposeInMainWorld("electronAPI", {
  onUpdateCounter: () => (callback: any) =>
    ipcRenderer.on("update-counter", callback),
});
//renderer.ts
const counter = document.getElementById("counter");
window.electronAPI.onUpdateCounter((_event: any, value: string) => {
  const oldValue = Number(counter.innerText);
  const newValue = oldValue + Number(value);
  counter.innerText = newValue.toString();
});
```

## Renderer to renderer:

不能直接实现，需要使用主进程作为中间程序
