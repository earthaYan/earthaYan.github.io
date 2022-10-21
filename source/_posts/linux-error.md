---
title: linux-error
date: 2022-09-23 13:50:37
tags: [虚拟机, CentOS8]
categories: 虚拟机
---

## 报错信息

> Failed to download metadata for repo ‘AppStream’ [CentOS8]

## 解决方法

1. 进入目录 `cd /etc/yum.repos.d/`
2. 执行以下命令：

- `sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*`
- `sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*`

3. 更新 `yum update -y`

### 磁盘过满怎么处理

1. `docker volume prune -f`
2. https://blog.csdn.net/a854517900/article/details/80824966
