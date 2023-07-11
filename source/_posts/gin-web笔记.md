---
title: gin-web笔记
date: 2023-03-23 01:25:14
tags: [GoLang]
categories: 后端
---

## 安装

```bash
go get -u github.com/gin-gonic/gin
```

Gin 默认使用`encoding/json`进行编译

## 快捷方式：

- gin.H 是 map[string]interface{}的快捷方式
- gin.Accounts 是 map[string]string 的一种快捷方式

## AsciiJSON

使用 AsciiJSON 生成具有转义的非 ASCII 字符的 ASCII-only JSON。
原数据：

```go
data := map[string]interface{}{
  "lang": "GO语言",
  "tag":  "<br>",
}
// 输出data:{"lang":"GO\u8bed\u8a00","tag":"\u003cbr\u003e"}
c.AsciiJSON(http.StatusOK, data)
```

## html 渲染

使用`LoadHTMLGlob()`或者`LoadHTMLFiles()`

```tmpl
<!-- templates/index.tmpl -->
<html>
	<h1>
		{{ .title }}
	</h1>
</html>
<!-- templates/posts/index.tmpl -->
{{ define "posts/index.tmpl" }}
<html><h1>
	{{ .title }}
</h1>
<p>Using posts/index.tmpl</p>
</html>
{{ end }}
<!-- templates/users/index.tmpl -->
{{ define "users/index.tmpl" }}
<html><h1>
	{{ .title }}
</h1>
<p>Using users/index.tmpl</p>
</html>
{{ end }}
```

如何使用模板：

```go
	router.LoadHTMLGlob("templates/**/*")
  //router.LoadHTMLFiles("templates/template1.html", "templates/template2.html")
  // 使用不同目录下的相同名称的模板
	router.GET("/posts/index", func(c *gin.Context) {
		c.HTML(http.StatusOK, "posts/index.tmpl", gin.H{
			"title": "Posts",
		})
	})
	router.GET("/users/index", func(c *gin.Context) {
		c.HTML(http.StatusOK, "users/index.tmpl", gin.H{
			"title": "Users",
		})
	})

```

### 自定义 html 模板

暂忽略

## HTTP2 server 服务器 推送

服务器推送：还没有收到浏览器的请求，服务器就把各种资源推送给浏览器。比如，浏览器只请求了 index.html，但是服务器把 index.html、style.css、example.png 全部发送给浏览器。这样的话，只需要一轮 HTTP 通信，浏览器就得到了全部资源，提高了性能

```go
var html = template.Must(template.New("https").Parse(`
<html>
<head>
  <title>Https Test</title>
  <script src="/assets/app.js"></script>
</head>
<body>
  <h1 style="color:red;">Welcome, Ginner!</h1>
</body>
</html>
`))
r.GET("/", func(c *gin.Context) {
  if pusher := c.Writer.Pusher(); pusher != nil {
    // 使用 pusher.Push() 做服务器推送
    if err := pusher.Push("/assets/app.js", nil); err != nil {
      log.Printf("Failed to push: %v", err)
    }
  }
  c.HTML(200, "https", gin.H{
    "status": "success",
  })
})
```

## JSONP

用来解决跨域问题:如果查询参数存在回调，则将回调添加到响应体中

```go
data := map[string]interface{}{
  "foo": "bar",
}
// 请求：/JSONP?callback=x
// 输出data:x({\"foo\":\"bar\"})
c.JSONP(http.StatusOK, data)
```

## Multipart/Urlencoded 绑定

```go
type LoginForm struct {
	User     string `form:"user" binding:"required"`
	Password string `form:"password" binding:"required"`
}
// 显式绑定声明绑定multipart form：
c.ShouldBindWith(&form, binding.Form)
// 使用ShouldBind 方法自动绑定
var form LoginForm
if c.ShouldBind(&form) == nil {
  if form.User == "user" && form.Password == "password" {
    c.JSON(200, gin.H{"status": "you are logged in"})
  } else {
    c.JSON(401, gin.H{"status": "unauthorized"})
  }
}
// curl测试
// curl -v --form user=user --form password=password http://localhost:8080/login
```

## Multipart/Urlencoded 表单

```go
	router.POST("/form_post", func(c *gin.Context) {
		message := c.PostForm("message")
		nick := c.DefaultPostForm("nick", "anonymous")
		c.JSON(200, gin.H{
			"status":  "posted",
			"message": message,
			"nick":    nick,
		})
	})
```

