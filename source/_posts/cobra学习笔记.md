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

## 安装和导入
```bash
go get -u github.com/spf13/cobra@latest
import "github.com/spf13/cobra"
```

## 基础概念
### Command
- 命令，表示一个行为或者动作，比如`serve`,`add`,`version`
- 一个命令可以有多个子命令
### Arg
- 参数，代表某个对象或事物
- 通常位于命令之后，比如`serve web` 中的 `web`
### Flags
- 标记，用于修饰或者配置命令的行为，以`--`或者`-`开头
- 比如 `--port`或者`-p`

## 遵循的模式：
1. `APPNAME VERB NOUN --ADJECTIVE`
git(APPNAME) add(VERB) file(NOUN)
2. `APPNAME COMMAND ARG --FLAG`
git(APPNAME) commit(COMMAND) docs/README.md(ARG) -m(FLAG)
### 举例
`hugo serve -p 8080 --baseURL https://example.com `
- command: serve,表示启动hugo的服务器
- flag：`-p`,`--baseUrl`,用于设置端口和baseUrl
- arg：无

`git add . `
- command: add,表示git添加文件
- flag：无
- arg：`.`，代表当前目录
`git commit -m "Update README"`
- command: commit,表示git提交文件
- flag：`-m`,设置提交信息
- arg：无

### flag和arg的区别
1. arg代表 必选参数，flag代表可选参数
2. arg如果缺少则command会报错，flag缺少不会报错，而是会使用默认值

## Command
类型定义
```go
type Command struct{
    Use string
    Aliases []string
    SuggestFor []string
}
```
### Use
#### 作用
1. 定义命令的使用说明,使用户快速理解每个命令及其子命令的用法
2. 在使用`--help`时显示,提供命令的帮助信息
3. 提供一种检验命令设计的手段
#### 语法
`Use:   "add [-F file | -D dir]... [-f format] profile"`
命令行使用:`./cobraDemo add xxx`
1. `[]`表示这个是可选参数,其他的参数是必须参数
2. `...`表示可以为前面的参数指定多个值,比如`Use: "app STR... NUM..."`,使用`app hello world 2 3` 。一个键(key)可以有多个值(value)
3. `|`表示互斥,在一个命令里不能同时使用两边的参数
4. `{}`表示分隔一组互斥参数,比如`add {arg1|arg2|arg3} {arg4|arg5|arg6}`
### Aliases
#### 作用
1. 表示命令或参数的别名
2. ` Aliases: []string{"param1", "p1","param2","p2"}`-param1的别名是p1,param2的别名是p2
### SuggestFor 
作用：用于为用户输入的错误参数提供建议
案例：
```go
var rootCmd = &cobra.Command{
    Use:        "app start|stop",  
    Args:       cobra.ExactArgs(1), 
    ValidArgs:  []string{"start", "stop"},
    SuggestFor: []string{"run"}, // 对 "run" 提供建议
}
```
此时用户输入`app run`，错误提示会变为：
- 不设置SuggstFor
> Error: invalid argument "run" for "app"
> Usage: app start|stop
- 设置SuggstFor
```go
SuggestFor: []string{"run"}, // 对 "run" 提供建议
```
>Error: invalid argument "run" for "app"
>Did you mean "start" or "stop"?
>Usage: app start|stop



