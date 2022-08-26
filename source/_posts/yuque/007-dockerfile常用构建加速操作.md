---
title: 007-dockerfile常用构建加速操作
urlname: vgfaye
date: '2021-12-28 17:22:58 +0800'
tags: []
categories: []
---

## 缓存：

当某一层发生变化后，该层及其后面的 layer 层都不会使用 cache
改进方法：将容易发生变化的层放在后面

## docker ignore：

Docker 是 client-server 架构，理论上 Client 和 Server 可以不在一台机器上。在构建 docker 镜像的时候，需要把所需要的文件由 CLI（client）发给 Server，这些文件实际上就是 build context
新建.dockerignore 文件，用法同.gitignore

## 多阶段构建：

```dockerfile
FROM gcc:9.4 AS builder

COPY hello.c /src/hello.c

WORKDIR /src

RUN gcc --static -o hello hello.c
//+++++++以上作为输出++++++++++++++++++++++


FROM alpine:3.13.5

COPY --from=builder /src/hello /src/hello

ENTRYPOINT [ "/src/hello" ]

CMD []
```

## 尽量使用非 root 用户：

原因：
docker 的 root 权限能够使得宿主机中的非 root 用户越权操作
解决方法：使用非 root 用户

1. 通过 groupadd 和 useradd 创建一个 flask 的组和用户
1. 通过 USER 指定后面的命令要以 flask 这个用户的身份运行

```dockerfile
FROM python:3.9.5-slim

RUN pip install flask && \
    groupadd -r flask && useradd -r -g flask flask && \
    mkdir /src && \
    chown -R flask:flask /src

USER flask

COPY app.py /src/app.py

WORKDIR /src
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]
```
