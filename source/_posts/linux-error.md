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

## git clone 报错

具体报错信息：

> git clone git@github.com:marmotedu/iam.git
> Cloning into 'iam'...
> Unable to negotiate with 192.30.255.112 port 22: no matching MAC found. Their offer: hmac-sha2-512-etm@openssh.com,
> hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
> fatal: Could not read from remote repository.
> Please make sure you have the correct access rights

解决方法：
在`/etc/ssh/ssh_config`文件最后一行修改`MACs hmac-sha1`为`MACs hmac-sha1,hmac-sha2-256,hmac-sha2-512`

## centos7 安装 最新版 git

1. 将最新版压缩包上传到云服务器（scp 命令）`scp git-2.38.1.tar.gz root@36.133.137.19:/root/setup/`
2. 安装依赖并解压，进入解压后的文件夹

```bash
yum -y install curl-devel expat-devel openssl-devel zlib-devel
yum -y install gcc
tar -zxf git-2.38.1.tar.gz
cd git-2.38.1
```

3. 编译并安装

```bash
make
make install prefix=/usr/local/git
```

此时会在/usr/local/下生成文件夹 git
{% asset_img make.jpg 生成文件夹git%}
进入文件夹后执行`./git --version`

4. 使其全局生效

- 通过将其添加至环境变量

```bash
# /etc/profile
PATH=$PATH:/usr/local/git/bin
EXPORT PATH
# shell
source /etc/profile
```

- 软链接[实测并不生效]

### 参考文章:

1. https://git-scm.com/download/linux
2. https://www.cnblogs.com/zhi-leaf/p/10978538.html
