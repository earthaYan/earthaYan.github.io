---
title: linux-error
date: 2022-09-23 13:50:37
tags: [CentOS]
categories: 虚拟机
---

## 报错信息

> Failed to download metadata for repo ‘AppStream’ [CentOS8]

### 解决方法

1. 进入目录 `cd /etc/yum.repos.d/`
2. 执行以下命令：

- `sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*`
- `sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*`

3. 更新 `yum update -y`

## 磁盘过满怎么处理

1. `docker volume prune -f`
2. https://blog.csdn.net/a854517900/article/details/80824966

## Linux 修改环境变量失败

1. /etc/profile
2. /root/.bash_profile（推荐）
3. **_ 修改完之后重启机器，环境变量的修改才会真正生效_**

## 把 centos7 系统打包成 docker 镜像

1. 安装 docker
2. 切换到系统根目录，对当前文件进行压缩
   `tar -cvpf /tmp/system.tar --directory=/ --exclude=proc --exclude=sys --exclude=dev --exclude=run --exclude=boot . `
   > /proc、/sys、/run、/dev 这几个目录都是系统启动时自动生成的，虽然也属于文件系统一部分，但是他们每次开机都会有变化，所以打包的时候就应该忽略它们
3. 导入 docker
   `docker import /tmp/system.tar linux:10.1`
4. 登录并新建仓库 emailforcodeyy/centos7_iam
5. 将生成的镜像推送到 docker hub

   ```bash
   docker login
   docker push emailforcodeyy/centos7_iam:v1.0.0
   ```

> 参考链接:https://cloud.tencent.com/developer/article/1920079
