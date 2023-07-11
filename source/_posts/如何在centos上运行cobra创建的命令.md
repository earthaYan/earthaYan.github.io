---
title: 如何在centos上运行cobra创建的命令
date: 2023-05-24 22:42:47
tags: [GoLang]
categories: 后端
---
1. 编写源码
```go
package main
import (
  "fmt"
  "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
  Use:   "demo",
  Short: "A brief description of your application",
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Hello CentOS!")
  },
}
func main() {
  rootCmd.Execute()
}
```
2. 本地编译，生成可执行文件
`go build -o demo main.go`
3. 运行demo命令
`./demo`
4. 非必选：将demo命令添加到centos的全局环境中
`mv demo /usr/local/bin `
5. 接下来就可以直接通过demo命令在任何目录下执行该应用