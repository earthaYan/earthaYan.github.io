---
title: cobra学习笔记
date: 2023-04-03 22:04:19
tags: [cobra, CLI]
categories: [GoLang]
---

待阅读链接：

1. https://pkg.go.dev/github.com/spf13/cobra#Command
2. https://github.com/spf13/pflag
3. https://github.com/spf13/cobra-cli/blob/main/README.md

---

cobra 本质：Go 的 CLI（命令行界面）框架
cobra 作用：

- 包含创建现代化 CLI 应用的库
- 包含一个用于快速生成基于 Cobra 的应用和命令文件的工具

## 安装

```bash
go get -u github.com/spf13/cobra@latest
import "github.com/spf13/cobra"
```

## 基础概念

Commands:动作
Args:事物
Flags:动作的修饰符，用来修改 command 的行为
遵循的模式：`APP_NAME VERB NOUN --ADJECTIVE`或者`APP_NAME COMMAND ARG --FLAG`

### 举例

hugo server --port=1313
遵循模式 2，server 是一个 command,port 是一个 flag
git clone URL --bare
遵循模式 1，clone 是一个动词，URL 是名词,bare 是一个形容词。告诉 git 克隆 url 的内容

## 常见目录形式

GoDemo/[APP_NAME]  
├─ cmd/  
│ ├─ ApiServer.go[YOUR_COMMAND1.go]
│ └─ AuthzServer.go[YOUR_COMMAND2.go]
├─ go.mod  
├─ go.sum  
└─ main.go

### main.go 文件

Cobra 应用中，main.go 文件都非常空，它只有一个目的：初始化 Cobra

## 使用方法

### Cobra Generator
https://github.com/spf13/cobra-cli/blob/main/README.md
### Cobra Library
必须元素：
1. 一个空的main.go文件
2. 一个rootCmd 文件
```go
// rootCmd.go
package cmd

import (
	"fmt"
	"os"

	"github.com/mitchellh/go-homedir"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var rootCmd = &cobra.Command{
	Use:   "hugo",
	Short: "Hugo is a very fast static site generator",
	Long: `A Fast and Flexible Static Site Generator built with
	love by spf13 and friends in Go.
	Complete documentation is available at http://hugo.spf13.com`,
	Run: func(cmd *cobra.Command, args []string) {
		// 实际代码
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

var (
	cfgFile     string
	projectBase string
	userLicense string
)

func init() {
	cobra.OnInitialize(initConfig)
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.cobra.yaml)")
	rootCmd.PersistentFlags().StringVarP(&projectBase, "projectbase", "b", "", "base project directory eg. github.com/spf13/")
	rootCmd.PersistentFlags().StringP("author", "a", "your_name", "Author name for copyright attribution")
	rootCmd.PersistentFlags().StringVarP(&userLicense, "license", "l", "", "Name of license for the project (can provide `licenseText` in config)")
	rootCmd.PersistentFlags().Bool("viper", true, "Use Viper for configuration")
	viper.BindPFlag("author", rootCmd.PersistentFlags().Lookup("author"))
	viper.BindPFlag("projectbase", rootCmd.PersistentFlags().Lookup("projectbase"))
	viper.BindPFlag("useViper", rootCmd.PersistentFlags().Lookup("viper"))
	viper.SetDefault("author", "NAME HERE <EMAIL ADDRESS>")
	viper.SetDefault("license", "apache")
  // 添加额外的命令
	rootCmd.AddCommand(versionCmd)
}
func initConfig() {
	if cfgFile != "" {
		// 使用来自flag的配置文件
		viper.SetConfigFile(cfgFile)
	} else {
		// 获取用户目录
		home, err := homedir.Dir()
		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}
		// 在主目录中搜索名为“.cobra”（无扩展名）的配置。
		viper.AddConfigPath(home)
		viper.SetConfigFile(".cobra")
	}
	if err := viper.ReadInConfig(); err != nil {
		fmt.Println("Can't read config:", err)
		os.Exit(1)
	}
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

```go
// main.go
package main
import (
	"Demo/cmd"
)

func main() {
	cmd.Execute()
}
```

### 和Flags一起使用
#### 为一个command分配flags
1. 由于flags
```go

```
### 位置和自定义参数