---
title: Go语言环境的安装
date: 2022-10-01 14:25:37
tags: [golang,后端]
categories: GoLang
---
## 安装

### windows:
下载[文件](https://golang.google.cn/dl/go1.19.2.windows-amd64.msi)，直接next直至完成

### Linux：
#### 通用步骤
1. 安装必要的包
```bash
yum install mercurial
yum install git 
yum install gcc
```
2. 下载go的压缩包并解压缩
```bash
cd /usr/local/
wget https://go.dev/dl/go1.19.2.linux-amd64.tar.gz
```
> 如果该地址不可用443，可以使用 <font color="red">`https://golang.google.cn/dl/go1.19.2.linux-amd64.tar.gz`</font> 代替

3. 添加PATH环境变量
```bash
vi ~/.bash_profile
# ~/.bash_profile添加内容
export GOROOT=/usr/local/go ##Golang安装目录
export PATH=$PATH:$GOROOT/bin
# 刷新环境变量
source ~/.bash_profile
```
4. 验证是否安装成功
{% asset_img go_version.jpg  安装成功 %}
#### v1.11以前
1. 设置GOPATH环境变量（go 1.11后不必设置,可使用go module）
```bash
export GOPATH=xxxx(即使手动设置为空，也会默认为/root/go)
```
2. 建立Go的工作空间（workspace，也就是 GOPATH 环境变量指向的目录）】
>GO代码必须在工作空间内。工作空间是一个目录，其中包含三个子目录：
> - src ---- 存放golang项目代码的位置,里面每一个子目录，就是一个包。
> - pkg ---- 编译后生成的，包的目标文件
> - bin ---- 生成的可执行文件，比如执行 `go get github.com/google/gops`,bin目录会生成 gops 的二进制文件。
```bash
cd /root
mkdir go
cd go/
mkdir bin
mkdir src
mkdir pkg
```
#### v1.11以后
1. 设置环境变量 GO111MODULE 进行开启或者关闭 go modules 模式
```bash
go env -w GO111MODULE=on #go env -w会将配置写到 GOENV 文件中去
```
> GO111MODULE的枚举值:
> - 空： auto自动模式，当项目根目录有 go.mod 文件，启用 Go modules
> - off： 关闭 go mod 模式
> - on： 开启go mod 模式

## GOPATH 缺点
{% asset_img GOPATH.jfif GOPATH %}

1. GOPATH模式下，必须指定目录,项目代码不能想放哪里就放哪里
2. go get 命令的时候，无法指定获取的版本
3. 引用第三方项目的时候，无法处理v1、v2、v3等不同版本的引用问题，因为在GOPATH 模式下项目路径都是 github.com/foo/project
4. 无法同步一致第三方版本号，在运行 Go 应用程序的时候，无法保证其它人与所期望依赖的第三方库是相同的版本。
## 问题

背景：国内因为墙的原因，所以下载一些包的时候会产生443报错
{% asset_img go_443.jpg  下载包报错 %}
解决方法：设置代理
常用代理：
- GOPROXY.IO：https://goproxy.io/zh/
- 七牛云：https://goproxy.cn
- 阿里云：https://mirrors.aliyun.com/goproxy/

设置步骤：
```bash
go env -w GOPROXY=https://goproxy.cn,direct
```
{% asset_img go_success.jpg 成功下载 %}

https://proxy.golang.com 设置为代理后拉包依旧失败原因：该地址在中国大陆已被屏蔽，所以不可用

```bash 
export GOPROXY=https://proxy.golang.com.cn,direct 
export GOPROXY=https://goproxy.io,direct
```



引用包：(指明本地路径)
 ```
 go mod edit -replace example.com/greetings=../greetings
 ```


 > 参考文章
 > 1. [简单聊聊 GOPATH 与 Go Modules](https://segmentfault.com/a/1190000041720288)