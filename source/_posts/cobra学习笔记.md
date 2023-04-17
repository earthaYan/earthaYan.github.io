---
title: cobra学习笔记
date: 2023-04-03 22:04:19
tags: [cobra,CLI]
categories: [GoLang]
---
cobra本质：Go的CLI（命令行界面）框架
cobra作用：
- 包含创建现代化CLI应用的库
- 包含一个用于快速生成基于Cobra的应用和命令文件的工具

## 安装
```bash
go get -u github.com/spf13/cobra@latest
import "github.com/spf13/cobra"
```

## 基础概念
Commands:动作
Args:事物
Flags:动作的修饰符
遵循的模式：`APPNAME VERB NOUN --ADJECTIVE`或者`APPNAME COMMAND ARG --FLAG`

### 举例
hugo server --po  rt=1313
遵循模式2，server是一个command,port是一个flag
git clone URL --bare
遵循模式1，clone是一个动词，URL是名词,bare是一个形容词。告诉git克隆url的内容

## Commands
cobra.Command
```go
type Command struct{
    // 描述用法信息，单行
    Use string
}
```
### Use用法
`add [-F file | -D dir]... [-f format] profile`
1. []标志：表明这是一份可选参数
2. ...标志：表明可以为之前的参数指定多个值
3. |标志：表明左右两边的参数是互相排斥的，即不能同时使用|左右两边的参数
4. {}标志：划定一系列互相排斥的参数，如果这些参数是可选的，应包括在[]之内

