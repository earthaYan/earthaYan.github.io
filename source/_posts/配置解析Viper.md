---
title: 配置解析Viper
date: 2023-05-18 23:46:45
tags: [GoLang,Viper]
categories: GoLang
---


## 安装
`go get github.com/spf13/viper`
## 作用
一个完整的配置解决方案，满足应用配置需求的注册表
1. 设置默认值
2. 从JSON,TOML,YAML,HCL,INI,环境文件和Java Properties配置文件中读取配置
3. 实时监听和重新读取配置文件
4. 从环境变量中读取配置
5. 从远程配置系统（etcd或Consul）中读取配置并监听变化
6. 从命令行flag中读取配置
7. 从buffer中读取配置
8. 设置显式值
### 好处
让开发者专注于构建应用，而不用担心配置文件形式
1. 寻找，加载和解析（unmarshal）配置文件
2. 为不同的配置项提供默认值设置机制
3. 为命令行flag中指定的选项值提供覆盖值设置机制
4. 在不破坏代码的情况下，提供别名系统方便对参数重命名
5. 轻松区分用户提供的命令行或配置文件和默认值相同的情况

### 优先顺序
1. 显示调用`Set`
2. flag
3. env
4. config
5. key/value存储：key不区分大小写
6. 默认值

## 将values放入Viper
### 建立默认值
```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```
### 读取配置文件
Viper可以搜索多个path，但是当下一个viper示例只能支持一个配置文件。
如何搜索和读取一个配置文件：
```go
// 配置文件的名称（无扩展名）
viper.SetConfigName("config")
// 如果配置文件名中没有扩展名，则需要设置Type
viper.SetConfigType("yaml")
// 在这个路径中寻找配置文件
viper.AddConfigPath("/etc/appName/")
// 多次调用来添加搜索路径
viper.AddConfigPath("$HOME/.appName")
// 可选,在当前工作目录中寻找配置
viper.AddConfigPath(".")
// 找到并读取配置文件
err := viper.ReadInConfig()
// 处理读取配置文件时候发生的错误
if err != nil {
  panic(fmt.Errorf("fatal error config file: %w", err))
}
```
处理没有配置文件的指定情况
```go
// 处理读取配置文件时候发生的错误
if err != nil {
  if _, ok := err.(viper.ConfigFileNotFoundError); ok {
    // 配置文件未找到，如果需要的话可以忽略错误
  } else {
    // 配置文件找到但是出现了其他问题
    panic(fmt.Errorf("fatal error config file: %w", err))
  }
}
// 配置文件找到并成功解析
```

### 编写配置文件
作用：存储运行期间的所有修改
- WriteConfig:
  - 将当前的viper配置写入已经存在的预定义的path,如果不存在预定义路径则报错
  - 如果当前已存在配置文件，则覆盖当前配置
- SafeWriteConfig:
  - 将当前的viper配置写入已经存在的预定义的path,如果不存在预定义路径则报错
  - 如果当前已存在配置文件，不会覆盖当前的配置文件
- WriteConfigAs:
  - 将当前的viper配置写入给定的文件
  - 如果已经存在，会覆盖当前的给定的文件
- SafeWriteConfigAs:
  - 将当前的viper配置写入给定的文件
  - 如果已经存在，不会覆盖当前的给定的文件

```go
	// 将当前配置写入由viper.AddConfigPath()和viper.SetConfigName()设置的预定义路径
	viper.WriteConfig()
	viper.SafeWriteConfig()
	viper.WriteConfigAs("/path/to/my/.config")
	//由于它已经存在并被写入，所以会报错
	viper.SafeWriteConfigAs("/path/to/my/.config")
	viper.SafeWriteConfigAs("/path/to/my/.other_config")
```

### 监听和重新读取配置文件
当应用运行时，实时读取配置文件
前提：确保在调用WatchConfig() 之前已经添加好所有配置路径
```go
viper.OnConfigChange(func(e fsnotify.Event) {
  fmt.Println("config file changed:", e.Name)
})
viper.WatchConfig()
```
### 从io.Reader中读取配置
可以实现自己需要的配置源并且传给viper，不局限于上述提到的一些形式
```go
	var yamlExample = []byte(`
		Hacker: true
		name: steve
		hobbies:
		- skateboarding
		- snowboarding
		- go
		clothing:
		jacket: leather
		trousers: denim
		age: 35
		eyes : brown
		beard: true
	`)
	viper.ReadConfig(bytes.NewBuffer(yamlExample))
	// 结果是"steve"
	viper.Get("name")
```

### 设置重写覆盖
这些可以来自于一个命令行flag或者自己的应用逻辑
```go
viper.Set("Verbose", true)
viper.Set("LogFile", LogFile)
```

### 注册和使用别名
一个value对应多个key的引用
```go
viper.RegisterAlias("loud", "Verbose")
viper.Set("verbose", true)
viper.Set("loud", true) // 和上一行执行结果一样

viper.GetBool("loud")    // true
viper.GetBool("verbose") // true
```

### 使用环境变量
环境变量名称区分大小写
#### `BindEnv(string...) : error`
- 第一个参数是key名，剩下的参数是将要绑定这个key的环境变量名称。
- 如果有多个环境变量则以指定的顺序排优先级。
- 如果没有提供环境变量名称，则默认为全部大写的` prefix_${key名}`
- 如果显示提供了一个环境变量名称，则不会自动添加前缀。例如第二个参数是id，viper会认为它是ID
- 每次访问时都会读取该值。调用 BindEnv 时，Viper不会固定该值
#### `SetEnvPrefix(string)`
告诉viper，当从环境变量中读取配置时使用前缀，而`BindEnv`和`AutomaticEnv`都将使用这个前缀
#### `AutomaticEnv()`
配合`SetEnvPrefix`使用十分高效
- 每当调用时，只要`viper.Get`发出请求，viper就会检查一个环境变量
- 检查名称是否符合key大写的规则，当设置了`EnvPrefix`时，是否添加了前缀
#### `SetEnvKeyReplacer(string...) *strings.Replacer`
允许你一定程度上使用`strings.Replacer`对象重写Env Key
#### `AllowEmptyEnv(bool)`
处理空环境变量
```go
// 会自动转换为大写
viper.SetEnvPrefix("spf")
viper.BindEnv("id")
// 通常在应用外完成
os.Setenv("SPF_ID", "13")
id := viper.Get("id")
```
### 使用Flags
viper可以绑定到flag,支持Cobra库中使用的 `pflag`
#### 单个flag`BindPFlag`
```go
serverCmd.Flags().Int("port", 1138, "Port to run Application server on")
viper.BindPFlag("port", serverCmd.Flags().Lookup("port"))
```
#### 已存在的pflag set
```go
pflag.Int("flagname", 1234, "help message for flagname")
pflag.Parse()
viper.BindPFlags(pflag.CommandLine)
i := viper.GetInt("flagname") // 从viper而不是从pflag中恢复值
```