## 对特殊 HTML 字符进行编码——PureJSON

JSON 使用 unicode 替换特殊 HTML 字符，例如 < 变为 \ u003c。如果要按字面对这些字符进行编码，则可以使用 PureJSON

```go
// 提供 unicode 实体
r.GET("/json", func(c *gin.Context) {
  c.JSON(200, gin.H{
    "html": "<b>Hello, world!</b>",
  })
})
// 提供字面字符
r.GET("/pureJson", func(c *gin.Context) {
  c.PureJSON(200, gin.H{
    "html": "<b>Hello, world!</b>",
  })
})
```

## Query 和 post form

请求如下：

> POST /post?id=1234&page=1 HTTP/1.1
> Content-Type: application/x-www-form-urlencoded
> name=mau&message=this_is_great

```go
id := c.Query("id")
page := c.DefaultQuery("page", "0")
name := c.PostForm("name")
message := c.PostForm("message")
fmt.Printf("id: %s; page: %s; name: %s; message: %s", id, page, name, message)
// 结果：id: 1234; page: 1; name: mau; message: this_is_great
```

## 防止 JSON 劫持——SecureJSON

如果给定的结构是数组值，则默认预置 "while(1)," 到响应体

```go
names := []string{"lena", "austin", "foo"}
// 自定义SecureJSON 前缀
r.SecureJsonPrefix(")]}',\n")
// 结果：while(1);["lena","austin","foo"]
c.SecureJSON(http.StatusOK, names)
```

## XML/JSON/YAML/ProtoBuf 渲染

```go
// JSON
r.GET("/someJSON", func(c *gin.Context) {
  c.JSON(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})
// JSON-使用结构体
r.GET("/moreJSON", func(c *gin.Context) {
  // 你也可以使用一个结构体
  var msg struct {
    Name    string `json:"user"`
    Message string
    Number  int
  }
  msg.Name = "Lena"
  msg.Message = "hey"
  msg.Number = 123
  // 输出：{"user": "Lena", "Message": "hey", "Number": 123}
  c.JSON(http.StatusOK, msg)
})
// XML
r.GET("/someXML", func(c *gin.Context) {
  c.XML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})
// Yaml
r.GET("/someYAML", func(c *gin.Context) {
  c.YAML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
})
// ProtoBuf
r.GET("/someProtoBuf", func(c *gin.Context) {
  reps := []int64{int64(1), int64(2)}
  label := "test"
  // protobuf 的具体定义写在 testdata/protoexample 文件中
  data := &protoexample.Test{
    Label: &label,
    Reps:  reps,
  }
  // 数据在响应中变为二进制数据
  // 将输出被 protoexample.Test protobuf 序列化了的数据
  c.ProtoBuf(http.StatusOK, data)
})
```

## 上传文件

### 单文件

```go
// 为 multipart forms 设置较低的内存限制 (默认是 32 MiB)
router.MaxMultipartMemory = 8 << 20  // 8 MiB,8右移20位
router.POST("/upload", func(c *gin.Context) {
  // 单文件
  file, _ := c.FormFile("file")
  log.Println(file.Filename)
  dst := "./" + file.Filename
  // 上传文件至指定的完整文件路径
  c.SaveUploadedFile(file, dst)
  c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
})
//curl -X POST http://localhost:8080/upload \
// -F "file=@/Users/appleboy/test.zip" \
// -H "Content-Type: multipart/form-data"
```

### 多文件

```go
router.POST("/upload", func(c *gin.Context) {
  // Multipart form
  form, _ := c.MultipartForm()
  files := form.File["upload[]"]
  for _, file := range files {
    log.Println(file.Filename)
    // 上传文件至指定目录
    c.SaveUploadedFile(file, dst)
  }
  c.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))
})
// curl -X POST http://localhost:8080/upload \
//   -F "upload[]=@/Users/appleboy/test1.zip" \
//   -F "upload[]=@/Users/appleboy/test2.zip" \
//   -H "Content-Type: multipart/form-data"
```

## 不使用默认的中间件

gin.Default()默认使用 Logger 和 Recovery 中间件
gin.New()可以用于不需要使用默认的中间件的场景下

## 从 reader 读取数据

