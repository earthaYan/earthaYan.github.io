---
title: iam项目的部署
date: 2022-12-08 22:16:09
tags: [golang, 实践]
categories: GoLang
---

## 设置环境变量
```bash
tee -a $HOME/.bashrc << 'EOF'
# Alias for quick access
export IAM_ROOT="/root/workspace/iam"
alias i="cd /root/iam"
EOF
```
## 安装和配置数据库
### MariaDB
mySQL的社区版,属于关系型数据库。用来存储 REST 资源的定义信息存储
### Redis
### MongoDB
## 安装和配置iam服务
### iam-apiServer
### iam-authz-server
### iam-pump
### iam-ctl
### man文件