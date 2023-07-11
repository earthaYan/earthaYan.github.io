---
title: 如何使用Go写一个React项目脚手架
date: 2023-05-23 15:21:35
tags: [脚手架,GoLang]
categories: 后端
---

使用库：pflag + cobra + viper
实现思路：

1. 命令行工具使用 cobra。cobra 可以很容易的构建命令行工具,可以定义 init、build、start 等命令
2. 使用 pflag 为命令添加参数。例如 init 命令可以添加名称、模板类型等参数
3. 使用 viper 加载配置文件。可以在命令行传入--config 指定一个配置文件,viper 会加载并解析该配置文件。
4. 在 init 命令中,使用 viper 的配置生成 React 项目。可以指定项目名称、React 模板(create-react-app、Gatsby 等)等。然后执行相应的命令生成项目。
5. 在 start 命令中,可以运行 npm start 启动 React 项目开发服务器
6. build 命令用于构建 React 生产环境构建。可以执行 npm run build 并做其他构建相关工作。

## 基本目录结构：

.
├── cmd
│ ├── build.go # build 命令
│ ├── init.go # init 命令
│ └── start.go # start 命令  
├── main.go  
└── config.yaml # 默认配置文件

## 示例文件

定义一个 init 命令,支持--name 和--template 参数,使用 viper 和 cobra 构建一个 React 项目脚手架

```go
var initCmd = &cobra.Command{
    Use:   "init",
    Short: "Initialize a new React project",
    Run: func(cmd *cobra.Command, args []string) {
        // 使用viper读取配置
        template := viper.GetString("template")

        // 执行create-react-app等命令生成项目
        exec.Command("npx", "create-react-app", name, "--template", template).Start()
    },
}

func init() {
    initCmd.Flags().StringP("name", "n", "", "project name")
    initCmd.Flags().StringP("template", "t", "create-react-app", "project template (create-react-app, Gatsby, Next.js)")
    rootCmd.AddCommand(initCmd)
}
```
