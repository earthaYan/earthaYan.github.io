---
title: 16-go-web服务
date: 2022-11-29 09:25:04
tags: [golang, 后端, 实践]
categories: GoLang
---

{% asset_img web服务.webp web服务分类 %}
> 前提：要实现一个web服务，必须先选择通信协议和通信格式。如果服务本身主要是提供REST 风格的API，则使用HTTP+JSON。反之则使用gRpc+Protobuf
## 基础功能
### 路由匹配
概念：根据(HTTP方法, 请求路径)匹配到处理这个请求的函数，最终由该函数处理这次请求，并返回结果
{% asset_img 路由匹配.webp 路由匹配%}
如上图所示：
-   最终这个请求由`Delete(c *gin.Context)`处理
-   参数c存放了请求参数
-   在函数Delete中进行业务处理(参数解析->参数校验->逻辑处理->返回结果)：也是web服务的核心诉求

### 路由分组
原因：API 接口随着需求的更新迭代，可能会有多个版本，为了便于管理，所以需要进行路由分组
### 一进程多服务
原因：避免为相同功能启动多个进程
典型例子：在一个服务进程中，同时开启 HTTP 服务的 80 端口和 HTTPS 的 443 端口对内的服务，访问 80 端口，简化服务访问复杂度；对外的服务，访问更为安全的 HTTPS 服务；此时有了

---
## 高级功能
### 中间件
原因：进行http请求的时候需要针对每一次请求都设置一些通用的操作，比如添加 Header、添加 RequestID、统计请求次数等
### 认证
- 方式1：基于用户名和密码
- 方式2：基于Token
### RequestID
原因：定位和跟踪某一次请求用来排障
### 跨域请求

原因：项目前后端分离，前端访问地址和后端访问地址不同，会因为浏览器的同源策略产生跨域问题

---
## Gin框架
基于net/http包封装的开源框架
### 选择web框架的考虑因素
1.  路由功能
2.  是否具有中间件或者过滤功能
3.  http的参数的解析和返回能力
4.  性能，稳定性
5.  使用门槛
6.  社区活跃度

---

### http/https支持
```go
// 一进程多端口
// 开启http服务
insecureServer := &http.Server{
    Addr:         ":8080",
    Handler:      router(),
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
}

// 开启https端口
secureServer := &http.Server{
    Addr:         ":8443",
    Handler:      router(),
    ReadTimeout:  5 * time.Second,
    WriteTimeout: 10 * time.Second,
}
```
----

### json 数据支持
1. 通过c.ShouldBindJSON函数解析Body 中的 JSON 格式数据参数
2. 通过c.JSON函数返回 JSON 格式的数据
```go
if err := c.ShouldBindJSON(&product); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
}
c.JSON(http.StatusOK, product)
```
---

### 路由匹配
#### 精确匹配
精确匹配——路由为 /products/:name
{% asset_img 路由精确匹配.webp 路由精确匹配%}
#### 模糊匹配
模糊匹配——路由为 /products/*name
{% asset_img 路由模糊匹配.webp 模糊匹配%}

---

### 路由分组
Gin通过Group函数实现分组
```go
func router() http.Handler {
    router := gin.Default()
    productHandler := newProductHandler()
    // 路由分组、中间件、认证
    // 给所有属于 v1 分组的路由都添加 gin.BasicAuth 中间件，以实现认证功能
    v1 := router.Group("/v1", gin.BasicAuth(gin.Accounts{"foo": "bar", "colin": "colin404"}))
    {
        productv1 := v1.Group("/products")
        {
            // 路由匹配
            productv1.POST("", productHandler.Create)
            productv1.GET(":name", productHandler.Get)
        }
    }
    return router
}
```
---

### 一进程多服务
#### go的并发

Go语言支持并发,通过go关键词来开启一个goroutine(轻量级线程,其调度由GoLang运行时进行管理)
```go
go 函数名( 参数列表 )
```

#### 实例
实现了2个相同的服务，分别监听在不同端口。
```go
var eg errgroup.Group
insecureServer := &http.Server{...}
secureServer := &http.Server{...}
// insecureServer
// 启动一个 goroutine 去处理
eg.Go(func() error {
  err := insecureServer.ListenAndServe()
  if err != nil && err != http.ErrServerClosed {
    log.Fatal(err)
  }
  return err
})
// secureServer
eg.Go(func() error {
  err := secureServer.ListenAndServeTLS("server.pem", "server.key")
  if err != nil && err != http.ErrServerClosed {
    log.Fatal(err)
  }
  return err
}
// 等待所有的 goroutine 结束后退出，返回的错误是一个出错的 err
if err := eg.Wait(); err != nil {
  log.Fatal(err)
})
```