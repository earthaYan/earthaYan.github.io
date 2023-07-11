---
title: ini文件配置
date: 2023-03-19 23:08:10
tags: [GoLang]
categories: 后端
---
github地址：https://github.com/go-ini/ini
文档地址：https://ini.unknwon.io/

包的功能：在Go语言中读写INI文件的功能
Go最低版本：1.6
安装：`go get gopkg.in/ini.v1`
更新：`go get -u gopkg.in/ini.v1`

my.ini
```bash
# my.ini
#  可选值：production, development
app_mode = development

# grafana存储临时文件，session和sqlite3数据库
[paths]
data=/home/git/grafana

[server]
# 协议
protocol=http
# http端口
http_port=9999
# 如果主机header不符合域名的话，重定向到正确的域名
# 防止 DNS 重新绑定攻击
enforce_domain=true
```
main.go
```go
func main() {
	cfg, err := ini.Load("my.ini")
	if err != nil {
		fmt.Printf("Fail to read file: %v", err)
		os.Exit(1)
	}
	// 简单的读取操作
	fmt.Println("App Mode:", cfg.Section("").Key("app_mode").String())
	fmt.Println("Data Path:", cfg.Section("paths").Key("data").String())
	// 做一些候选值限制的操作
	// 如果读取的值不在候选列表内，则会回退使用提供的默认值
	fmt.Println("Server Protocol:", cfg.Section("server").Key("protocol").In("http", []string{"http", "https"}))
	fmt.Println("Email Protocol:", cfg.Section("server").Key("protocol").In("smtp", []string{"imap", "smtp"}))
	// 自动类型转换
	fmt.Printf("Port Number:(%[1]T) %[1]d\n", cfg.Section("server").Key("http_port").MustInt((9999)))
	fmt.Printf("Enforce Domain: (%[1]T) %[1]v\n", cfg.Section("server").Key("enforce_domain").MustBool(false))
	// 修改某个值后保存到新文件
	cfg.Section("").Key("app_mode").SetValue("production")
	cfg.SaveTo("mysql.ini.local")
}
// 输出：
// App Mode: development
// Data Path: /home/git/grafana
// Server Protocol: http
// Email Protocol: smtp
// Port Number:(int) 9999
// Enforce Domain: (bool) true
```

### 从数据源加载配置
数据源类型：
- []byte类型的原始数据
- string 类型的文件路径
- io.ReadCloser

特点：
- 可以加载多个数据源  `ini.Load("my.ini")`
- 可以从一个空白的文件开始 `cfg:=ini.Empty()`
- 后期可以按需加载 `err := cfg.Append("other file", []byte("other raw data"))`
- 不确定是否有文件不存在，可以使用LooseLoad `cfg, err := ini.LooseLoad("filename", "filename_404")`,后期通过`Reload()`可以正常加载
- 加载多个数据源，如果出现同名键，则后面的配置会覆盖前面的配置
- 数据覆盖只有在使用 ShadowLoad 加载数据源不会被触发

#### 跳过无法识别的数据行
如果配置文件包含非键值对的数据行，解析器默认报错并终止解析
忽略错误：
```go
cfg, err := ini.LoadSources(ini.LoadOptions{
    SkipUnrecognizableLines: true,
}, "other.ini")
```

#### 保存配置
1. 输出配置到某个文件
```go
err = cfg.SaveTo("my.ini")
err = cfg.SaveToIndent("my.ini", "\t")
```
2. 写入到任何实现 io.Writer 接口的对象中
```go
cfg.WriteTo(writer)
cfg.WriteToIndent(writer, "\t")
```


### 操作分区Section
- 获取默认分区1:`sec, err := cfg.GetSection("")`
- 获取默认分区2:`sec, err := cfg.GetSection(ini.DEFAULT_SECTION)`
- 获取指定分区1：`sec, err := cfg.GetSection("section name")`
- 获取指定分区2：`sec := cfg.Section("section name")`，如果不存在则自动创建并返回一个对应的分区
- 创建分区：`err := cfg.NewSection("new section")`
- 获取所有分区对象或名称：

```go
secs := cfg.Sections()
names := cfg.SectionStrings()
```

#### 父子分区
概念：在分区名称中使用 . 来表示两个或多个分区之间的父子关系
关系：如果某个键在子分区中不存在，则会去它的父分区中再次寻找，直到没有父分区为止
```bash
NAME = ini
VERSION = v1
IMPORT_PATH = gopkg.in/%(NAME)s.%(VERSION)s

[package]
CLONE_URL = https://%(IMPORT_PATH)s

[package.sub]


# https://gopkg.in/ini.v1
cfg.Section("package.sub").Key("CLONE_URL").String()   
```

#### 非键值对分区
使用选项`LoadOptions.UnparsableSections`配置解析
```go
cfg, err := ini.LoadSources(ini.LoadOptions{
    UnparseableSections: []string{"COMMENTS"},
}, `[COMMENTS]<1><L.Slide#2> This slide has the fuel listed in the wrong units <e.1>`)

body := cfg.Section("COMMENTS").Body()

