---
title: 命令行框架cobra
date: 2023-02-17 01:40:56
tags: [GoLang,Cobra]
categories: GoLang
---

基于
1. Commands 命令
2. arguments 非选项参数
3. flags 选项参数（即标志）

```bash
# clone 是一个命令，URL是一个非选项参数，bare是一个选项参数
git clone URL --bare 
```

## 创建命令
### 使用cobra库
1. 创建一个 rootCmd——文件cmd/root.go
```bash
mkdir -p newApp2 && cd newApp2
var rootCmd = &cobra.Command{
  Use:   "hugo",
  Short: "Hugo is a very fast static site generator",
  Long: `A Fast and Flexible Static Site Generator`,
  Run: func(cmd *cobra.Command, args []string) {
    // Do Stuff Here
  },
}
func Execute() {
  if err := rootCmd.Execute(); err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
}
```
2. 创建main.go:调用rootCmd
```go
package main
import (
  "{pathToYourApp}/cmd"
)
func main() {
  // main.go 中不建议放很多代码，通常只需要调用 cmd.Execute() 
  cmd.Execute()
}
```   
3. 添加命令
```go
package cmd
import (
  "fmt"
  "github.com/spf13/cobra"
)
func init() {
    // 定义标志和处理配置  cmd/version.go文件
  rootCmd.AddCommand(versionCmd)
}
// rootCmd之外可以调用 AddCommand 添加其他命令
var versionCmd = &cobra.Command{
  Use:   "version",
  Short: "Print the version number of Hugo",
  Long:  `All software has versions. This is Hugo's`,
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hugo Static Site Generator v0.9 -- HEAD")
  },
}
```
4. 编译运行
`go build -v .`

### 使用Cobra 命令
生成一个 Cobra 命令模板，而命令模板也是通过引用 Cobra 库来构建命令的


## 核心特性
### 使用标志
1. 使用持久化的标志
作用：用于它所分配的命令以及该命令下的每个子命令
`rootCmd.PersistentFlags().BoolVarP(&Verbose, "verbose", "v", false, "verbose output")`
2. 使用本地标志
作用：本地标志只能在它所绑定的命令上使用
`rootCmd.Flags().StringVarP(&Source, "source", "s", "", "Source directory to read from")`
3. 将标志绑到viper
作用：可以通过viper.Get()获取标志的值
```go
var author string
func init() {
  rootCmd.PersistentFlags().StringVar(&author, "author", "YOUR NAME", "Author name for copyright attribution")
  viper.BindPFlag("author", rootCmd.PersistentFlags().Lookup("author"))
}
```
4. 设置标志为必选
```go
rootCmd.Flags().StringVarP(&Region, "region", "r", "", "AWS region (required)")
rootCmd.MarkFlagRequired("region")
```

### 非选项参数验证
使用 Command 的 Args 字段来验证非选项参数
#### 内置验证函数
- NoArgs：如果存在任何非选项参数，该命令将报错。
- ArbitraryArgs：该命令将接受任何非选项参数。
- OnlyValidArgs：如果有任何非选项参数不在 Command 的 ValidArgs 字段中，该命令将报错。
- MinimumNArgs(int)：如果没有至少 N 个非选项参数，该命令将报错。
- MaximumNArgs(int)：如果有多于 N 个非选项参数，该命令将报错。
- ExactArgs(int)：如果非选项参数个数不为 N，该命令将报错。
- ExactValidArgs(int)：如果非选项参数的个数不为 N，或者非选项参数不在 Command 的 ValidArgs 字段中，该命令将报错。
- RangeArgs(min, max)：如果非选项参数的个数不在 min 和 max 之间，该命令将报错。

```go
var cmd = &cobra.Command{
  Short: "hello",
  Args: cobra.MinimumNArgs(1), // 使用内置的验证函数
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello, World!")
  },
}
```
#### 自定义验证函数
```go
var cmd = &cobra.Command{
  Short: "hello",
  Args: func(cmd *cobra.Command, args []string) error { // 自定义验证函数
    if len(args) < 1 {
      return errors.New("requires at least one arg")
    }
    if myapp.IsValidColor(args[0]) {
      return nil
    }
    return fmt.Errorf("invalid color specified: %s", args[0])
  },
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello, World!")
  },
}
```
解析命令行参数->Pflag
解析配置文件-> Viper->从命令行参数、环境变量、配置文件等位置读取配置项
实现命令行框架->  Cobra
