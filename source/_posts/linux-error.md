---
title: linux-error
date: 2022-09-23 13:50:37
tags: [虚拟机, CentOS8]
categories: 虚拟机
---

## 报错信息

> Failed to download metadata for repo ‘AppStream’ [CentOS]

## 解决方法

1. 进入目录 `cd /etc/yum.repos.d/`
2. 执行以下命令：

- `sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*`
- `sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*`

3. 更新 `yum update -y`

## git 链接失败

报错失败：kex_exchange_identification: Connection closed by remote host
解决方法：将 Github 的连接端口从 22 改为 443 即可
.ssh/config 文件

```bash
Host github.com
    HostName ssh.github.com
    User git
    Port 443
```
