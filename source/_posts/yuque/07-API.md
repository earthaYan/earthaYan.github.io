---
title: 07-API
urlname: vqcmu7
date: '2022-07-19 01:00:41 +0800'
tags:  [electron]
categories: [electron]
---

## 主进程 Api：main.ts

Menu

- 作用：创建本地应用菜单和上下文菜单 ` const menu=new Menu()`
- 静态方法
  - `Menu.setApplicationMenu(menu:Menu|null)`
    - 设置窗口顶部菜单，null 是隐藏顶部菜单
  - `Menu.getApplicationMenu()`
    - 获取菜单配置，返回值为 Menu|null
  - `Menu.sendActionToFirstResponder(action:string)`
    - 将 action 发送到应用程序的第一个响应方
    - 主要用于模拟默认的 macOS 菜单行为
  - `Menu.buildFromTemplate(template:Array<MenuItemConstructorOptions|MenuItem>)`
    - 从模板创建菜单，返回值为 Menu
- 实例方法
  - `menu.popup([options:{windows:BrowserWindow,x:number,y:number,callback:Function}])`
    - 在当前窗口弹出此菜单作为上下文菜单
    - callback 在菜单关闭的适合调用
  - `menu.closePopup(window?:BrowserWindow);`
    - 关闭上下文菜单
  - `menu.append(menuItem:MenuItem)`
    - 将 menuItem 追加到菜单
  - `menu.getMenuItemById(id:string)`
    - 返回具有指定 id 项的 MenuItem 或者 null
  - `menu.insert(pos：number, menuItem:MenuItem)`
    - 将 menuItem 插入菜单的 pos 位置。
- 实例事件
  - menu-will-show：调用 menu.popup()事件时触发该事件
  - menu-will-close：手动关闭弹出，或使用 menu.closePopup()方法关闭弹出时，触发该事件

```javascript
//动态创建菜单
let menu = new Menu();
let menuFile = new MenuItem({ label: "文件", type: "normal" });
menu.append(menuFile);
Menu.setApplicationMenu(menu);
//模板生成
const menuTemplate: (
  | Electron.MenuItemConstructorOptions
  | Electron.MenuItem
)[] = [
  {
    label: "文件",
    submenu: [
      {
        label: "新建",
      },
      {
        label: "新建窗口",
      },
      {
        label: "打开",
      },
      {
        label: "保存",
      },
      {
        label: "另存为",
      },
      {
        label: "分隔",
      },
      // 分隔线
      {
        label: "退出",
        role: process.platform === "darwin" ? "close" : "quit",
      },
    ],
  },
];
const menu = Menu.buildFromTemplate(menuTemplate);
//设置自定义菜单栏
Menu.setApplicationMenu(menu);
```

dialog 作用：展示本地系统对话框，用来打开或保存文件以及告警等
简单用法：

```javascript
export function openExistFile(): void {
  // 第一个参数browserWindow允许该对话框将自身附加到父窗口, 作为父窗口的模态框
  dialog.showOpenDialog(win as BrowserWindow, {
    // 对话框窗口标题
    title: '选择文件',
    // 对话框默认展示路径
    defaultPath: '',
    // 确认按钮自定义名称,windows默认值是 打开
    buttonLabel: '选定离手',
    // 底部文件过滤,指定某种后缀，并不能过滤文件夹
    filters: [
      {
        name: '文本文档',
        extensions: ['txt'],
      },
      {
        name: 'oneNote',
        extensions: ['one', 'onetoc*'],
      },

      {
        name: '所有文件',
        extensions: ['*'],
      },
    ],
    properties: [
      'openFile',
      'multiSelections',
      'showHiddenFiles',
      // 当输入的文件路径不存在的时候，提示是否要创建该文件
      // 并不会真正创建,只是允许返回一些不存在地址交给应用程序去创建
      'promptToCreate',
      // 不要将正在打开的项目添加到最近使用中
      'dontAddToRecent',
    ],
  });
}
export function openSaveDialog(): void {
  dialog.showSaveDialog({
    title: '保存内容',
    defaultPath: '',
    buttonLabel: '备份至本地',
    filters: [],
    properties: ['dontAddToRecent', 'showHiddenFiles'],
  });
}
export function openMessageBox(): void {
  dialog.showMessageBox({
    // 主题消息
    message: '当前操作违法了',
    // 消息类型: "none", "info", "error", "question"
    type: 'error',
    // 按钮数组,置空或不设置会显示确定按钮
    buttons: [],
    // 对话框打开的时候，设置默认选中的按钮，值为在 buttons 数组中的索引.
    defaultId: 1,
    // 左上角标题
    title: '友情提示',
    // message下的提示内容
    detail: '详情',
    // 按钮是否以链接方式呈现
    noLink: false,
    // 规范跨平台的键盘访问键
    normalizeAccessKeys: true,
    checkboxLabel: '是否认可该结论',
    checkboxChecked: true,
  });
}
```