```go
response, err := http.Get("https://raw.githubusercontent.com/gin-gonic/logo/master/color.png")
if err != nil || response.StatusCode != http.StatusOK {
  c.Status(http.StatusServiceUnavailable)
  return
}
reader := response.Body
contentLength := response.ContentLength
contentType := response.Header.Get("Content-Type")
extraHeaders := map[string]string{
  "Content-Disposition": `attachment; filename="gopher.png"`,
}
c.DataFromReader(http.StatusOK, contentLength, contentType, reader, extraHeaders)
```

## 重启或停止 web 服务器

使用`fvbock/endless`代替`ListenAndServe`

```go
router := gin.Default()
router.GET("/", handler)
// [...]
endless.ListenAndServe(":4242", router)
```

## 使用 BasicAuth 中间件

gin.BasicAuth() 中间件

```go
var secrets = gin.H{
	"foo":    gin.H{"email": "foo@bar.com", "phone": "123433"},
	"austin": gin.H{"email": "austin@example.com", "phone": "666"},
	"lena":   gin.H{"email": "lena@guapa.com", "phone": "523443"},
}
authorized := r.Group("/admin", gin.BasicAuth(gin.Accounts{
 "foo":    "bar",
 "austin": "1234",
 "lena":   "hello2",
 "manu":   "4321",
}))

// /admin/secrets 端点
// 触发 "localhost:8080/admin/secrets
authorized.GET("/secrets", func(c *gin.Context) {
  // 获取用户，它是由 BasicAuth 中间件设置的
  user := c.MustGet(gin.AuthUserKey).(string)
  if secret, ok := secrets[user]; ok {
    c.JSON(http.StatusOK, gin.H{"user": user, "secret": secret})
  } else {
    c.JSON(http.StatusOK, gin.H{"user": user, "secret": "NO SECRET :("})
  }
})
```

## 使用 http 方法

```go
	// 使用默认中间件（logger 和 recovery 中间件）创建 gin 路由
	router := gin.Default()
	router.GET("/someGet", getting)
	router.POST("/somePost", posting)
	router.PUT("/somePut", putting)
	router.DELETE("/someDelete", deleting)
	router.PATCH("/somePatch", patching)
	router.HEAD("/someHead", head)
	router.OPTIONS("/someOptions", options)
	// 默认在 8080 端口启动服务，除非定义了一个 PORT 的环境变量。
	router.Run()
```

## 使用中间件

```go
// Logger 中间件将日志写入 gin.DefaultWriter，
r.Use(gin.Logger())
// Recovery 中间件会 recover 任何 panic。如果有 panic 的话，会写入 500。
r.Use(gin.Recovery())
// 可以为每个路由添加任意数量的中间件。
r.GET("/benchmark", MyBenchLogger(), benchEndpoint)
```

### 路由组

```go
authorized := r.Group("/", AuthRequired())
{
  authorized.POST("/login", loginEndpoint)
  authorized.POST("/submit", submitEndpoint)
  authorized.POST("/read", readEndpoint)
  // 嵌套路由组
  testing := authorized.Group("testing")
  testing.GET("/analytics", analyticsEndpoint)
}
```

同下面的完全一样

```go
authorized := r.Group("/")
authorized.Use(AuthRequired())
{
  authorized.POST("/login", loginEndpoint)
  authorized.POST("/submit", submitEndpoint)
  authorized.POST("/read", readEndpoint)
}
```

## 只绑定 url 查询字符串

只绑定 url 查询参数，而忽略 post 参数：`ShouldBindQuery`

```go
type Person struct {
	Name    string `form:"name"`
	Address string `form:"address"`
}
route.PUT("/testing", startPage)
func startPage(c *gin.Context) {
	var person Person
	if c.ShouldBindQuery(&person) == nil {
		log.Println("====== Only Bind By Query String ======")
		log.Println(person.Name)
		log.Println(person.Address)
	}
	c.String(200, "Success")
}
```

## 在中间件使用 go routine

当在中间件或 handler 中启动新的 Goroutine 时，不能使用原始的上下文，必须使用只读副本。

