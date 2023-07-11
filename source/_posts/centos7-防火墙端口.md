---
title: centos7-防火墙端口
date: 2022-11-30 08:55:24
tags: [CentOS]
categories: 虚拟机
---

## 查看端口占用
```bash
lsof -i:8000
```
## 开启/关闭端口
```bash
firewall-cmd --zone=public --add-port=5672/tcp --permanent   # 开放5672端口

firewall-cmd --zone=public --remove-port=5672/tcp --permanent  #关闭5672端口

firewall-cmd --reload   # 配置立即生效
```

## 查看防火墙开放的所有端口
```bash
firewall-cmd --zone=public --list-ports
```

## 全局关闭防火墙
```bash
systemctl stop firewalld.service
```

## 查看防火墙状态
```bash
 firewall-cmd --state
```

## 检查端口被进程占用情况
```bash
netstat -lnpt |grep 5672
```

## 查看进程的详细信息
```bash
ps pid
```

## 终止进程
```bash
kill -9 pid
```