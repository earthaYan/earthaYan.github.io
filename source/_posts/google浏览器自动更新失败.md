---
title: google浏览器自动更新失败
date: 2023-01-05 10:09:33
tags: [google,浏览器,缺陷修复]
categories: google浏览器
---

报错：
> 无法启动更新检查（错误代码为 4: 0x80070005 — system level）

解决方法：
快捷键 Win R 输入：services.msc，找到 “Google 更新服务 (gupdatem)”、“Google 更新服务 (gupdate)”服务，改为手动即可，再去更新Chrome。