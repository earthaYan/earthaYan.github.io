---
title: 02-用go写一个hello_word程序
date: 2022-10-08 15:32:39
tags: [GoLang]
categories: 后端
---

去除 go.mod 文件中项目不需要的依赖：`go mod tidy `

## 用 go 写一个 hello_word 程序

go_demo/pki/main.go

```go
// 包声明:源文件中非注释的第一行,指明这个文件属于哪个包
// package main表示一个可独立执行的程序，每个 Go 应用程序都包含一个名为 main 的包
package main
// 引入包:告诉 Go 编译器这个程序需要使用 fmt 包
// 方式1：编写多个导入语句
// 方式2: 用圆括号组合了导入
import "fmt"
// 程序开始执行的函数。main 函数是每一个可执行程序所必须包含的，
// 一般来说都是在启动后第一个执行的函数（如果有 init() 函数则会先执行该函数）

func main(){
	/* 这是我的第一个简单的程序 */
	fmt.Println("Hello, World!")
}
func init(){
	fmt.Println("init me first!")
}
```

> ##### 注意点：
>
> 1. 当标识符以一个大写字母开头,使用这种形式的标识符的对象就可以被外部包的代码所使用，即导出
> 2. 标识符如果以小写字母开头，则对包外是不可见的，但是他们在整个包的内部是可见并且可用的
> 3. 函数的左侧大括号不能单独一行，否则会报错
> 4. 导入：方式 1-编写多个导入语句;方式 2-用圆括号组合导入

## 运行程序

```bash
 go run pki/main.go
```

运行结果
{% asset_img hello.jpg 执行go run  %}

## 生成二进制文件

在根目录处生成同名二进制文件

```bash
go build pki/main.go
```

## 问题

### 导入同一个项目中的本地包报错

{% asset_img error.jpg 导入本地包报错  %}
官方文档(1.16)提供的方法:

1. 进入待导入本地包目录
2. 执行 `go build`
3. 进入项目根目录
4. 执行 `go install go_demo`

> 结果:本地开发环境为 1.19,验证为在该版本上无效,报错同尝试 1

#### 尝试 1:

```go
import (
	"fmt"
	"go_demo/mathClass"
)
```

结果:

> package go_demo/mathClass is not in GOROOT

#### 尝试 2:

菜鸟教程上有一个笔记说包名和文件夹名称无关,于是基于尝试 1,将 package 名称和对应的文件夹名称修改一致
结果:成功,但是不知道为啥...

补充：如果觉得包名和文件夹名称必须一致很麻烦，可以使用别名的方式

```go
import (
	"fmt"
	complex "test_mod/ArrayDemo"
	"test_mod/functionList"
)
func init() {
	fmt.Println("init me first!")
	complex.GetAddress()
}

```

{% asset_img package.png package和文件夹名称不一样的时候的处理 %}

## 参考文章:

[issue#38812](https://github.com/golang/go/issues/38812)
