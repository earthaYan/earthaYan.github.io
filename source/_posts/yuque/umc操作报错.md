---
title: umc操作报错
urlname: pnx542
date: '2022-01-20 18:01:05 +0800'
tags: [工作]
categories: [工作]
---

# [ushard 创建实例-安装/启动 dble 报错： rpc error: code = Unknown desc = parse rule.xml error: unmarshal sharding.xml error: EOF](http://10.186.18.11/confluence/pages/viewpage.action?pageId=29696886)

原因：dble 跨版本了，元数据不兼容，一个组的第一个 dble 实例的版本（2/3）会决定元数据的格式
解决方法：保证同一组的所有 dble 版本都要和第一个安装的 dble 版本相对应。

# docker 服务莫名 fail：

journal -xe 得知以下报错

> 报错信息：
> docker.socket: Failed with result 'service-start-limit-hit'
> docker.service: Service RestartSec=100ms expired, scheduling restart.
> docker.service: Scheduled restart job, restart counter is at 3.
> Stopped Docker Application Container Engine.
> docker.service: Start request repeated too quickly.
> docker.service: Failed with result 'exit-code'.
> Failed to start Docker Application Container Engine.

原因：docker 启动参数有问题，把参数改成红框中的变量
![62bab51747c151d6df0ac17ae6266fc.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644379395888-c5d863f5-2318-4650-bdbe-906ba71310e7.png#clientId=u4de33745-897b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=425&id=u51036d36&margin=%5Bobject%20Object%5D&name=62bab51747c151d6df0ac17ae6266fc.png&originHeight=743&originWidth=1227&originalType=binary∶=1&rotation=0&showTitle=true&size=61314&status=done&style=none&taskId=ufb725310-8646-4ce8-b63c-fb6c776b5d0&title=%2Flib%2Fsystemd%2Fsystem%2Fdocker.service&width=701.1428571428571 "/lib/systemd/system/docker.service")
执行以下命令：

```bash
systemctl daemon-reload
service docker start
```

# 服务视图报错：

报错内容似乎是 no connection pinged and dail new connection failed ,忘记记录了
解决方法：
在实例视图重启 mysql-udb1 实例即可
