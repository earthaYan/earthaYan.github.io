---
title: 配置解析Viper
date: 2023-02-16 23:46:45
tags: [GoLang,Viper]
categories: GoLang
---

作用：加载并解析配置文件，将这些配置信息保存在配置文件中，由程序启动时加载和解析
## 目前配置解析主流途径：
- 小项目：配置少，通过命令行参数即可
- 大型项目：配置多，通过命令行参数传递难以维护

从不同位置读取配置,位置不同，优先级也不。高优先级的配置会覆盖低优先级中`相同`的配置
优先级排列：
>-   通过 viper.Set 函数显示设置的配置[不区分大小写]
>-   命令行参数
>-   环境变量
>-   配置文件
>-   Key/Value 
>-   存储默认值

---
## 读入配置
定义：将配置读入到Viper中，读入方式如下
-   设置默认的配置文件名
-   读取配置文件。
-   监听和重新读取配置文件。
-   从 io.Reader 读取配置。
-   从环境变量读取。
-   从命令行标志读取。
-   从远程 Key/Value 存储读取。

### 设置默认值
让程序在没有明确指定配置时也能够正常运行
```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```

### 读取配置文件
读取配置文件(JSON/TOML/YAML/YML/Properties/Props/Prop/HCL/Dotenv/Env)

```go
// 使用 Viper 搜索和读取配置文件
import (
  "fmt"
  "github.com/spf13/pflag"
  "github.com/spf13/viper"
)
var (
  cfg  = pflag.StringP("config", "c", "", "Configuration file.")
  help = pflag.BoolP("help", "h", false, "Show this help message.")
)
func main() {
  pflag.Parse()
  if *help {
    pflag.Usage()
    return
  }
  // 从配置文件中读取配置
  if *cfg != "" {
     // 指定配置文件名
    viper.SetConfigFile(*cfg) 
    // 如果配置文件名中没有文件扩展名，则需要指定配置文件的格式，告诉viper以何种格式解析文件 
    viper.SetConfigType("yaml") 
  } else {
    // 把当前目录加入到配置文件的搜索路径中
    viper.AddConfigPath(".") 
    // 设置配置文件搜索路径，可以设置多个配置文件搜索路径         
    viper.AddConfigPath("$HOME/.iam") 
    // 设置配置文件名称（没有文件扩展名）
    viper.SetConfigName("config")     
  }
   // 读取配置文件。如果指定了配置文件名，则使用指定的配置文件，否则在注册的搜索路径中搜索
  if err := viper.ReadInConfig(); err != nil {
    panic(fmt.Errorf("Fatal error config file: %s \n", err))
  }
  fmt.Printf("Used configuration file is: %s\n", viper.ConfigFileUsed())
}
```
### 监听和重新读取配置文件
```go
// 热加载配置[不推荐]
// 确保已经添加了配置文件的搜索路径
viper.WatchConfig()
// 在每次发生更改时运行
viper.OnConfigChange(func(e fsnotify.Event) {
   // 配置文件发生变更之后会调用的回调函数
  fmt.Println("Config file changed:", e.Name)
})
```

### 设置配置值
```go
viper.Set("user.username", "colin")
```
### 使用环境变量[区分大小写]
- AutomaticEnv()
- BindEnv(input ...string  键名，环境变量名称【默认`环境变量前缀_键名全大写`】) error
- SetEnvPrefix(in string)
- SetEnvKeyReplace(r *string.Replacer):重写 Env 键
`viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_", "-", "_"))`//用 _ 替换.和-
- AllowEmptyEnv(allowEmptyEnv bool)

【注意】：设置了 viper.SetEnvPrefix(“VIPER”)，则viper.Get(“apiversion”) 读取的环境变量是VIPER_APIVERSION

### 使用标志
绑定 key 到 Flag
```go
viper.BindPFlag("token", pflag.Lookup("token")) // 绑定单个标志
viper.BindPFlags(pflag.CommandLine)             //绑定标志集
```

## 读取配置
> 每一个 Get 方法在找不到值的时候都会返回零值
Get(key string) interface{}
Get<Type>(key string) <Type>：Type->Bool、Float64、Int、IntSlice、String、StringMap、StringMapString、StringSlice、Time、Duration

AllSettings() map[string]interface{}
IsSet(key string) : bool->检查给定的键是否存在

### 访问嵌套的键
<!-- 加载JSON文件:a.json -->
```json

{
    // 如果存在与分隔的键路径匹配的键，则直接返回其值
    "datastore.metric.host": "0.0.0.0",
    "host": {
        "address": "localhost",
        "port": 5799
    },
    "datastore": {
        "metric": {
            "host": "127.0.0.1",
            "port": 3099
        },
        "warehouse": {
            "host": "198.0.0.1",
            "port": 2112
        }
    }
}
```
```go
viper.GetString("datastore.metric.host") // (返回 "127.0.0.1")
```
### 反序列化
将所有或特定的值解析到结构体、map 
- Unmarshal(rawVal interface{}) error
- UnmarshalKey(key string, rawVal interface{}) error
```go
type config struct {
  Chart struct{
        Values map[string]interface{}
    }
}
var C config
v.Unmarshal(&C)
```
### 序列化成字符串
`yaml.Marshal`
```go

import (
    yaml "gopkg.in/yaml.v2"
    // ...
)

func yamlStringSettings() string {
    c := viper.AllSettings()
    bs, err := yaml.Marshal(c)
    if err != nil {
        log.Fatalf("unable to marshal config to YAML: %v", err)
    }
    return string(bs)
}
```