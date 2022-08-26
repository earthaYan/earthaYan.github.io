---
title: 002-centos安装docker
urlname: svcf4g
date: '2021-12-09 11:13:20 +0800'
tags: []
categories: []
---

```bash
//从get.docker.com下载脚本并命名为get-docker.sh
curl -fsSL get.docker.com -o get-docker.sh
//执行脚本
sh get-docker.sh
//查看docker版本，验证是否安装
docker version

```

## ![1640616161(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640616177408-e46bffff-2ec1-471a-91bf-77329cd7cc01.png#clientId=u5f88119b-0472-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=141&id=u749c501f&margin=%5Bobject%20Object%5D&name=1640616161%281%29.png&originHeight=281&originWidth=1027&originalType=binary∶=1&rotation=0&showTitle=true&size=18313&status=done&style=none&taskId=u2b475b78-318d-4ded-b66d-e1193a07192&title=%E5%90%AF%E5%8A%A8docker%E6%9C%8D%E5%8A%A1%E5%89%8D&width=513.5 "启动docker服务前")

![1640616202(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640616211638-2ac18c25-280a-429f-9369-be853b57305c.png#clientId=u5f88119b-0472-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=324&id=uf1d269dd&margin=%5Bobject%20Object%5D&name=1640616202%281%29.png&originHeight=647&originWidth=932&originalType=binary∶=1&rotation=0&showTitle=true&size=36667&status=done&style=none&taskId=uaa6ceb72-c3d0-40d8-86fa-6de65e36d0d&title=%E5%90%AF%E5%8A%A8docker%E6%9C%8D%E5%8A%A1%E5%90%8E&width=466 "启动docker服务后")

## 常见报错：

- connect to the Docker daemon at unix:///var/run/docker.sock.Is the docker daemon running?
  - 启动 docker 服务：`systemctl start docker`
