---
title: 配置解析Viper
date: 2023-05-18 23:46:45
tags: [GoLang]
categories: 后端
---

## 安装

`go get github.com/spf13/viper`

## 作用
简言之：用于读取配置。它支持将配置从多种不同的源加载到一个应用程序
一个完整的配置解决方案，满足应用配置需求的注册表
1. 设置默认值
2. 从 JSON,TOML,YAML,HCL,INI,环境文件和 Java Properties 配置文件中读取配置
3. 实时监听和重新读取配置文件
4. 从环境变量中读取配置
5. 从远程配置系统（etcd 或 Consul）中读取配置并监听变化
6. 从命令行 flag 中读取配置
7. 从 buffer 中读取配置
8. 设置显式值

### 好处

让开发者专注于构建应用，而不用担心配置文件形式

1. 寻找，加载和解析（unmarshal）配置文件
2. 为不同的配置项提供默认值设置机制
3. 为命令行 flag 中指定的选项值提供覆盖值设置机制
4. 在不破坏代码的情况下，提供别名系统方便对参数重命名
5. 轻松区分用户提供的命令行或配置文件和默认值相同的情况

### 优先顺序

1. 显示调用`Set`
2. flag
3. env
4. config
5. key/value 存储：key 不区分大小写
6. 默认值

## 将 values 放入 Viper

### 建立默认值

```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```

### 读取配置文件

Viper 可以搜索多个 path，但是当下一个 viper 示例只能支持一个配置文件。
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
  - 将当前的 viper 配置写入已经存在的预定义的 path,如果不存在预定义路径则报错
  - 如果当前已存在配置文件，则覆盖当前配置
- SafeWriteConfig:
  - 将当前的 viper 配置写入已经存在的预定义的 path,如果不存在预定义路径则报错
  - 如果当前已存在配置文件，不会覆盖当前的配置文件
- WriteConfigAs:
  - 将当前的 viper 配置写入给定的文件
  - 如果已经存在，会覆盖当前的给定的文件
- SafeWriteConfigAs:
  - 将当前的 viper 配置写入给定的文件
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
前提：确保在调用 WatchConfig() 之前已经添加好所有配置路径

```go
viper.OnConfigChange(func(e fsnotify.Event) {
  fmt.Println("config file changed:", e.Name)
})
viper.WatchConfig()
```

### 从 io.Reader 中读取配置

可以实现自己需要的配置源并且传给 viper，不局限于上述提到的一些形式

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

这些可以来自于一个命令行 flag 或者自己的应用逻辑

```go
viper.Set("Verbose", true)
viper.Set("LogFile", LogFile)
```

### 注册和使用别名

一个 value 对应多个 key 的引用

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

- 第一个参数是 key 名，剩下的参数是将要绑定这个 key 的环境变量名称。
- 如果有多个环境变量则以指定的顺序排优先级。
- 如果没有提供环境变量名称，则默认为全部大写的` prefix_${key名}`
- 如果显示提供了一个环境变量名称，则不会自动添加前缀。例如第二个参数是 id，viper 会认为它是 ID
- 每次访问时都会读取该值。调用 BindEnv 时，Viper 不会固定该值

#### `SetEnvPrefix(string)`

告诉 viper，当从环境变量中读取配置时使用前缀，而`BindEnv`和`AutomaticEnv`都将使用这个前缀

#### `AutomaticEnv()`

配合`SetEnvPrefix`使用十分高效

- 每当调用时，只要`viper.Get`发出请求，viper 就会检查一个环境变量
- 检查名称是否符合 key 大写的规则，当设置了`EnvPrefix`时，是否添加了前缀

#### `SetEnvKeyReplacer(string...) *strings.Replacer`

允许你一定程度上使用`strings.Replacer`对象重写 Env Key

#### `AllowEmptyEnv(bool)`

处理空环境变量,默认是 unset，会到下一个配置文件。这个方法会设置该环境变量为已 set 状态

```go
// 会自动转换为大写
viper.SetEnvPrefix("spf")
viper.BindEnv("id")
// 通常在应用外完成
os.Setenv("SPF_ID", "13")
id := viper.Get("id")
```

### 使用 Flags

viper 可以绑定到 flag,支持 Cobra 库中使用的 `pflags`

#### 绑定单个 flag`BindPFlag`

```go
serverCmd.Flags().Int("port", 1138, "Port to run Application server on")
viper.BindPFlag("port", serverCmd.Flags().Lookup("port"))
```

#### 绑定 pflag set`BindPFlags`

```go
pflag.Int("flagName", 1234, "help message for flagName")
pflag.Parse()
viper.BindPFlags(pflag.CommandLine)
i := viper.GetInt("flagName") // 从viper而不是从pflag中恢复值
```

#### 兼容性

pflag 库与标准库 flag 包兼容。通过调用 `pflag.AddGoFlagSet()`可以将使用 flag 包定义的标志导入 pflag

```go
// 标准库flag
flag.Int("flagName", 1234, "help message for flagName")
// 加入pflag
pflag.CommandLine.AddGoFlagSet(flag.CommandLine)
pflag.Parse()
viper.BindPFlags(pflag.CommandLine)
// 从viper中获取值
i := viper.GetInt("flagName")
```

