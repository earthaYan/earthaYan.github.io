---
title: PFlag
date: 2023-02-16 22:37:23
tags: [GoLang,PFlag]
categories: GoLang
---

作用：
对命令行参数进行处理。一个命令行参数在Pflag包中会解析为一个`Flag`结构体类型的变量
```go

type Flag struct {
    Name                string // flag长选项的名称
    Shorthand           string // flag短选项的名称，一个缩写的字符
    Usage               string // flag的使用文本
    Value               Value  // flag的值
    DefValue            string // flag的默认值
    Changed             bool // 记录flag的值是否有被设置过
    NoOptDefVal         string // 当flag出现在命令行，但是没有指定选项值时的默认值
    Deprecated          string // 记录该flag是否被放弃
    Hidden              bool // 如果值为true，则从help/usage输出信息中隐藏该flag
    ShorthandDeprecated string // 如果flag的短选项被废弃，当使用flag的短选项时打印该信息
    Annotations         map[string][]string // 给flag设置注解
}

type Value interface {
    String() string // 将flag类型的值转换为string类型的值，并返回string的内容
    Set(string) error // 将string类型的值转换为flag类型的值，转换失败报错
    Type() string // 返回flag的类型，例如：string、int、ip等
}
```
总结：
通过将 Flag 的值抽象成一个 interface 接口，我们就可以自定义 Flag 的类型了。只要实现了 Value 接口的结构体，就是一个新类型。


## FlagSet
本质：预先定义好的一些Flag的集合,日常用FlagSet的方法操作Pflag
### 获取并使用FlagSet
1. 调用 `NewFlagSet`创建一个FlagSet
```go
var version bool
flagSet := pflag.NewFlagSet("test", pflag.ContinueOnError)
flagSet.BoolVar(&version, "version", true, "Print version information and quit.")
```
2. 使用全局FlagSet：`CommandLine`
主要用于不需要定义子命令的命令行工具
```go
import (
    "github.com/spf13/pflag"
)
pflag.BoolVarP(&version, "version", "v", true, "Print version information and quit.")

// pflag.BoolVarP 函数定义
func BoolVarP(p *bool, name, shorthand string, value bool, usage string) {
    flag := CommandLine.VarPF(newBoolValue(value, p), name, shorthand, usage)
    flag.NoOptDefVal = "true"
}

// CommandLine is the default set of command-line flags, parsed from os.Args.
var CommandLine = NewFlagSet(os.Args[0], ExitOnError)
```

## Pflag使用方法
### 支持多种命令行参数定义方式
> 函数名带Var -> true:将标志的值绑定到变量，false:将标志的值存储在指针中
> 函数名带P -> true:支持短选项，false:不支持短选项


1. 支持长选项、默认值和使用文本，并将标志的值存储在指针中
```go
var name = pflag.String("name", "colin", "Input Your Name")
```
2. 支持长选项、短选项、默认值和使用文本，并将标志的值存储在指针中。
```go
var name = pflag.StringP("name", "n", "colin", "Input Your Name")
```
3. 支持长选项、默认值和使用文本，并将标志的值绑定到变量
```go
var name string
pflag.StringVar(&name, "name", "colin", "Input Your Name")
```
4. 支持长选项、短选项、默认值和使用文本，并将标志的值绑定到变量。
```go
var name string
pflag.StringVarP(&name,"n","colin","Input Your Name")
```

### 使用Get<Type>获取参数的值
Type 代表 Pflag 所支持的类型
案例：有一个 pflag.FlagSet，带有一个名为 flagname 的 int 类型的标志，可以使用GetInt()来获取 int 值。需要注意 flagname 必须存在且必须是 int
```go
i, err := flagset.GetInt("flagname")
```

### 获取非选项参数
```go
package main
import (
    "fmt"
    "github.com/spf13/pflag"
)
var flagvar = pflag.Int("flagname", 1234, "help message for flagname")
func main() {
    // 解析定义的标志
    pflag.Parse()
    // 返回非选项参数的个数
    fmt.Printf("argument number is: %v\n", pflag.NArg()) //2
    // 返回所有的非选项参数
    fmt.Printf("argument list is: %v\n", pflag.Args()) //[arg1,arg2]
    // 返回第i个非选项参数
    fmt.Printf("the first argument is: %v\n", pflag.Arg(0))//arg1
}
go run example1.go arg1 arg2
```

### 指定了选项但是没有指定选项值时的默认值
```go
var ip = pflag.IntP("flagname", "f", 1234, "help message")
pflag.Lookup("flagname").NoOptDefVal = "4321"


--flagname=1357 -> ip=1357
--flagname -> ip=4321
[nothing] -> ip=1234
```

### 弃用标志或标志的简写
弃用标志在帮助文本中会被隐藏，并在使用不推荐的标志或简写时打印正确的用法提示
```go
//  deprecate a flag by specifying its name and a usage message
pflag.CommandLine.MarkDeprecated("logmode", "please use --log-mode instead")
```

### 弃用简写形式，保留标志
隐藏了帮助文本中的简写 
```go
pflag.IntVarP(&port, "port", "P", 3306, "MySQL service host port.")
// deprecate a flag shorthand by specifying its flag name and a usage message
pflag.CommandLine.MarkShorthandDeprecated("port", "please use --port only")
```

### 隐藏标志
仍将正常运行，但不会显示在 usage/help 文本中
```go
// hide a flag by specifying its name
pflag.CommandLine.MarkHidden("secretFlag")
```