```go
r.GET("/long_async", func(c *gin.Context) {
  // 创建在 goroutine 中使用的副本
  cCp := c.Copy()
  go func() {
    // 用 time.Sleep() 模拟一个长任务。
    time.Sleep(5 * time.Second)
    // 使用的是复制的上下文 "cCp"，这一点很重要
    log.Println("Done! in path " + cCp.Request.URL.Path)
  }()
})
r.GET("/long_sync", func(c *gin.Context) {
  // 用 time.Sleep() 模拟一个长任务。
  time.Sleep(5 * time.Second)
  // 因为没有使用 goroutine，不需要使用上下文副本
  log.Println("Done! in path " + c.Request.URL.Path)
})
```

## 记录日志

```go
// 只将日志写入文件
f, _ := os.Create("gin.log")
gin.DefaultWriter = io.MultiWriter(f)
// 需要同时将日志写入文件和控制台
gin.DefaultWriter = io.MultiWriter(f, os.Stdout)
```

## 定义路由日志的格式

默认的路由日志格式

```bash
[GIN-debug] POST   /foo                      --> main.main.func1 (3 handlers)
[GIN-debug] GET    /bar                      --> main.main.func2 (3 handlers)
[GIN-debug] GET    /status                   --> main.main.func3 (3 handlers)
```

自定义日志格式：JSON，key-value 等->`gin.DebugPrintRouteFunc`

```go
gin.DebugPrintRouteFunc = func(httpMethod, absolutePath, handlerName string, nuHandlers int) {
  log.Printf("endpoint %v %v %v %v\n", httpMethod, absolutePath, handlerName, nuHandlers)
}
```

## 将 request body 绑定到不同的结构体中

`c.ShouldBind`通过`c.Request.Body`绑定数据，但是在部分格式不能多次调用：

- JSON
- XML
- MsgPack
- ProtoBuf
  如果需要多次绑定到不同结构体,需要使用`c.ShouldBindBodyWith`
  可以多次调用`c.ShouldBind`的格式：
- Query
- Form
- FormPost
- FormMultipart

```go
type formA struct {
  Foo string `json:"foo" xml:"foo" binding:"required"`
}
type formB struct {
  Bar string `json:"bar" xml:"bar" binding:"required"`
}
func SomeHandler(c *gin.Context) {
  objA := formA{}
  objB := formB{}
  // c.ShouldBind 使用了 c.Request.Body，不可重用。
  if errA := c.ShouldBind(&objA); errA == nil {
    c.String(http.StatusOK, `the body should be formA`)
  // 因为现在 c.Request.Body 是 EOF，所以这里会报错。
  } else if errB := c.ShouldBind(&objB); errB == nil {
    c.String(http.StatusOK, `the body should be formB`)
  }
}
// 读取 c.Request.Body 并将结果存入上下文。
if errA := c.ShouldBindBodyWith(&objA, binding.JSON); errA == nil {
  c.String(http.StatusOK, `the body should be formA`)
// 这时, 复用存储在上下文中的 body。
} else if errB := c.ShouldBindBodyWith(&objB, binding.JSON); errB == nil {
  c.String(http.StatusOK, `the body should be formB JSON`)
// 可以接受其他格式
} else if errB2 := c.ShouldBindBodyWith(&objB, binding.XML); errB2 == nil {
  c.String(http.StatusOK, `the body should be formB XML`)
}
```

## 控制日志输出颜色

输出到控制台的日志默认是有颜色的

```go
// 禁止日志的颜色
gin.DisableConsoleColor()
// 强制日志颜色化
gin.ForceConsoleColor()
```

## 映射查询字符串或表单参数

```bash
POST /post?ids[a]=1234&ids[b]=hello HTTP/1.1
Content-Type: application/x-www-form-urlencoded

names[first]=thinkerou&names[second]=tianou
```

```go
ids := c.QueryMap("ids")
names := c.PostFormMap("names")
fmt.Printf("ids: %v; names: %v", ids, names)

// query参数——ids: map[b:hello a:1234],
// 表单参数——names: map[second:tianou first:thinkerou]

```

## 查询字符串参数

// 使用现有的基础请求对象解析查询字符串参数。
示例 URL： /welcome?firstname=Jane&lastname=Doe

```go
router.GET("/welcome", func(c *gin.Context) {
  firstname := c.DefaultQuery("firstname", "Guest")
  lastname := c.Query("lastname") // c.Request.URL.Query().Get("lastname") 的一种快捷方式

  c.String(http.StatusOK, "Hello %s %s", firstname, lastname)
})
```

## model binding 绑定和验证

