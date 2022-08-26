---
title: 010-docker-compose
urlname: gi7n7u
date: '2022-01-25 07:03:48 +0800'
tags: []
categories: []
---

## 安装：

- pip install docker-compose
- 从 github 下载安装

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
```

## yaml 文件的结构

```bash
version: "3.8"

services: # 容器
  servicename: # 服务名字，这个名字也是内部 bridge网络可以使用的 DNS name
    image: # 镜像的名字
    command: # 可选，如果设置，则会覆盖默认镜像里的 CMD命令
    environment: # 可选，相当于 docker run里的 --env
    volumes: # 可选，相当于docker run里的 -v
    networks: # 可选，相当于 docker run里的 --network
    ports: # 可选，相当于 docker run里的 -p
  servicename2:

volumes: # 可选，相当于 docker volume create
```

改写：
原脚本：

```bash
# prepare image
docker image pull redis
docker image build -t flask-demo .

# create network
docker network create -d bridge demo-network

# create container
docker container run -d --name redis-server --network demo-network redis
docker container run -d --network demo-network --name flask-demo --env REDIS_HOST=redis-server -p 5000:5000 flask-demo
```

改写后：

```bash
services:
  flask-demo:
  	build: ./flask/Dockerfile
    build：
    	context: ./flask
      dockerfile:Dockerfile_name
  //已经在本地的镜像
    image: flask-demo:latest
    environment:
      - REDIS_HOST=redis-server
    networks:
      - demo-network
    ports:
      - 8080:5000
    volumes:
    	- ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./var/log/nginx:/var/log/nginx
    depends-on:
    	xxx:依赖于前面的service

  redis-server:
    image: redis:latest
    networks:
     - demo-network

networks:
  demo-network:
```

## docker-compose 命令行：

- docker-compose up -d
- docker-compose ls
- docker-compose stop
- docker-compose rm

## docker-compose 镜像拉取和删除：

- 如果是 dockerhub 的，会直接拉取
- 如果需要本地构建，添加 build 选项，设置为 Dockerfile 所在的文件夹

docker-compose 更新：

- docker-compose build:
  - docker-compose 重启
  - docker-compose build 手动更新镜像
- docker-compose up -d --build 镜像更新的情况下
- docker-compose up -d yml 配置文件更新的情况下
- docker-compose restart 重启已经存在的容器，如 services 的某个容器使用了 volume 的情况下
- docker-compose up -d --scale serviceName=3 :一次性创建多个服务
- docker-compose --env-file config:查看配置预览

## 服务依赖:

通过 depends_on 关键字实现

## 健康检查：

HEALTHCHECK