方法：

- `dialog.showOpenDialogSync([browserWindow, ]options)`
  - 打开本地文件选择框
  - 返回值为 string[]|undefined——取消则返回 undefined,否则返回用户选择的文件路径
- `dialog.showOpenDialog([browserWindow, ]options)`
  - 同上
  - 返回值为 Promise<canceled:boolean,filePaths:string[],bookmarks:string[]>
- `dialog.openSaveDialog([browserWindow, ]options)`
  - 打开本地文件保存对话框
  - 返回值同 dialog.showOpenDialog
  - mac 上建议使用异步版本，可以避免展开和折叠对话框时出现问题
- `dialog.openSaveDialogSync([browserWindow, ]options)`
  - 同上
  - 返回值同 dialog.showOpenDialogSync
- `dialog.showMessageBoxSync([browserWindow, ]options)`
  - 显示一个消息框，它将阻塞进程直到消息框关闭
  - 返回值为点击的按钮的索引-正整数
- `dialog.showMessageBox([browserWindow, ]options)`
  - 同上
  - 返回值为 Promise<response,checkboxChecked>
- `dialog.showErrorBox(title,content)`
  - 展示一个报错弹窗
- `dialog.showCertificateTrustDialog（[window,]options）`

  - 弹出一个用于展示消息与证书信息并向用户提供信任/导入证书的选项的模态对话框
    webContents[属于 BrowserWindow]作用：负责渲染和控制网页
    静态方法：

- webContents.getAllWebContents()
  - 所有 WebContents 实例的数组
  - 包含所有 Windows，webviews，opened devtools 和 devtools 扩展背景页的 web 内容
- webContents.getFocusedWebContents（）
  - 应用程序中的焦点所在 WebContents ，否则返回 null

实例方法：

-

ipcMain 作用：从主进程到渲染进程的异步通信
方法：

- ipcMain.on(channel, listener)
  - 监听 channel, 当新消息到达，将通过 listener(event, args...) 调用 listener
- ipcMain.once(channel, listener)
  - 添加一次性 listener 函数
- ipcMain.removeListener(channel, listener)
  - 为特定的 channel 从监听队列中删除特定的 listener 监听者.
- ipcMain.removeAllListeners([channel])
  - 移除所有指定 channel 的监听器； 若未指定 channel，则移除所有监听器
- ipcMain.handle(channel, listener)
  - 为一个 invokeable 的 IPC 添加一个 handler。 每当一个渲染进程调用 ipcRenderer.invoke(channel, ...args) 时这个处理器就会被调用
- ipcMain.handleOnce(channel, listener)
  - 处理单个 invokeable 可触发的 IPC 消息，然后移除侦听器

---

## 渲染进程：preload.ts

ipcRenderer 作用：渲染器进程（web 页面）->主进程的异步通信
方法：

- ipcRenderer.on(channel：string, listener:(event,...args)=>void) ：
  - 监听 channel, 当新消息到达，将通过 listener(event, args...) 调用 listener
- ipcRenderer.once(channel, listener)
  - 同上，这个 listener 只会在 channel 下一次收到消息的时候被调用，之后这个监听器会被移除
- ipcRenderer.removeListener(channel, listener)
  - 为特定的 channel 从监听队列中删除特定的 listener 监听者
- ipcRenderer.removeAllListeners(channel)
  - 移除所有的监听器，当指定 channel 时只移除与其相关的所有监听器
- ipcRenderer.send(channel, ...args)
  - 通过 channel 向主进程发送异步消息，可以发送任意参数
- ipcRenderer.invoke(channel, ...args):any-Resolves 主进程返回值
  - 通过 channel 向主进程发送消息，并异步等待结果
- ipcRenderer.sendSync(channel, ...args):any-由 ipcMain 处理程序发送过来的值。
  - 通过 channel 向主过程发送消息，并同步等待结果
- ipcRenderer.postMessage(channel, message, [transfer])
  - 发送消息到主进程，同时可以选择性发送零到多个 MessagePort 对象
- ipcRenderer.sendTo(webContentsId, channel, ...args)
  - 通过 channel 发送消息到带有 webContentsId 的窗口.
- ipcRenderer.sendToHost(channel, ...args)
  - 像 ipcRenderer.send，但是消息会被发送到 host 页面上的 <webview> ，而不是主进程
