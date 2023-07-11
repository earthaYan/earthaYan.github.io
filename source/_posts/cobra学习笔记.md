---
title: cobra学习笔记
date: 2023-04-03 22:04:19
tags: [GoLang]
categories: 后端
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
    Short string
    GroupID string
    Example  string
    ValidArgs []string
    ValidArgsFunction func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
    Args PositionalArgs
	ArgAliases []string
    BashCompletionFunction string
    Deprecated string
    Annotations map[string]string
    Version string
    PersistentPreRun func(cmd *Command, args []string)
    PersistentPreRunE func(cmd *Command, args []string) error
    PreRun func(cmd *Command, args []string)
    PreRunE func(cmd *Command, args []string) error
    Run func(cmd *Command, args []string)
    RunE func(cmd *Command, args []string) error
    PostRun func(cmd *Command, args []string)
    PostRunE func(cmd *Command, args []string) error
    PersistentPostRun func(cmd *Command, args []string)
    PersistentPostRunE func(cmd *Command, args []string) error
    FParseErrWhitelist FParseErrWhitelist
    CompletionOptions CompletionOptions
    TraverseChildren bool
    Hidden bool
    SilenceErrors bool
	SilenceUsage bool
    DisableFlagParsing bool
	DisableAutoGenTag bool
    DisableFlagsInUseLine bool
    DisableSuggestions bool
    SuggestionsMinimumDistance int
}
```
### Hidden
定义该命令不应该出现在可获得命令列表中的
### TraverseChildren
定义当用户输入该命令的路径时,是否遍历其子命令。
### CompletionOptions
定义自动补全选项
```go
var cmd = &cobra.Command{
  CompletionOptions: cobra.CompletionOptions{
    Flags: []string{"flag1", "flag2"},
    Commands: []string{"subcmd1", "subcmd2"},
    GlobalFlags: true,
  },
}

```
### FParseErrWhitelist
定义该命令在标志解析阶段忽略的错误。
原本：当我们在命令行中输入与命令标志不匹配的内容时,Cobra 会返回一个 flag parse error
```bash
Error: unknown flag: --gh
Usage:
  add [action] [options] [target] [flags]

Flags:
  -h, --help   help for add
```
### Run相关函数
> 执行顺序：
>	PersistentPreRun()
>	PreRun()
>	Run()
>	PostRun()
>	PersistentPostRun()
**Run和RunE的区别是后者会返回error**
#### PersistentPostRun
会在每次运行Run命令后被调用，会被子命令继承
#### PostRun
在Run之后调用，主要用于收尾工作
- 清理临时文件
- 断开数据库连接
- 停止日志记录
#### Run
通常是实际功能函数，命令的核心功能
- 访问命令的标志、参数等
- 执行命令的主要业务逻辑
- 调用外部服务
- 修改系统状态
- 返回结果给用户
- 如果没有定义Run,本质上就是一个空命令
#### PreRun
会在每次运行该命令前被调用，不会被子命令继承

#### PersistentPreRun
会在每次运行该命令前被调用，会被子命令继承
1. 验证全局标志或环境变量
2. 启动日志记录
3. 连接数据库等
#### PersistentPreRunE
### Annotations
用于为该命令添加注解，可以用`cmd.Annotations`访问，主要用于在应用逻辑中传递和共享上下文信息,对最终用户不可见。
### Version
为命令定义版本，如果命令中定义了该字段且命令还没有定义 `version`标志，则cobra会自动给命令添加 --version和-v 标志，前提是这两者都没有定义。
执行`cmd --version`会输出Version中定义的值
### Deprecated
如果该命令已经被废弃，当使用的时候应该打印这个字符串
### BashCompletionFunction
值是我们的 Bash 自动补全函数的函数名,例如:
```go
go
var cmd = &cobra.Command{
  BashCompletionFunction: "autocompleteDo",
}
// 同名函数实现
func autocompleteDo(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
  // ...
}
```
### ArgAliases
ValidArgs别名列表，不会提示给用户，但是手动输入也会接收
### Args
作用：指定它接收的位置参数模式,在内部可以：
1. 定义当前命令接收的位置参数
2. 校验用户输入的参数是否正确
3. 返回一个 nil 的 error 表示校验成功,或返回非 nil 的 error 表示校验失败
取值类型：`PositionalArgs`

```go
type PositionalArgs func(*Command, []string) error
```
### ValidArgsFunction
动态的ValidArgs，一个命令中不能同时存在`ValidArgsFunction`和`ValidArgs`选项
- 第三个参数`toCoplete`用于实现命令补全
    - cobra.ShellCompDirectiveDefault:继续使用默认的补全方案
    - cobra.ShellCompDirectiveError：阻止补全并返回错误
    - cobra.ShellCompDirectiveNoFileComp：仅提供文件名补全而非命令补全
```go
ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
    // 检查 toComplete 是否以 "enabl" 开头,如果是则返回可能的补全选项 ["enable", "enables", "enabling"]
  if toComplete == "enabl" {
    return []string{"enable", "enables", "enabling"}, cobra.ShellCompDirectiveNoFileComp 
  }
  
  if args[0] != "enable" {
    // 阻止补全并返回错误
    return nil, cobra.ShellCompDirectiveError
  }
  
  return nil, cobra.ShellCompDirectiveDefault
} 

```
### ValidArgs
作用：定义命令接收的所有合法的非flag参数，cobra会根据这个验证用户在shell命令中输入的参数是否有效，并在help输出中生成参数列表信息
疑问：为什么定义了ValidArgs，运行./demo add不会报错？
原因：cobra的解析流程导致的
1. 解析命令链,识别出各个命令和参数
2. 对每个命令及其参数,检查是否符合 ValidArgs 中的要求
3. 如果不符合,则视为普通参数传入,并继续后续检查
4. 检查是否定义了该参数的子命令
5. 如果没有子命令,则将该参数传入 Run 方法
6. 在 Run 方法中,需要我们自行判断该参数是否有效,如果无效需要手动报错
### Example
作用：示范如何使用命令
区别：Use定义规范，Example展示用例
### GroupID
#### 作用
用于将命令分组，具有相同 GroupID 的命令会被放入同一个命令组中。
1. 实际使用中不会影响命令的实际行为
2. 优化help输出和自动补全功能
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

> - 如果go build生成的二进制文件名demo和 rootCmd 的 Use 字段第一个单词相同,那么 ./demo 会直接被 Cobra 识别为 rootCmd 命令,而不是普通参数。
> - 如果不同，则./demo相当于普通参数传入，需要在Run方法中自行解析

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
### Short
定义命令或字段的简短描述，在`help`里展示的简短描述
#### 显示条件
1. 实际定义了该字段
2. 没有定义Long字段
如果同时定义了，则只会展示Long字段
### Long
作用：定义命令或字段的 详细描述
