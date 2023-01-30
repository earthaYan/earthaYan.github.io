---
title: go.mod文件
date: 2023-01-30 15:37:00
tags: [GoLang]
categories: [GoLang]
---
## go.mod常见用法以及注释
```go
// module path，一般采用仓库或者仓库+module_name定义
module github.com/actiontech/dtle

// go directive,非必须,指定代码所需要的go的最低版本，一般为go 1.xx
go 1.16

// require段中列出了项目所需要的各个依赖库以及它们的版本
require (
	// 正规版本号
	github.com/Shopify/sarama v1.26.4
	// 伪版本号： go module 为它生成的一个类似符合语义化版本 2.0.0 版本，实际这个库并没有发布这个版本
	// commit 的 base versio-本次提交时间-第三方库本次提交时最新的commitId
	github.com/actiontech/golang-live-coverage-report v0.0.0-20210902074032-43aa91afdc2c
	//indirect: 间接的使用了这个库，但是又没有被列到某个 go.mod 中
	// 1. 当前项目依赖 A，但是 A 的go.mod 遗漏了 B，那么就会在当前项目的 go.mod 中补充 B，加 indirect 注释；
	// 2.	当前项目依赖 A，但是 A 没有 go.mod，同样就会在当前项目的 go.mod 中补充 B，加 indirect 注释；
	// 3.	当前项目依赖 A，A 又依赖 B。当对 A 降级的时候，降级的 A 不再依赖 B，这个时候 B 就标记 indirect 注释。我们可以执行go mod tidy来清理不依赖的 module。
	github.com/go-playground/universal-translator v0.17.0 // indirect
	// 没有采用go.mod管理或者module path 中依然没有添加 v2、v3 这样的后缀,不符合 Go 的 module 管理规范
	github.com/go-playground/validator v9.31.0+incompatible
)

// 1. 替换库
// 2.	某个依赖库有问题，自己 fork 到本地做修改，通过替换成本地文件夹进行调试
replace github.com/go-mysql-org/go-mysql => github.com/ffffwh/go-mysql v0.0.0-20211206100736-edbdc58f729a

//replace github.com/Sirupsen/logrus => github.com/sirupsen/logrus v1.4.2

replace github.com/araddon/qlbridge => github.com/ffffwh/qlbridge v0.0.0-20220113095321-0b48c80b13e9

replace github.com/pingcap/dm => github.com/actiontech/dm v0.0.0-20211206092524-9e640f6da0ac

replace github.com/pingcap/tidb => github.com/actiontech/tidb v0.0.0-20220928030323-1f192702a2c7

replace github.com/pingcap/tidb/parser => github.com/actiontech/tidb/parser v0.0.0-20220928030323-1f192702a2c7

// 后面的commitId为当时提交代码的时候依赖包的commitId
replace github.com/hashicorp/go-discover => github.com/hashicorp/go-discover v0.0.0-20211203145537-8b3ddf4349a8
// 将grpc版本固定为1.29.1
replace google.golang.org/grpc => google.golang.org/grpc v1.29.1

// exclude :Go 在版本选择的时候，如go get -u 或者go get github.com/xxx/xxx@latest 就会主动跳过这些版本
// retract :go 1.16 中新增加的内容

```


## 第三方库的replace
### 场景
第三方库中缺少自己项目中需要的某个方法，自己fork一份并加入自定义的新方法，在项目中调用这个自定义方法
### 解决方法1-引用新库
1. 将fork的库的go.mod中module name 修改为一个新的 name
2. 增加所需要的方法
3. 增加新的 git tag
4. 当前项目中，引用修改后的这个 repo，替换地址以及tag版本号
### 解决方法2 - go mod replace 
1. fork第三方库
2. 增加需要的方法
3. 在当前项目中，执行 go mod edit -replace 命令:`go mod edit -replace=old[@v]=new[@v]`

```go
go mod edit -replace=golang.org/x/image@v0.0.0-20180708004352-c73c2afc3b81=github.com/golang/image@v0.0.0-20180708004352-c73c2afc3b81

```
## 补充知识
### 初始化module 
`go mod init project_name`
### go mod tidy作用
1. 解析项目文件，并找到所使用的包
2. 生成 go.sum 文件，其中保存了所使用包的版本
### 执行项目
`go run main.go`