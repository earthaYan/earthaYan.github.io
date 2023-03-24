---
title: gin-web笔记
date: 2023-03-23 01:25:14
tags: [golang, Gin]
categories: GoLang
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
## 使用http方法
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
## 只绑定url查询字符串
只绑定url查询参数，而忽略post参数：`ShouldBindQuery`
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