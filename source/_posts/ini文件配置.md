---
title: ini文件配置
date: 2023-03-19 23:08:10
tags: [golang, package，ini]
categories: GoLang
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