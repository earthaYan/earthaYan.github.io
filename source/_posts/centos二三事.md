---
title: centos二三事
date: 2022-10-20 13:24:13
tags: [虚拟机, CentOS8]
categories: 虚拟机
---

## centos7 安装 mariadb

1.  配置 MariaDB Yum 源

```bash
#/etc/yum.repos.d/mariadb.repo
# MariaDB 10.5 CentOS repository list - created 2020-10-23 01:54 UTC
# http://downloads.mariadb.org/mariadb/repositories/
[mariadb]
name = MariaDB
baseurl = http://mirrors.aliyun.com/mariadb/mariadb-10.7.6/yum/centos/7/x86_64/
module_hotfixes=1
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=0
```

2.  安装 MariaDB 和 MariaDB 客户端
    `yum -y install MariaDB-server MariaDB-client`
3.  启动 MariaDB，并设置开机启动
    `systemctl enable mariadb`
    `systemctl start mariadb`
4.  设置 root 初始密码
    `mysqladmin -u${MARIADB_ADMIN_USERNAME} password ${MARIADB_ADMIN_PASSWORD}`
5.  验证
    `mysql -h127.0.0.1 -uroot -p'iam59!z$'`

## centos7 安装 redis

由于 yum 不支持 redis，所以通过源码方式安装

1. 获取最新稳定版本的 redis 并解压
   `wget https://download.redis.io/redis-stable.tar.gz`
   `tar -zxvf redis-4.0.8.tar.gz`
2. 安装 python3

3. 编译

```bash
cd redis-stable
make
make install prefix=/usr/local/redis
mkdir /usr/local/redis/etc
mv redis.conf /usr/local/redis/etc
```

4. 修改为后台启动
   `将daemonize no 改成daemonize yes`
5. 将 redis 加入到开机启动

## centos7 安装 Python3.7

1. 安装依赖包
   `yum install gcc patch libffi-devel python-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y `
2. 下载 Python
   `wget https://www.python.org/ftp/python/3.7.10/Python-3.7.10.tgz`
3. 创建一个空文件夹，存放 python3 程序
   `mkdir /usr/local/python3`
4. 编译/安装

```bash
./configure --prefix=/usr/local/python3
./configure --enable-optimization
make
make install prefix=/usr/local/python3
```
