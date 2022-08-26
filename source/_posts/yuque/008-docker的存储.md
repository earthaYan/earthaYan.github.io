---
title: 008-docker的存储
urlname: rvncs2
date: '2021-12-28 22:44:04 +0800'
tags: [docker]
categories: [docker]
---

## 背景：

- 在运行的容器里创建的文件，被保存在一个可写的容器层
- 若容器被删，则数据也不存在
- 这个可写的容器层和特定的容器绑定，数据无法和其他容器共享

## 方法：

- Data Volume
  - 由**docke**r 管理，/var/lib/docker/volumes
  - 推荐使用
- Bind Mount
  - 由**用户指定**存储的数据具体 MOUNT 在系统什么位置

![types-of-mounts-volume.png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640704598232-50c82759-daa6-490f-9dc0-b62bdef56e69.png#clientId=u8147d5af-ec22-4&crop=0&crop=0&crop=1&crop=1&from=ui&id=uffce69d9&margin=%5Bobject%20Object%5D&name=types-of-mounts-volume.png&originHeight=255&originWidth=502&originalType=binary∶=1&rotation=0&showTitle=false&size=23458&status=done&style=none&taskId=ub5895628-1e71-439b-93c6-5f57ec6647b&title=)

---

## Data Volume:

docker run -it -v /宿主机目录:/容器目录 镜像名 /bin/bash
![1643071710(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1643071717294-76f0e6c1-de40-47b2-90fe-3021ec3b760e.png#clientId=u56023851-d56d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=314&id=ubd6f871d&margin=%5Bobject%20Object%5D&name=1643071710%281%29.png&originHeight=471&originWidth=1142&originalType=binary∶=1&rotation=0&showTitle=false&size=54555&status=done&style=none&taskId=u82d48bb9-0b97-45cb-b2e5-716d64cf2ab&title=&width=761.3333333333334)

### 常用命令：

- docker volume ls
- docker volume prune
- docker volume inspect

### data vloume 使用方法：

1. Dockerfile 中的 volume 选项
   1. 如果创建容器的时候没有指定-v 参数，docker 会自动创建一个 volume，名字随机，存储在 Dockerfile 定义的 volume
2. docker run -v 参数
   1. 手动的指定需要创建 Volume 的名字，以及对应于容器内的路径。
   1. 这个路径是可以任意的，不必需要在 Dockerfile 里通过 VOLUME 定义

## Bind Mount:

可以在本地指定任意路径

## 机器间的数据共享：

![](https://cdn.nlark.com/yuque/0/2022/png/115484/1643254141889-ebad73d2-96cc-463f-bb28-21cb78160c1c.png#clientId=ua81978af-9532-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u2c9c68d2&margin=%5Bobject%20Object%5D&originHeight=602&originWidth=1284&originalType=url∶=1&rotation=0&showTitle=false&status=done&style=none&taskId=u78941e08-c225-468a-b066-36eeeb03c58&title=)
【注意】Docker 的 volume 支持多种 driver。默认创建的 volume driver 都是 local
