---
title: 01-goLang-Proxy
date: 2022-10-01 14:25:37
tags: [golang,后端]
categories: GoLang
---


背景：国内因为墙的原因，所以下载go lang的时候会报错443
解决方法：设置代理，且go尽量不要安装在默认目录下
常用代理：
- https://goproxy.io/zh/
- https://goproxy.cn
- https://mirrors.aliyun.com/goproxy/

设置步骤：
1. go env -w GO111MODULE=on
2. go env -w GOPROXY=https://goproxy.cn,direct

失败原因：
export GOPROXY=https://proxy.golang.com.cn,direct 该地址在中国大陆已被屏蔽，所以不可用