在绑定的所有字段上，设置相应的 tag，比如使用 json 绑定的时候，设置字段标签为 `json:"filename"`
方法：ShouldBind, ShouldBindJSON, ShouldBindXML, ShouldBindQuery, ShouldBindYAML
行为： 如果发生绑定错误，Gin 会返回错误并由开发者处理错误和请求。

```go
type Login struct {
	User     string `form:"user" json:"user" xml:"user"  binding:"required"`
	Password string `form:"password" json:"password" xml:"password" binding:"required"`
}
// 绑定 JSON ({"user": "manu", "password": "123"})
router.POST("/loginJSON", func(c *gin.Context) {
  var json Login
  if err := c.ShouldBindJSON(&json); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }

  if json.User != "manu" || json.Password != "123" {
    c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
    return
  }

  c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
})
// 绑定XML
//	<?xml version="1.0" encoding="UTF-8"?>
//	<root>
//		<user>manu</user>
//		<password>123</password>
//	</root>)
router.POST("/loginXML", func(c *gin.Context) {
  var xml Login
  if err := c.ShouldBindXML(&xml); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }

  if xml.User != "manu" || xml.Password != "123" {
    c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
    return
  }

  c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
})
// 绑定 HTML 表单 (user=manu&password=123)
router.POST("/loginForm", func(c *gin.Context) {
  var form Login
  // 根据 Content-Type Header 推断使用哪个绑定器。
  if err := c.ShouldBind(&form); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }
  if form.User != "manu" || form.Password != "123" {
    c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
    return
  }
  c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
})
```

## 绑定 uri

```go
type Person struct {
	ID   string `uri:"id" binding:"required,uuid"`
	Name string `uri:"name" binding:"required"`
}
route.GET("/:name/:id", func(c *gin.Context) {
  var person Person
  if err := c.ShouldBindUri(&person); err != nil {
    c.JSON(400, gin.H{"msg": err.Error()})
    return
  }
  c.JSON(200, gin.H{"name": person.Name, "uuid": person.ID})
})
```

## 绑定查询字符串或者表单数据

```go

type Person struct {
	Name     string    `form:"name"`
	Address  string    `form:"address"`
	Birthday time.Time `form:"birthday" time_format:"2006-01-02" time_utc:"1"`
}
route.GET("/testing", startPage)
func startPage(c *gin.Context) {
	var person Person
	// 如果是 `GET` 请求，只使用 `Form` 绑定引擎（`query`）。
	// 如果是 `POST` 请求，首先检查 `content-type` 是否为 `JSON` 或 `XML`，然后再使用 `Form`（`form-data`）。
	// 查看更多：https://github.com/gin-gonic/gin/blob/master/binding/binding.go#L88
	if c.ShouldBind(&person) == nil {
		log.Println(person.Name)
		log.Println(person.Address)
		log.Println(person.Birthday)
	}

	c.String(200, "Success")
}
```

## 绑定表单数据到自定义 struct

不支持嵌套的 struct

```go
type StructA struct {
    FieldA string `form:"field_a"`
}

type StructB struct {
    NestedStruct StructA
    FieldB string `form:"field_b"`
}
func GetDataB(c *gin.Context) {
  var b StructB
  c.Bind(&b)
  c.JSON(200, gin.H{
      "a": b.NestedStruct,
      "b": b.FieldB,
  })
}
```

## 自定义 http 配置

```go
http.ListenAndServe(":8080", router)
// 自定义
s := &http.Server{
  Addr:           ":8080",
  Handler:        router,
  ReadTimeout:    10 * time.Second,
  WriteTimeout:   10 * time.Second,
  MaxHeaderBytes: 1 << 20,
}
s.ListenAndServe()
```

## 自定义中间件

```go
func Logger() gin.HandlerFunc {
	return func(c *gin.Context) {
		t := time.Now()

		// 设置 example 变量
		c.Set("example", "12345")

		// 请求前

		c.Next()

		// 请求后
		latency := time.Since(t)
		log.Print(latency)

		// 获取发送的 status
		status := c.Writer.Status()
		log.Println(status)
	}
}
//
r := gin.New()
r.Use(Logger())

r.GET("/test", func(c *gin.Context) {
  example := c.MustGet("example").(string)
  // 打印："12345"
  log.Println(example)
})
```

## 自定义验证

