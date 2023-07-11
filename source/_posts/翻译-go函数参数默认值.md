---
title: 翻译-go函数参数默认值
date: 2023-02-23 10:32:59
tags: [GoLang]
categories: 翻译
---

原文地址：https://medium.com/@func25/golang-secret-how-to-add-default-values-to-function-parameters-60bd1e9625dc
## GloLang 小技巧：如何给 Function 参数添加默认值?

![](https://cdn-images-1.medium.com/max/4044/1*7PBtpnlYoSLWJMSOliQweQ.png)

你曾经因为 Go 没有默认参数值而感到苦恼吗?事实上你不是唯一一个!这种烦人的限制会让你的代码写起来单调乏味，读起来也更困难。

一直以来,你不得不写额外的代码来检测某个参数是否有被提供，如果没有的话要使用一个默认值赋给这个参数。

别担心!现在已经有方法来避开这些限制并且能添加默认值到 Go Function 里面。当然肯定不会像内置的方法那样方便,但是至少你不需要一直背负着限制。

Golang 小技巧系列:

- GloLang 小技巧：如何给 Function 参数添加默认值? (当前篇)

- [GloLang 小技巧: 自定义结构标签比如 `json:”name”`](https://medium.com/@func25/golang-technique-custom-struct-tag-technique-in-go-8667bf7da457)

## 简单的 wrapper

完成这件事的方法之一就是定义一个 wrapper 函数,在这个函数里将默认值作为参数调用原始函数。
如果客户端没有指明 name,默认的 name 就是"Aiden""。下面是一个使用 wrapper 的案例：

```go
    func greet(name string) string {
     return "Hello, " + name
    }

    func greetWithDefaultAiden(name string) string {
     if name == "" {
      name = "Aiden"
     }
     return greet(name)
    }

    // you can have more than 1 default set
    func greetWithDefaultJohn(name string) string {
     if name == "" {
      name = "John"
     }
     return greet(name)
    }
```

通过这种方式，可以在不修改 greet 函数内部的代码的情况下，为 greet 函数设置默认参数值。

> "但是这对于一个简单的函数来说是不是太臃肿了?"

这是一个不利之处，因为它需要你写一些额外的代码，这会让代码的可读性变差。

## 隐藏参数

我们可以把函数的惨呼放在一个未导出的 struct 中，允许客户端按照需要初始化这些参数：

```go
  type greetingArguments struct {
    Name string
    Age  int
  }

  func GreetingArguments() greetingArguments {
    return greetingArguments{
    Name: "Aiden",
    Age:  30,
    }
  }
```

现在定义 Greet 函数:

```go
    func Greet(options greetingArguments) string {
      return "Hello, my name is " + options.Name + " and I am " + strconv.Itoa(options.Age) + " years old."
    }
```

每次客户端想要使用 Greet 函数的时候,他们就必须使用 GreetingArguments()函数来创建一个 greetingArguments 类型的 struct。

这个方法只有在在从包外而不是包内调用函数时有效。

另外一个选择就是使用 functional options pattern，它可以让你向函数传递数量可变的选项作为参数。这个方法更灵活，代码可读性也更好，但是也会让你的代码更加复杂。

## Functional options pattern 功能选项模式

这个模式已经被很多库采用了。在本章节中，我会一步一步带你体验如何使用它：

1. 创建一个 struct,保存有两个字段的参数：Name 和 age。

```go
type GreetingOptions struct {
  Name string
  Age int
}
```

2. 现在顶一个 Greet 函数，将新的 struct 作为一个参数:

```go
func Greet(options GreetingOptions) string {
  return "Hello, my name is " + options.Name + " and I am " + strconv.Itoa(options.Age) + " years old."
}
```

3. 为 struct 中的字段定义功能选项是很有趣的内容:

```go
type GreetingOption func(*GreetingOptions)
func WithName(name string) GreetingOption {
  return func(o *GreetingOptions) {
    o.Name = name
  }
}
func WithAge(age int) GreetingOption {
  return func(o *GreetingOptions) {
    o.Age = age
  }
}
```

4. 使用新类型**GreetingOption** 创建 wrapper:

```go
func GreetWithDefaultOptions(options ...GreetingOption) string {
  opts := GreetingOptions{
    Name: "Aiden",
    Age: 30,
  }
  for _, o := range options {
    o(&opts)
  }
  return Greet(opts)
}
```

GreetWithDefaultOptions 函数为 GreetingOptions struct 的 Name(= “Aiden”)和 Age (= 30) 字段设置了默认值，然后将作为参数传递的选项应用到该 struct。

最后，使用修改后的 struct 作为参数调用 Greet 函数

为了使用这段代码，你可以调用使用你需要的选项调用 GreetWithDefaultOptions 函数：

```go
  greeting := GreetWithDefaultOptions(WithName("Alice"), WithAge(20))
  // "Hello, my name is Alice and I am 20 years old."
```

许多库都使用了 功能选项模式，这其中包括 mongodb, aws-sdk-go, gorm, cli 和许多其他的库
