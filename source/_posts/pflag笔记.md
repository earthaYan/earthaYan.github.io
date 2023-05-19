---
title: pflag笔记
date: 2023-05-19 13:25:23
tags: [GoLang, flag, 命令行]
categories: GoLang
---

前提：pflag 是完全兼容 flag 的

## 安装

安装：`go get github.com/spf13/pflag`
测试：`go test github.com/spf13/pflag`

## 在包中引入并定义 flag

`import flag "github.com/spf13/pflag"`

- 使用 lag.String(),Bool(),Int()等声明 flag
  `var ip *int = flag.Int("flagName", 1234, "help message for flagName")`
- 使用 Var()函数将 flag 绑定到一个变量

```go
var ipFlag int
flag.IntVar(&ipFlag,"flagName",1234,"help message from flagName")
```

- 创建满足 Value 接口的自定义 flag

```go
type Duration time.Duration
func (d *Duration) Set(s string) error {
  // 解析s为 Duration 并保存
}
func (d *Duration) Type() string {
  return "duration"
}
func (d *Duration) String() string {
  return time.Duration(*d).String()
}

var duration Duration
pflag.Var(&duration, "duration", "Some duration")
```

当你在命令行参数中传入`--duration=1m30s`后:

1. pflag 找到 Duration 类型并调用 Set("1m30s")
2. Set()方法使用指针接收器解析该值并保存在 Duration 的内部字段中
3. duration 现在保存传递的值(90 秒)
4. 通过 duration.String()或直接使用 duration 的值访问解析后的值

## 解析

前提：所有的 flag 都定义好了
方法：`flag.Parse()`

```go
	var ip *int = flag.Int("ip", 123, "help message from ip")
	var ipFlag int
	flag.IntVar(&ipFlag, "ipFlag", 1234, "help message from ipFlag")
	flag.Parse()
	fmt.Println(*ip,ipFlag)
```

执行`go run . --ipFlag=12 --ip=345`,运行结果为 345,12

### flagSet
