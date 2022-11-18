---
title: 13-go在vscode中的调试
date: 2022-11-18 11:55:04
tags: [golang, 后端, 实践]
categories: GoLang
---

1. 新建.vscode/launch.json
2. 文件-将文件夹添加到工作区

```json
// launch.json
{
  // 使用 IntelliSense 了解相关属性。
  // 悬停以查看现有属性的描述。
  // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch file",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/main.go"
    }
  ]
}
```
