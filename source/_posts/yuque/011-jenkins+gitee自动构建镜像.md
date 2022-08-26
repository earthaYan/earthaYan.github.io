---
title: 011-jenkins+gitee自动构建镜像
urlname: kzxamo
date: '2022-03-22 22:12:36 +0800'
tags: []
categories: []
---

## 使用 docker 安装 Jenkins

### 前置条件：

1. 机器有 256M 的 RAM，10 GB 的磁盘空间
   1. `df -hl`查看可用磁盘空间
   1. `grep MemTotal /proc/meminfo`查看内存
2. 需要安装 Java8(JRE 和 JDK)
   1. `yum install java-11-openjdk-devel` 安装 JDK
   1. 配置环境变量 JAVA_HOME

```bash
vi /etc/profile.d/java.sh
#  java.sh修改内容
JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk"
#	使修改生效
source /etc/profile.d/java.sh
echo $JAVA_HOME
```

3. 机器上安装了正确版本的 docker

### 步骤：

1. 创建 network` docker network create jenkins`
1. 为了在 jenkins 节点内部执行 docker 命令，需要下载并运行 docker:dind

```bash
docker run --name jenkins-docker --rm --detach \
  --privileged --network jenkins --network-alias jenkins_network \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind --storage-driver overlay2
```

3. 定制镜像

```dockerfile
FROM jenkins/jenkins:2.332.1-jdk11
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.25.3 docker-workflow:1.28"
```

4. 构建 `docker image build -t myjenkins-blueocean:2.332.1-1 .`
5. 运行 jenkins 容器

```dockerfile
docker run --name jenkins-blueocean --rm --detach \
  --network jenkins --env DOCKER_HOST=tcp://jenkins_network:2376 \
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.332.1-1
```

## 向导设置

![1647970718(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1647970722976-f84f5ee6-1e6d-4fc8-97e8-d64dd66d1790.png#clientId=u4b6560ae-43bc-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=566&id=u1e74e495&margin=%5Bobject%20Object%5D&name=1647970718%281%29.png&originHeight=849&originWidth=1591&originalType=binary∶=1&rotation=0&showTitle=true&size=151891&status=done&style=none&taskId=u1e331b32-804b-46de-a632-583f87e01a2&title=%E8%A7%A3%E9%94%81%E9%A1%B5%E9%9D%A2&width=1060.6666666666667 "解锁页面")
![1647970929(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1647970932921-a607fffc-3298-416f-95cb-8ce6115dbf1e.png#clientId=u4b6560ae-43bc-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=538&id=u8c4019ad&margin=%5Bobject%20Object%5D&name=1647970929%281%29.png&originHeight=807&originWidth=1533&originalType=binary∶=1&rotation=0&showTitle=true&size=47102&status=done&style=none&taskId=u277777b2-ffb6-4573-9812-e802cb03fe5&title=%E5%88%9B%E5%BB%BA%E7%AC%AC%E4%B8%80%E4%B8%AA%E7%AE%A1%E7%90%86%E5%91%98%E7%94%A8%E6%88%B7&width=1022 "创建第一个管理员用户")
![1647971051(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1647971059075-f1fb2f67-a1c9-475d-a4ee-671b042346dd.png#clientId=u4b6560ae-43bc-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=608&id=u216c40ac&margin=%5Bobject%20Object%5D&name=1647971051%281%29.png&originHeight=912&originWidth=1886&originalType=binary∶=1&rotation=0&showTitle=true&size=127563&status=done&style=none&taskId=u9367062c-54f8-4bcb-8e28-dbc31463597&title=%E6%88%90%E5%8A%9F%E6%88%AA%E5%9B%BE&width=1257.3333333333333 "成功截图")

## 配置 SSH

1. 安装 publish over ssh
1.
