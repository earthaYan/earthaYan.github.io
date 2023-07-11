---
layout: why I  Love Golang
title: Golang
date: 2022-11-21 10:21:51
tags: [GoLang]
categories: 翻译
---

# 为什么我喜欢 Golang

我喜欢 Go 语言编程,也就是一些人提到的 Golang。它简单且伟大。

我写的有点跑题。没想到 GoLang 会这么好。

我第一次遇到 Go 大概是在 2016 年 1 月份,它在以色列有一个比较小众却很活跃的社区。

当时也没多想,只是想磨练编程技能,GoLang 也只是我用来完成任务的一个工具。

即使是一年以前,使用 Go 也是非常明智的。一旦掌握了这门语言的核心要领,整个过程就很简单易懂。

我为公司[Visualead](https://www.visualead.com/)写了一段关键代码,它没有让我们失望,一年之后仍然以零维护的形式运行在生产环境。

最近我发现自己一次又一次地使用了 Golang,感觉有必要写一篇文章来描述我为什么对 GoLang 情有独钟了。

## GoPATH 环境

当你开始使用 Go 写代码的时候,这是你必须要处理的事情之一。

将你的电脑上的任意一个位置设置为 GOPATH 目录,并且里面包含 bin,src 和 pkg 目录,那就可以开始编码了。

```bash
// How the directory structure looks like:
go
- bin
- pkg
- src
```

我在 home 目录下为用到的每种编程语言都创建了一个新目录。home 目录的文件夹结构如下所示：

```bash
chef
cpp
elixir
elm
go
javascript
meteor
ocaml
php
python
scala
```

除了 Go 以外,没有一种语言是强制执行这种结构的。Go 迫使你为所有的 GoLang 项目定义一个根目录，这样做是非常有好处的,接下来我们马上就会讲到。

## GoLang 应用

想要创建一个新的 GoLang 应用?非常简单。

进入 `$GOPATH/src` 目录,创建一个新文件夹,并且创建一个新的 `file.go`，调用 `main` 包,添加一个 `func main() {}` 函数,这就大功告成了。从此以后你可以使用 go 所有的好东西了。

更多 Go 的好东西出现！但首先要提的必须是 GoLang modules。

## GoLang modules

我最喜欢的编程范式做得很好，我把模块系统视为面向对象类系统的一种替代方案。

GoLang 调用它的模块包。所以从现在起每次我们说一个模块就意味着一个包，反之亦然。

```bash
Module == Package == Module
```

在 GoLang 里面,你创建的每一个目录都会变成一个包。如果包的名称是 main,那他会变成一个应用。这有助于将代码自然分隔为可管理的逻辑块。

你总是想要从可复用的组件或者 Golang 的包中创建业务逻辑。

在现在的应用中,我必须在部分文件中操作一些行,并且一旦完成就会将他们上传到 AWS S3。

我的应用结构如下所示：

```bash
src
- my_app
- - main.go
- - main_test.go
- - uploader
- - - uploader.go
- - - uploader_test.go
- - replace_file_lines
- - - replace.go
- - - replace_test.go
- - - strings_util.go
- - - strings_util_test.go
```

`_test.go` 文件毫无疑问是 Golang 的单元测试文件,其核心部分有一个构建好的测试框架。

对于来自面向对象编程语言的人来说,把每个目录认为是一个完整的静态类是很有用的,并且 `.go` 文件中的每个函数或者变量会变成它的属性或者方法。

这里有个 `replace.go` 的例子：

```go
package replace_file_lines

import (
  // ...
)

// Variables that begin with an uppercase is exposed
var PublicVariable int = 42
// While those that begin with loweracse are private to the module
var privateVariable int = 0

// Function that begins with an uppercase is exposed
func Replace(oldFilePath, outputFilePath, with, what string) {
 // ...
}

// Function that begins with an uppercase is exposed
func PublicFunction(/* .. */) {
  // ...
)

// While lowercase names makes functions private to the module
func privateFunction(/* .. */) {
  // ...
)
```

如果一个目录有不止一个的 `.go` 文件,所有的方法和变量甚至是私有的,在整个包里面都是可共享的。这有助于将一个包分割成更小的块,也可以避免大的单个文件出现。

在不讨论面向对象 vs 功能/程序的情况下,知道 Go 创始人决定不再将经典的类放在语言里是很重要的。取而代之的是使用 struct/interface ，当然还有包。

## Golang gofmt

GoLang 有一个公约:一切该如何看待，每个案例和每行需要的精确空间。

这允许开发者可以专注于写代码而不是开始关于花括号位置的战争。

旧的 {} vs {\n} 战争：
{% asset_img cruly-brarce.png Or perhaps I am only happy because my side won in Go?%}

点击此处阅读关于该问题的更多信息:https://golang.org/cmd/gofmt/

## GoLang Import

import 总是相对于 `GOPATH/src` 来说的。一直如此。我不会夸大这个决定在这个程度上在沮丧中拯救了我。

警告：下一行会令人迷惑。【todo:此处翻译不确定】

当使用其他语言的时候,你既可以使用相对/绝对路径,也可以以某种方式设置古怪的 import,这使得你可以从鬼知道的任意地方导入一个文件(Python 我已经注意到你了)。

Go 用一种独特的方式解决了这个问题。所有的 import，无论是哪一个文件，都是相对于 `GOPATH/src` 而言。

所以在 my_app 中,主要的 import 如下所示：

```go
package main

import (
	"my_app/replace_file_lines"
	"my_app/uploader"
	// ...
)
```

my_app 在 src 目录下,所以我们首先需要提到它,然后导入存在于 my_app 下的包,比如 `uploader` 和 `replace_file_lines`。注意,我们不再是引入单个文件,而是引入了整个包。像挂件一样工作并且引起 零值可用。【todo:此处翻译不确定】

此外,除非你实际使用了导入的包,否则 GoLang 不会编译,这个小特性有助于你了解实际使用的每一个 import。

期望你的程序员能够写一个没有未使用的 import 的干净代码?那为什么不让你本地的 Go 关注这个呢?

## Golang Get System

import 章节让我们了解了 GoLang 下一个伟大的特性, `go get` 特性。当其他人对[JavaScripts NPM](https://www.npmjs.com/) 包管理印象深刻,Go 采用了任意的 git 仓库作为它的包管理。

它是怎么工作的呢?

我之前写过我需要上传到 S3 对么?然后这意味着我需要 AWS SDK 来完成这个任务。

为了让它可以工作,我只需要打开终端并且写下:

```
go get github.com/aws/aws-sdk-go
```

然后会发生什么呢?没有什么特殊的,GoLang 只是从https://github.com/aws/aws-sdk-go 下载了仓库到你的 `GOPATH/src` 目录下。

然后你为了使用 aws-sdk 需要做的只是导入它：

```go
package uploader

import (
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/aws"
	// ...
)
```

还记得所有的 import 都是相对于 `GOPATH/src` 么? 现在你可以知道 `s3` 包位于`GOPATH/src/github.com/aws/aws-sdk-go/services/s3` 下面。

简单,优雅。对于 Go 而言是另外一个闪光点。

## Golang Build 和 Package Systems

我们一直关注 `GOPATH/src` ,但是仍然有其他目录我们需要处理,`GOPATH/pkg` 和 `GOPATH/bin`。

GoLang 是一种编译型语言,这意味着代码必须先完成编译才能运行。GoLang 编译速度很快。它是怎么做的呢?

每次你编译代码运行的时候,GoLang 会在同样的路径创建一个 `.a` 文件作为包，它只出现在 `GOPATH/pkg` 目录里。这
意味着比如你编译了 aws-sdk,一次编译之后,就可以在你其他代码之间共享。

这当然不是 GoLang 编译快速的唯一原因,但是它只是一个引子来帮助你理解 `GOPATH/pkg` 的角色。

现在,关于 `GOPATH/bin` 有哪些用途呢? 当你运行 `go install` 命令的时候,go 会创建一个二进制文件,放在 `GOPATH/bin` 下面,文件获取到你的 main 包目录的名字,即我们案例里面的 `my_app`。

为什么说它非常棒呢? 因为你可以添加 `GOPATH/bin` 到环境变量中,这样构建的所有二进制文件都可以在命令行中获取到,而且不需要做任何额外的工作!(是不是很棒呢?)

## GoLang 跨平台构建

想要部署到编码平台以外的其他平台?别担心,你不需要使用 windows 机器来构建你的 windows 版本的代码。[GoLang 已经为你做好了](https://github.com/golang/go/wiki/WindowsCrossCompiling)。

主要运行:

```bash
GOOS=windows GOARCH=amd64 go install
```

我们的代码将会输出可以在 windows 机器上部署的二进制文件。 `.exe` 文件会出现在 `GOPATH/bin/windows_amd64/my_app.exe`。难度就像在公园里散步一样。

## Golang 编程语言

GoLang 旨在成为一门简单的编程语言。

我很喜欢下面这个帖子,它问道:为什么 Go 没有被设计成函数式语言： https://www.quora.com/Why-wasnt-Go-written-as-a-functional-language

> 在 google 工作的程序员职业生涯开始得很早，并且最熟悉过程式编程语言，尤其是来自于 c 语言家族的。需要程序员快速提高生产力,这意味着语言不能过于激进。

它确实很简单。

这是 GoLang 不支持的部分特性清单:

1. 类
2. 操作符重载
3. 函数重载
4. 可选参数
5. 异常

尽管有时候我发现写 Go 的时候会丢掉一些语言特性,但是最终总是能够完成想做的事。只是有时候,需要更多的写和偶尔的思考。底线就是它使得代码更容易推理,不会那么抽象。

有时候我很惊讶,在没有多年经验的情况下,用 Go 写代码,我竟然可以如此之快地达到目标,仅仅因为这门语言如此包容和清晰。

## Golang 并发

我有意把关于并发的讨论留在最后。为什么?因为我不认为它不是那么重要。

它是 Go 语言中令人震惊的特性。但是有时候被认为是 Go 语言的本质,我不认同这种说法。

因此我准备尝试用一段话总结一下。

是的,GoLang 有很棒的并发性。你不需要处理线程,只需要创建简单的 goroutine,它的制作和管理都很简单。 Goroutines 使你可以在所有的 CPU 上分配负载，而不需要担心如何管理。

有兴趣进一步了解 goroutines?可以阅读：https://tour.golang.org/concurrency/1
