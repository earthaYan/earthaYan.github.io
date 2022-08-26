---
title: 006-Dockerfile2
urlname: gh96x0
date: '2021-12-28 11:07:37 +0800'
tags: []
categories: []
---

## 基础镜像选择原则-FROM：

FROM BASE_IMAGE

1. 优先选择官方镜像
1. 如果没有官方镜像，则选择有 docker file 的开源镜像
1. 尽量选择固定版本的镜像，而不是默认 latest
1. 相同 tag 尽量选择体积小的基础镜像

![1640661416(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640661420821-11213505-b2d6-45ca-807d-b126e6342352.png#clientId=u3e4ace8d-8e88-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=452&id=u280a25df&margin=%5Bobject%20Object%5D&name=1640661416%281%29.png&originHeight=904&originWidth=1268&originalType=binary∶=1&rotation=0&showTitle=false&size=66258&status=done&style=none&taskId=ufa417bf7-3355-4799-a9b6-67fa9e0ab79&title=&width=634)
采用不同 nginx 版本做 base_image 结果
![1640662274(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640662291806-e55a1a14-aef9-4d32-a180-e6676c207e65.png#clientId=uc99858bd-37ce-4&crop=0&crop=0&crop=1&crop=1&from=drop&id=u81ccb6ed&margin=%5Bobject%20Object%5D&name=1640662274%281%29.png&originHeight=140&originWidth=864&originalType=binary∶=1&rotation=0&showTitle=false&size=14674&status=done&style=none&taskId=u8e2553a8-7685-475f-bd9a-d58089cf6cb&title=)

---

## 执行指令 RUN：

RUN xxx
每执行一个 RUN 命令，都会产生一层 image layer, 导致镜像的臃肿
常用方法：只有一个 run 命令，用**_&&_**连接，换行用\*\*\*\*表示

```dockerfile
FROM ubuntu:21.04
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/ipinfo/cli/releases/download/ipinfo-2.0.1/ipinfo_2.0.1_linux_amd64.tar.gz && \
    tar zxf ipinfo_2.0.1_linux_amd64.tar.gz && \
    mv ipinfo_2.0.1_linux_amd64 /usr/bin/ipinfo && \
    rm -rf ipinfo_2.0.1_linux_amd64.tar.gz
```

对比：
代码：`docker image build -f Dockerfile.latest -t bad:1.0 .`
![1640670496(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640670506193-1d653dee-a88f-44f6-ab2e-9a887885c5b4.png#clientId=u096228e7-e798-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=82&id=u3a7b8d78&margin=%5Bobject%20Object%5D&name=1640670496%281%29.png&originHeight=163&originWidth=827&originalType=binary∶=1&rotation=0&showTitle=false&size=16492&status=done&style=none&taskId=u312a892c-7f7d-4cf1-a814-c4b354abbfb&title=&width=413.5)

- [x] 通过执行多个 run 的 dockerfile 构建的镜像

![1640670613(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640670616894-f1f3f83f-6b01-498b-9d37-7fc724556c35.png#clientId=u096228e7-e798-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=104&id=u12ebe7a3&margin=%5Bobject%20Object%5D&name=1640670613%281%29.png&originHeight=208&originWidth=1091&originalType=binary∶=1&rotation=0&showTitle=false&size=29485&status=done&style=none&taskId=ubf765b9e-9364-4114-b2d7-39e6faf5cc5&title=&width=545.5)

- [x] 通过执行单个 run 的 dockerfile 构建的镜像

![1640670628(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640670631921-bb77c17a-755e-4212-8de5-44d4046b6bf1.png#clientId=u096228e7-e798-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=66&id=u1a34d95f&margin=%5Bobject%20Object%5D&name=1640670628%281%29.png&originHeight=131&originWidth=1152&originalType=binary∶=1&rotation=0&showTitle=false&size=15866&status=done&style=none&taskId=u9c659f71-a384-4747-ac94-bd01266596b&title=&width=576)

---

## 文件的复制和目录操作：

### 文件的复制：

COPY:
`FROM python:3.9.5-alpine3.13 `
`COPY hello.py /app/hello.py`
ADD:
`**FROM** python:3.9.5-alpine3.13 `
`**ADD** hello.tar.gz /app/`

#### 两者关系：

1. 两者都是把本地文件复制到 docker 镜像中，如镜像中目录不存在则自动创建该目录
1. 如果复制的是一个 gzip 等压缩文件时，ADD 会帮助我们自动去解压缩文件，copy 不会
1. 如果需要解压缩情况，使用 ADD，其余情况优先使用 COPY

### 目录操作：

WORKDIR:
作用：进行目录切换，类似于 cd 命令，
区别：目录不存在的时候 WORKDIR 会自动创建目标目录，cd 不会
代码：`WORKDIR 目标目录`
应用：从本地复制一个复杂的目录到镜像中，可以通过 WORKDIR 切换到目标子目录

---

## 构建参数和环境变量：

ARG&&ENV 设置变量
ENV:

```dockerfile
FROM ubuntu:21.04
ENV VERSION=2.0.1
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/ipinfo/cli/releases/download/ipinfo-${VERSION}/ipinfo_${VERSION}_linux_amd64.tar.gz && \
    tar zxf ipinfo_${VERSION}_linux_amd64.tar.gz && \
    mv ipinfo_${VERSION}_linux_amd64 /usr/bin/ipinfo && \
    rm -rf ipinfo_${VERSION}_linux_amd64.tar.gz
```

ARG:

```dockerfile
FROM ubuntu:21.04
ARG VERSION=2.0.1
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/ipinfo/cli/releases/download/ipinfo-${VERSION}/ipinfo_${VERSION}_linux_amd64.tar.gz && \
    tar zxf ipinfo_${VERSION}_linux_amd64.tar.gz && \
    mv ipinfo_${VERSION}_linux_amd64 /usr/bin/ipinfo && \
    rm -rf ipinfo_${VERSION}_linux_amd64.tar.gz
```

![1640673742(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640673752556-7810f718-cbf6-4181-88e3-497f1f0414d6.png#clientId=ucd2b1d4b-4a86-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=168&id=u5aa2ff8f&margin=%5Bobject%20Object%5D&name=1640673742%281%29.png&originHeight=336&originWidth=799&originalType=binary∶=1&rotation=0&showTitle=true&size=27134&status=done&style=none&taskId=u37b1e990-68b7-4eb1-9528-e7d35d284f6&title=%E6%89%A7%E8%A1%8C%E7%BB%93%E6%9E%9C&width=399.5 "执行结果")

### 区别：

arg:构建时变量
![1640677012(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640677020192-55ff1abb-c3ec-486e-b859-511b1c2bc8c3.png#clientId=ucd2b1d4b-4a86-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=372&id=u849efa38&margin=%5Bobject%20Object%5D&name=1640677012%281%29.png&originHeight=744&originWidth=1935&originalType=binary∶=1&rotation=0&showTitle=false&size=95290&status=done&style=none&taskId=u6e189ec9-dcba-4c42-9ebe-a7fdf64b90e&title=&width=967.5)

1. 通过 arg 创建的变量只能存在于镜像构建中，创建运行容器的时候无法使用该变量
1. 通过 env 创建的变量可以存在于镜像构建中，并永久保存在镜像中，创建运行容器的时候可以使用该变量
1. 构建镜像的时候可以通过--build-arg 选项修改 arg 变量，覆盖镜像文件中定义的 arg 变量

```bash
docker image build -f .\Dockerfile-arg -t ipinfo-arg-2.0.0 --build-arg VERSION=2.0.0 .
```

![docker_environment_build_args.png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640672713556-cd0d8bd1-753e-4cec-9280-55844749a799.png#clientId=u86165680-5e8d-4&crop=0&crop=0&crop=1&crop=1&from=ui&height=476&id=ua6bc57d8&margin=%5Bobject%20Object%5D&name=docker_environment_build_args.png&originHeight=476&originWidth=533&originalType=binary∶=1&rotation=0&showTitle=true&size=27420&status=done&style=none&taskId=ud3d6189c-2f01-4b1b-8b6d-e5ccf2df474&title=ENV%E5%92%8Carg%E7%9A%84%E5%8C%BA%E5%88%AB&width=533 "ENV和arg的区别")

---

## 容器启动命令：

CMD&ENTRYPOINT

### CMD 作用：

- 容器启动时默认会执行的命令
- 如果启动运行容器的时候指定了其他命令，则 CMD 的命令不会被执行
- 如果定义了多个 CMD，则只有最后一个会被执行
- CMD 可以被继承

### ENTRYPOINT 作用：

- 容器启动的时候会执行的命令

### 二者区别：

1. 如果启动容器的时候加了命令，CMD 会被覆盖掉直接执行外部命令，ENTRYPOINT 会先执行内部命令再执行外部命令
1. 一般是 CMD 做参数，ENTRYPOINT 做命令

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
CMD ["name mox"]
```

```bash
//使用
docker run --rm -it mix //name mox
docker run --rm -it mix newword //newword
```

### 写法：

#### shell 写法：`**ENTRYPOINT** echo "hello docker"`

#### exec 写法：`**ENTRYPOINT** ["echo", "hello docker"]`

```dockerfile
//exec中有变量的时候用shell解决
FROM ubuntu:21.04
ENV NAME=docker
CMD ["sh", "-c", "echo hello $NAME"]
```

---

## 常用操作：

`docker system prune -a`:清理所有非运行状态的容器，镜像，build cache
`docker image prune -a`:删除没有正在使用的镜像
`docker run --rm -it image_name`:退出容器后立刻删除容器

---