```go
type Booking struct {
	CheckIn  time.Time `form:"check_in" binding:"required,bookabledate" time_format:"2006-01-02"`
	CheckOut time.Time `form:"check_out" binding:"required,gtfield=CheckIn,bookabledate" time_format:"2006-01-02"`
}
var bookableDate validator.Func = func(fl validator.FieldLevel) bool {
	date, ok := fl.Field().Interface().(time.Time)
	if ok {
		today := time.Now()
		if today.After(date) {
			return false
		}
	}
	return true
}
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		v.RegisterValidation("bookabledate", bookableDate)
	}
```

## 设置/获取 cookie

获取:`cookie, err := c.Cookie("gin_cookie")`
设置:`c.SetCookie("gin_cookie", "test", 3600, "/", "localhost", false, true)`

## 路由参数
匹配 /user/john 但不会匹配 /user/ 或者 /user:
```go
router.GET("/user/:name", func(c *gin.Context) {
  name := c.Param("name")
  c.String(http.StatusOK, "Hello %s", name)
})
```
匹配 /user/john/ 和 /user/john/send:
```go
//  如果没有其他路由匹配 /user/john，它将重定向到 /user/john/
router.GET("/user/:name/*action", func(c *gin.Context) {
  name := c.Param("name")
  action := c.Param("action")
  message := name + " is " + action
  c.String(http.StatusOK, message)
})
```

## 路由组
```go
v1 := router.Group("/v1")
{
  v1.POST("/login", loginEndpoint)
  v1.POST("/submit", submitEndpoint)
  v1.POST("/read", readEndpoint)
}
```

## 运行多个服务
GO 
```go
var (
	g errgroup.Group
)

func router01() http.Handler {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/", func(c *gin.Context) {
		c.JSON(
			http.StatusOK,
			gin.H{
				"code":  http.StatusOK,
				"error": "Welcome server 01",
			},
		)
	})
	return e
}
func router02() http.Handler {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/", func(c *gin.Context) {
		c.JSON(
			http.StatusOK,
			gin.H{
				"code":  http.StatusOK,
				"error": "Welcome server 02",
			},
		)
	})

	return e
}

server01 := &http.Server{
  Addr:         ":8080",
  Handler:      router01(),
  ReadTimeout:  5 * time.Second,
  WriteTimeout: 10 * time.Second,
}

server02 := &http.Server{
  Addr:         ":8081",
  Handler:      router02(),
  ReadTimeout:  5 * time.Second,
  WriteTimeout: 10 * time.Second,
}

g.Go(func() error {
  return server01.ListenAndServe()
})

g.Go(func() error {
  return server02.ListenAndServe()
})

if err := g.Wait(); err != nil {
  log.Fatal(err)
}
```
## 重定向
### get重定向
```go
r.GET("/test", func(c *gin.Context) {
	c.Redirect(http.StatusMovedPermanently, "http://www.google.com/")
})
```
### post 重定向
```go
r.POST("/test", func(c *gin.Context) {
	c.Redirect(http.StatusFound, "/foo")
})
```
### 路由重定向
使用`HandleContext`
```go
r.GET("/test", func(c *gin.Context) {
    c.Request.URL.Path = "/test2"
    r.HandleContext(c)
})
r.GET("/test2", func(c *gin.Context) {
    c.JSON(200, gin.H{"hello": "world"})
})
```

## 静态文件
```go
router.Static("/assets", "./assets")
router.StaticFS("/more_static", http.Dir("my_file_system"))
router.StaticFile("/favicon.ico", "./resources/favicon.ico")
```
## 静态资源嵌入
```go
// loadTemplate 加载由 go-assets-builder 嵌入的模板
func loadTemplate() (*template.Template, error) {
	t := template.New("")
	for name, file := range Assets.Files {
		if file.IsDir() || !strings.HasSuffix(name, ".tmpl") {
			continue
		}
		h, err := ioutil.ReadAll(file)
		if err != nil {
			return nil, err
		}
		t, err = t.New(name).Parse(string(h))
		if err != nil {
			return nil, err
		}
	}
	return t, nil
}
t, err := loadTemplate()
if err != nil {
  panic(err)
}
r.SetHTMLTemplate(t)

r.GET("/", func(c *gin.Context) {
  c.HTML(http.StatusOK, "/html/index.tmpl", nil)
})
```