/* --- start ---
<1><L.Slide#2> This slide has the fuel listed in the wrong units <e.1>
------  end  --- */
```

### 操作键Key

- 获取某个分区下的键1：`key, err := cfg.Section("").GetKey("key name")`
- 获取某个分区下的键2：`key := cfg.Section("").Key("key name")`
- 判断某个键是否存在：`yes := cfg.Section("").HasKey("key name")`
- 创建新的Key：`err := cfg.Section("").NewKey("name", "value")`
- 获取分区下的所有键或键名：

```go
keys := cfg.Section("").Keys()
names := cfg.Section("").KeyStrings()
```

#### 忽略分区或键名大小写
`cfg, err := ini.InsensitiveLoad("filename")`

#### 同一个键名包含多个值
普通情况下：只有最后一次出现的值会被保存到url中
需要保留所有值：
```go
cfg, err := ini.ShadowLoad(".gitconfig")

f.Section(`remote "origin"`).Key("url").String() 
# Result: https://github.com/Antergone/test2.git

f.Section(`remote "origin"`).Key("url").ValueWithShadows()
//  Result:  []string{
//             "https://github.com/Antergone/test1.git",
//               "https://github.com/Antergone/test2.git",
//           }
```
####  自增键名
如果数据源中的键名为 -，则认为该键使用了自增键名的特殊语法。计数器从 1 开始，并且分区之间是相互独立的
`cfg.Section("features").KeyStrings()    // []{"#1", "#2", "#3"}`
#### 获取父分区下的所有键名
`cfg.Section("package.sub").ParentKeys() // ["CLONE_URL"]`

### 操作键值Value
- 获取key的值:`al := cfg.Section("").Key("key name").String()`
- 获取原值：`val := cfg.Section("").Key("key name").Value()`
- 判断某个原值是否存在：`yes := cfg.Section("").HasValue("test value")`
#### Value布尔值的规则：
结果为true：为：1, t, T, TRUE, true, True, YES, yes, Yes, y, ON, on, On
结果为false 为：0, f, F, FALSE, false, False, NO, no, No, n, OFF, off, Off
#### Must开头的方法
由 Must 开头的方法名允许接收一个相同类型的参数来作为默认值，
当键不存在或者转换失败时，则会直接返回该默认值。但是，MustXXXX方法必须传递一个默认值。
```go
v = cfg.Section("").Key("INT").MustInt(10)
```
#### 多行书写
可以使用\分隔
`cfg.Section("advance").Key("two_lines").String() `获取到的是一个不换行的字符串

#### 自动处理特殊字符
具体概念：值使用双引号括起来，内部的双引号被转义
案例：create_repo="created repository <a href=\"%s\">%s</a>"
```go
cfg, err := ini.LoadSources(ini.LoadOptions{UnescapeValueDoubleQuotes: true}, "en-US.ini")
cfg.Section("<name of your section>").Key("create_repo").String()
// 结果：created repository <a href="%s">%s</a>
```
#### 辅助方法
- 设置默认值,不在给定的值内就设置为默认值
`v = cfg.Section("").Key("STRING").In("default", []string{"str", "arr", "types"})`
- 判断获取的值是否在指定范围内,第一个参数为默认值，第二个参数和第三个参数为范围
`vals = cfg.Section("").Key("FLOAT64").RangeFloat64(0.0, 1.1, 2.2)`
- 自动分割键值到切片
    - 存在无效输入的的时候，使用零值代替
```go
// Input: 1.1, 2.2, 3.3, 4.4 -> [1.1 2.2 3.3 4.4]
// Input: how, 2.2, are, you -> [0.0 2.2 0.0 0.0]
vals = cfg.Section("").Key("STRINGS").Strings(",")
vals = cfg.Section("").Key("FLOAT64S").Float64s(",")
```
    -  去除无效输入
```go
// Input: 1.1, 2.2, 3.3, 4.4 -> [1.1 2.2 3.3 4.4]
// Input: how, 2.2, are, you -> [2.2]
vals = cfg.Section("").Key("FLOAT64S").ValidFloat64s(",")
```
    - 存在无效输入时，直接返回错误
```go
// Input: 1.1, 2.2, 3.3, 4.4 -> [1.1 2.2 3.3 4.4]
// Input: how, 2.2, are, you -> error
vals = cfg.Section("").Key("FLOAT64S").StrictFloat64s(",")
```
- 递归读取键值
语法：` %(<name>)s`， 其中name只能是相同分区或默认分区下的键名，如果指定的键不存在，则会用空字符串替代
```go
NAME = ini

[author]
NAME = Unknwon
GITHUB = https://github.com/%(NAME)s

[package]
FULL_NAME = github.com/go-ini/%(NAME)s
// cfg.Section("author").Key("GITHUB").String()：https://github.com/Unknwon
// cfg.Section("package").Key("FULL_NAME").String()：github.com/go-ini/ini
```

### 注释Comment
#### 注释分类
1. 所有以 # 或 ; 开头的行
2. 所有在 # 或 ; 之后的内容
3. 分区标签后的文字 (即 [分区名] 之后的内容)


### 结构体和分区双向映射
暂时忽略
### 自定义键名和键值映射器
暂时忽略

