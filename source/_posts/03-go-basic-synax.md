---
title: 03-go 基础语法
date: 2022-10-09 09:52:42
tags: [golang, 后端]
categories: GoLang
---

关键字，标识符(变量，类型)，常量，字符串，符号->标记->GO 程序

### 基础知识

1. 标识符：`A-Z,a-z,0-9,下划线\_`，第一个字符不能是数字
2. 字符串拼接：使用`+`实现
3. 保留字或者关键字不能作为标识符名
4. 变量的声明必须使用空格隔开 `var age int`
5. Go 程序是通过 package 来组织的，只有 package 名称为 main 的源码文件可以包含 main 函数，一个可执行程序有且仅有一个 main 包，其他包中即使有 main 函数也不会执行

### 数据类型

- 布尔型：
  - true
  - false
- 数字:
  - int/float32/float64
  - 支持复数
  - 位的运算采用补码
  - 无需定义 int 及 float32、float64，系统会自动识别
- 字符串
- 派生类型
  - 指针类型 Pointer
  - 数组类型
  - 结构化类型 struct
  - Channel 类型 chan
  - 函数类型 func
  - 切片类型
  - 接口类型 interface
  - Map 类型

### 变量

### 变量组成

`A-Z,a-z,0-9,下划线\_`，第一个字符不能是数字

### 变量声明

1. 可一次声明多个变量 `var identifier1, identifier2 type`
2. 不同类型的变量不可以一次声明多个 `var i int,f float64`会语法报错

#### 类型和变量声明

1. 指定变量类型，如果没有初始化，则变量默认为零值（即该类型的系统默认值）
2. 系统根据值自行判定变量类型
3. 如果变量已经使用 var 声明过了，再使用 := 声明变量，就产生编译错误，

```go
intVal := 1
//上下两者意义一致
var intVal int
intVal =1
```

#### 多变量声明

```go
//类型相同多个变量, 非全局变量
var vname1, vname2, vname3 type
vname1, vname2, vname3 = v1, v2, v3
var vname1, vname2, vname3 = v1, v2, v3 // 和 python 很像,不需要显示声明类型，自动推断
vname1, vname2, vname3 := v1, v2, v3 //  := 左侧的变量不应该是已经被声明过的，否则会导致编译错误
// 这种因式分解关键字的写法一般用于声明全局变量
var (
    vname1 v_type1
    vname2 v_type2
)
```

### 值类型和引用类型

{% asset_img 值类型和引用类型.jpg 值类型和引用类型 %}

#### 值类型

- 定义：使用这些类型的变量直接指向存在内存中的值
- 范围：基本类型都属于值类型
- 拷贝：当使用等号 = 将一个变量的值赋值给另一个变量时，如：j = i，实际上是在内存中将 i 的值进行了拷贝
- 存储：存储在堆中，通过 &i 来获取变量 i 的内存地址 ` fmt.Printf("地址：%d",&i)`

#### 引用类型

- 存储：一个引用类型的变量 r1 存储的是 r1 的值所在的内存地址（数字），或内存地址中第一个字所在的位置。内存地址称之为指针
- 拷贝：当使用赋值语句 r2 = r1 时，只有引用（地址）被复制，修改变量 r1 和 r2 会互相影响

### 常量

- 类型：布尔型、数字型和字符串型
- 在定义常量组的时候，如果不提供初始值，则初始值自动设置为上一行的<font color=red>**表达式**</font>
- 定义：

```go
const b string = "abc" //显式类型定义
const b = "abc" //隐式类型定义
```

- 常量表达式中，函数必须是 `len(), cap(), unsafe.Sizeof()`这些内置函数

### 特殊常量 iota

特殊之处：

- 可以被编译器修改的常量
- iota 在 const 关键字下次出现时将被重置为 0，const 中每新增一行常量声明将使 iota 计数一次

```go
func GetIOTA(){
	const (
		a = iota   //0
		b          //1
		c          //2
		d = "ha"   //独立值，iota += 1
		e          //"ha"   iota += 1
		f = 100    //iota +=1
		g          //100  iota +=1
		h = iota   //7,恢复计数
		i          //8
	)
	fmt.Printf("ITOA:%v %v %v %q %q %v %v %v %v\n",a,b,c,d,e,f,g,h,i)//0 1 2 ha ha 100 100 7 8
}

```
