---
title: 15-go-viper-cobra-pflag
date: 2022-11-22 11:28:33
tags: [golang, 后端, 实践]
categories: GoLang
---

## 如何构建应用框架

### 命令行参数解析 pflag 包

用来解析命令行参数【启动参数】，这些命令行参数可以影响命令的运行效果。

#### flag 定义

一个命令行参数在 Pflag 包中会解析为一个 Flag 类型的变量，即:

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
```

Flag 的值是一个 Value 类型的接口，通过将 Flag 的值抽象成一个 interface 接口，可以自定义 Flag 的类型了,只要实现了 Value 接口的结构体，就是一个新类型

```go

type Value interface {
    String() string // 将flag类型的值转换为string类型的值，并返回string的内容
    Set(string) error // 将string类型的值转换为flag类型的值，转换失败报错
    Type() string // 返回flag的类型，例如：string、int、ip等
}
```

实际使用：

```go
package main

import (
    "fmt"
)

type Value interface {
    String() string // 将flag类型的值转换为string类型的值，并返回string的内容
    Set(string) error // 将string类型的值转换为flag类型的值，转换失败报错
    Type() string // 返回flag的类型，例如：string、int、ip等
}

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

func (flag1 Flag) String() {
    fmt.Println("将flag类型的值转换为string类型的值，并返回string的内容")
}

type Flag2 struct {
  Value               Value  // flag的值
}

func (flag2 Flag2) String() {
    fmt.Println("自定义flag类型")
}

func main() {
    var val Value
    flag1 = new(Flag)
    flag1.String()
    flag2 = new(Flag2)
    flag2.String()
}
```

#### FlagSet 定义

预先定义好的 Flag 的集合
获取并使用 Flag 的方法：

1. 调用 NewFlagSet 创建一个 FlagSet,通过定义一个新的 FlagSet 来定义命令及其子命令的 Flag。

```go
var version bool
flagSet:=pflag.NewFlagSet("test",pflag.ContinueOnError)
flagSet.BoolVar(&version,"version",true,"Print version information and quit.")
```

2. 使用 Pflag 包定义的全局 FlagSet：CommandLine。实际上 CommandLine 也是由 NewFlagSet 函数创建的
   在一些不需要定义子命令的命令行工具中，我们可以直接使用全局的 FlagSet

```go

import (
    "github.com/spf13/pflag"
)

pflag.BoolVarP(&version, "version", "v", true, "Print version information and quit.")
func BoolVarP(p *bool, name, shorthand string, value bool, usage string) {
  flag := CommandLine.VarPF(newBoolValue(value, p), name, shorthand, usage)
  flag.NoOptDefVal = "true"
}
```

#### 常用方法

---

1. 支持多种命令行参数定义方式

- 支持长选项、默认值和使用文本，并将标志的值存储在指针中

```go
var name=pflag.String("name","colin","Input ur name")
```

- 支持长选项、短选项、默认值和使用文本，并将标志的值存储在指针中

```go
var name=pflag.StringP("name","n","colin","input ur name")
```

- 支持长选项、默认值和使用文本，并将标志的值绑定到变量

```go
var name string
pflag.StringVar(&name,"name","colin","Input ur name")
```

- 支持长选项、短选项、默认值和使用文本，并将标志的值绑定到变量

```go
var name string
pflag.StringVarP(&name, "name", "n","colin", "Input Your Name")
```

> 1. 函数名带有 Var 说明是将标志的值绑定到变量，否则就是将标志的值存储在指针中
> 2. 函数名带 P 说明支持短选项，否则不支持短选项。

---

2.  使用 Get<Type> 获取参数的值

```go

i, err := flagset.GetInt("flagname")
```

---

3. 获取非选项参数

```go

package main

import (
    "fmt"
    "github.com/spf13/pflag"
)
// 定义标志
var  flagvar = pflag.Int("flagname", 1234, "help message for flagname")

func main() {
    // 解析定义的标志
    pflag.Parse()
    // 返回无选项参数
    fmt.Printf("argument number is: %v\n", pflag.NArg())
    // 返回所有的非选项参数
    fmt.Printf("argument list is: %v\n", pflag.Args())
    //pflag.Arg(i) 返回第 i 个非选项参数
    fmt.Printf("the first argument is: %v\n", pflag.Arg(0))
}
// go run example1.go arg1 arg2
// argument number is: 2
// argument list is: [arg1 arg2]
// the first argument is: arg1
```

---

4. 指定了选项但是没有指定选项值时的默认值

```go
// 定义标志
var ip = pflag.IntP("flagname", "f", 1234, "help message")
// 为ip这个flag设置NoOptDefVal,
pflag.Lookup("flagname").NoOptDefVal = "4321"
```

| 命令行参数      | 解析结果 |
| --------------- | -------- |
| --flagname=1357 | ip=1357  |
| --flagname      | ip=4321  |
|                 | ip=1234  |

---

5. 弃用标志或者弃用标志的简写

在帮助文本中会被隐藏，并在使用不推荐的标志或简写时打印正确的用法提示

```go
pflag.CommandLine.MarkDeprecated("logmode","please use --log-mode instead")
//隐藏帮助文本中的logmode.当使用logmode的时候，打印出 Flag --logmode has been deprecated, please use --log-mode instead。
```

---

6. 只弃用简写形式

```go
pflag.IntVarP(&port,"port","p",3306,"MySQL service host port.")
// 弃用简写形式
pflag.CommandLine.MarkShorthandDeprecated("port", "please use --port only")

