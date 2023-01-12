---
title: docker安装
date: 2023-01-11 17:46:55
tags: [docker]
categories: Docker
---

## 基于centos7的设置Docker方式的安装 
官方文档：https://docs.docker.com/engine/install/centos/
### 设置仓库
1. 删除旧版本的docker engine
```bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```
2.  安装提供`yum-config-manager`工具的yum-utils包
```bash
yum install -y yum-utils
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```
### 安装docker 引擎
```bash
yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin #安装最新版
#安装指定版本
yum list docker-ce --showduplicates | sort -r
yum install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-compose-plugin 
```
### 启动docker
```bash
systemctl start docker
# 验证
docker run hello-world
```
### 创建docker 组和用户(非必须)
```bash
groupadd docker # 创建docker用户组
usermod -aG docker $USER #将用户添加到组内
```
退出登录后重新登录,组和用户才会生效，此时即使是非root用户也不需要使用sudo
####  解决报错
> WARNING: Error loading config file: /home/user/.docker/config.json - stat /home/user/.docker/config.json: permission denied
解决方法
```bash
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
```
### 设置为开机自启动
```bash
systemctl enable docker.service
systemctl enable containerd.service
# 停止开机自启动
systemctl disable docker.service
systemctl disable containerd.service
```


## 创建一个mysql容器
`docker run --name test_sql -e MYSQL_ROOT_PASSWORD=123 -d mysql:latest`

## 其他操作
```bash
docker exec -it test_sql bash
# 查看日志
docker logs test_sql 
```