### 远程读取 key/value 存储

例如：etcd,Consul

- 引入`viper/remote`包
  `import _ "github.com/spf13/viper/remote"`
- 使用 `AddRemoteProvider()`注册特定提供程序
  `viper.AddRemoteProvider("etcd"/"etcd3", "http://127.0.0.1:4001","/config/hugo.json")`
- 使用 `Get()` 或类似方法使用提供程序前缀获取值
  `viper.Get("etcd.key")`
- 调用 WatchRemoteConfig()来启用更改监视(非必须)
  `viper.WatchRemoteConfig()`

#### 未加密

1. etcd/etcd3

```go
viper.AddRemoteProvider("etcd"/"etcd3", "http://127.0.0.1:4001","/config/hugo.json")
// 字节流中没有扩展名，
viper.SetConfigType("json")
err := viper.ReadRemoteConfig()
```

---

2. 集成 consul 和 viper

- 在 Consul 中设置一个密钥,其 JSON 值包含想要的配置

```json
{
  "port": 8080,
  "hostname": "HostName.com"
}
```

- viper 中设置

```go
viper.AddRemoteProvider("consul", "localhost:8500", "MY_CONSUL_KEY")
// 需要显式设置为json格式
viper.SetConfigType("json")
err:=viper.ReadRemoteConfig()
fmt.Println(viper.Get("port")) // 8080
fmt.Println(viper.Get("hostname")) // HostName.com
```

#### 加密`SecureRemoteProvider`

```go
viper.AddSecureRemoteProvider("etcd","http://127.0.0.1:4001","/config/hugo.json","/etc/secrets/mykeyring.gpg")
viper.SetConfigType("json")
err := viper.ReadRemoteConfig()
```

#### 监听变化

`runtime_viper.WatchRemoteConfig()`

### 从 viper 获取值

- Get(key string) : interface{}
- GetBool(key string) : bool
- GetFloat64(key string) : float64
- GetInt(key string) : int
- GetIntSlice(key string) : []int
- GetString(key string) : string
- GetStringMap(key string) : map[string]interface{}
- GetStringMapString(key string) : map[string]string
- GetStringSlice(key string) : []string
- GetTime(key string) : time.Time
- GetDuration(key string) : time.Duration
- IsSet(key string) : bool
- AllSettings() : map[string]interface{}

【注】：如果未找到的会返回一个零值。检查是否存在指定 key，使用`IsSet`方法

```go
// setting 和getting不区分大小写
viper.GetString("logFile")
if viper.GetBool("verbose") {
	fmt.Println("verbose enabled")
}
```

### 访问嵌套的 key

通过`.`分隔符分割 key 的路径

```json
{
  "host": {
    "address": "localhost",
    "port": 5799
  }
}
```

GetString("host.address")的返回值为 localHost

#### 使用路径中的数字访问数组索引

```json
{
  "host": {
    "address": "localhost",
    "ports": [5799, 6029]
  }
}
```

GetInt("host.ports.1")的返回值为 5799

#### 如果存在与分隔键路径匹配的键,则会返回其值,而不是继续解析路径。

上文如果添加 key："host.address":"online"
则 GetString("host.address")返回值为 online

### 提取配置子集

场景：开发可复用模块，提取配置的子集并将其传递给模块。这样,模块可以实例化多次,具有不同的配置

```go
// 使用viper.Sub()创建配置子集
// cache1Config 是一个viper实例
cache1Config := viper.Sub("cache.cache1")
// 如果没有找到key会返回一个nil
if cache1Config == nil {
	panic("cache configuration not found")
}
cache1 := NewCache(cache1Config)

func NewCache(v *Viper) *Cache {
	return &Cache{
		// 获取配置值
		MaxItems: v.GetInt("max-items"),
		ItemSize: v.GetInt("item-size"),
	}
}
```

### Unmarshal 解析

目的：将 viper 的配置值解析到一个 map，struct,slice 等形式

1. `Unmarshal(rawVal interface{}) : error`
2. `UnmarshalKey(key string, rawVal interface{}) : error`

原配置：

```yaml
yaml
database:
  host: localhost
  port: 5432
  enabled: true
```

解析

```go
type DBConfig struct {
   Host string
   Port int
   Enabled bool
}
// struct
var dbConfig DBConfig
viper.Unmarshal(&dbConfig)
// 基础类型
var enabled bool
viper.UnmarshalKey("database.enabled", &enabled) //true
// map
var dbMap map[string]interface{}
viper.Unmarshal(&dbMap)
```

此时 dbConfig 的值为 struct：{Host: localhost, Port: 5432, Enabled: true}
dbMap 现在的值为 map[string]interface{}{"Host": "localhost", "Port": 5432, "Enabled": true}
enabled 的值为 true

### Marshal 序列化为字符串

```go
import (
	yaml "gopkg.in/yaml.v2"
)
settings := viper.AllSettings()
bytes, err := json.Marshal(settings)
bytes, err := yaml.Marshal(settings)
jsonStr := string(bytes)
```
