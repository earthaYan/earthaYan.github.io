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
1. 创建一个 rootCmd 文件_cmd/root.go

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
    // 函数中定义标志和处理配置
  rootCmd.AddCommand(versionCmd)
}

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


### 使用Cobra 命令
生成一个 Cobra 命令模板，而命令模板也是通过引用 Cobra 库来构建命令的