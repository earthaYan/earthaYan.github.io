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

- gin.H 是 map[string]interface{}的快捷方式

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
