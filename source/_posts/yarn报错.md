---
title: yarn报错
date: 2023-02-16 22:25:39
tags: [yarn]
categories: 工作
---

yarn install 报错
报错信息：
> yarn : 无法加载文件 C:\Users\yueyu\AppData\Roaming\npm\yarn.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.mi
crosoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
所在位置 行:1 字符: 1


解决方法：
1. 以管理员身份打开powershell,
2. 输入`set-ExecutionPolicy RemoteSigned` 选择Y 