// 这样隐藏了帮助文本中的简写 P，并且当使用简写 P 时，打印了Flag shorthand -P has been deprecated, please use --port only。usage message 在此处必不可少，并且不应为空。
```

---

7. 隐藏标志

将 Flag 标记为隐藏，仍然可以正常运行，但不会显示在 usage/help 中,只在内部使用

```go
// hide a flag by specifying its name
pflag.CommandLine.MarkHidden("secretFlag")
```

---

### 配置文件解析 viper

小型应用：配置项较少,可以通过命令行参数来传递配置
大型应用：配置项较多,通常具有很多参数，通过命令行参数传递不好维护。
解决方法：将这些配置信息保存在配置文件中，由程序启动时加载和解析
Viper 特点：
高优先级配置会覆盖低优先级相同配置

#### 优先级排序

1. 通过 viper.Set 函数显示设置的配置
2. 命令行参数
3. 环境变量
4. 配置文件
5. Key/Value 存储
6. 默认值

#### 读入配置：将配置读入到 Viper 中

1. 设置默认的配置文件名

```go

viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})

```

---

2. 读取配置文件

支持 JSON、TOML、YAML、YML、Properties、Props、Prop、HCL、Dotenv、Env 格式的配置文件

```go

package main

import (
  "fmt"
  "github.com/spf13/pflag"
  "github.com/spf13/viper"
)

var (
  cfg  = pflag.StringP("config", "c", "", "Configuration file.")
  help = pflag.BoolP("help", "h", false, "Show this help message.")
)

func main() {
  pflag.Parse()
  if *help {
    pflag.Usage()
    return
  }
  // 从配置文件中读取配置
  if *cfg != "" {
    viper.SetConfigFile(*cfg)   // 指定配置文件名
    // 如果配置文件名中没有文件扩展名，则需要指定配置文件的格式，告诉viper以何种格式解析文件
    viper.SetConfigType("yaml")
  } else {
    // 会根据添加的路径顺序搜索配置文件，如果找到则停止搜索
    viper.AddConfigPath(".")          // 把当前目录加入到配置文件的搜索路径中
    viper.AddConfigPath("$HOME/.iam") // 配置文件搜索路径，可以设置多个配置文件搜索路径
    viper.SetConfigName("config")     // 配置文件名称（没有文件扩展名）
  }

  if err := viper.ReadInConfig(); err != nil {
    // 读取配置文件。如果指定了配置文件名，则使用指定的配置文件，否则在注册的搜索路径中搜索
    panic(fmt.Errorf("Fatal error config file: %s \n", err))
  }
  fmt.Printf("Used configuration file is: %s\n", viper.ConfigFileUsed())
}
```

---

3. 监听和重新读取配置文件【不推荐】

在运行的时候应用程序实时读取配置文件[热加载配置]。通过`WatchConfig`函数进行操作。
在操作之前需要确保已经添加了配置文件的搜索路径
可以为 Viper 提供一个回调函数，以便在每次发生更改时运行
不推荐使用原因：因为即使配置热加载了，程序中的代码也不一定会热加载。例如：修改了服务监听端口，但是服务没有重启，这时候服务还是监听在老的端口上，会造成不一致。

```go
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) {
   // 配置文件发生变更之后会调用的回调函数
  fmt.Println("Config file changed:", e.Name)
})
```

---

4. 从 io.Reader 读取配置

---

5. 从环境变量读取【区分大小写】
   - AutomaticEnv()
   - BindEnv(input …string)
   - errorSetEnvPrefix(in string)
   - SetEnvKeyReplacer(r \*strings.Replacer)
   - AllowEmptyEnv(allowEmptyEnv bool)

---

6. 从命令行标志读取

```go
// 绑定单个标志
viper.BindPFlag("token", pflag.Lookup("token"))
```

---

7. 从远程 Key/Value 存储读取

---

#### 读取配置

### 应用的命令行框架 Cobra

1. 命令需要具备 Help 功能，这样才能告诉使用者如何去使用
2. 命令需要能够解析命令行参数和配置文件
3. 命令需要能够初始化业务代码，并最终启动业务进程
