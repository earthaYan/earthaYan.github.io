---
title: web工作方式
date: 2023-01-10 15:44:08
tags: [浏览器,web,Go]
categories: 浏览器
---

##### 表现：
浏览网页的时候,会打开浏览器，输入网址后按下回车键，然后就会显示出你想要浏览的内容

## 背后流程
普通上网过程：
1.  输入URL时,浏览器(客户端)请求DNS服务器，获取到应对应的IP
2.  通过ip地址找到ip对应的服务器，要求建立TCP连接
3.  浏览器发送完HTTP Request（请求）包
4.  服务器接收到请求包之后开始处理请求包
5.  服务器调用自身服务，返回HTTP Response（响应）包
6.  客户端收到来自服务器的响应后开始渲染这个Response包里的主体（body）
7.  收到全部的内容随后断开与该服务器之间的TCP连接


##  Web服务器的工作原理
1.  客户机通过TCP/IP协议建立到服务器的TCP连接
2.  客户端向服务器发送HTTP协议请求包，请求服务器里的资源文档
3.  服务器向客户机发送HTTP协议应答包，如果请求的资源包含有动态语言的内容，那么服务器会调用动态语言的解释引擎负责处理“动态内容”，并将处理得到的数据返回给客户端
4.  客户机与服务器断开。由客户端解释HTML文档，在客户端屏幕上渲染图形结果

> 注意：客户机与服务器之间的通信是非持久连接的，也就是当服务器发送了应答后就与客户机断开连接，等待下一次请求


##  url和DNS解析
### URL
```
scheme://host[:port#]/path/.../[?query-string][#anchor]
scheme         指定底层使用的协议(例如：http, https, ftp)
host           HTTP服务器的IP地址或者域名
port#          HTTP服务器的默认端口是80，这种情况下端口号可以省略。如果使用了别的端口，必须指明，例如 http://www.cnblogs.com:8080/
path           访问资源的路径
query-string   发送给http服务器的数据
anchor         锚
```
### DNS-域名系统
用于TCP/IP网络，将主机名或域名转换为实际IP地址
{% asset_img 3.1.dns_hierachy.png dns %}
#### DNS解析过程
1. 在浏览器中输入www.qq.com域名，操作系统会先检查自己本地的hosts文件是否有这个网址映射关系，如果有，就先调用这个IP地址映射，完成域名解析
2.  如果hosts里没有这个域名的映射，则查找本地DNS解析器缓存，是否有这个网址映射关系，如果有，直接返回，完成域名解析。
3.  如果前两步都没有相应的网址映射关系，首先会找TCP/IP参数中设置的首选DNS服务器【本地DNS服务器】，此服务器收到查询时，如果要查询的域名，包含在本地配置区域资源中，则返回解析结果给客户机，完成域名解析
4.  如果要查询的域名，不由本地DNS服务器区域解析，但该服务器已缓存了此网址映射关系，则调用这个IP地址映射，完成域名解析
5.  如果本地DNS服务器本地区域文件与缓存解析都失效，则根据本地DNS服务器的设置（是否设置转发器）进行查询，
    - 如果未用转发模式，本地DNS就把请求发至 “根DNS服务器”，“根DNS服务器”收到请求后会判断这个域名(.com)是谁来授权管理，并会返回一个负责该顶级域名服务器的一个IP。本地DNS服务器收到IP信息后，将会联系负责.com域的这台服务器。这台负责.com域的服务器收到请求后，如果自己无法解析，它就会找一个管理.com域的下一级DNS服务器地址(qq.com)给本地DNS服务器。当本地DNS服务器收到这个地址后，就会找qq.com域服务器，重复上面的动作，进行查询，直至找到www.qq.com主机。
    - 如果用的是转发模式，此DNS服务器就会把请求转发至上一级DNS服务器，由上一级服务器进行解析，上一级服务器如果不能解析，或找根DNS或把转请求转至上上级，以此循环。不管本地DNS服务器用的是转发，还是根提示，最后都是把结果返回给本地DNS服务器，由此DNS服务器再返回给客户机

  {% asset_img 3.1.dns_inquery.png inquery %}

##  http协议

功能：让Web服务器与浏览器(客户端)通过Internet发送与接收数据
基于：TCP协议，一般使用TCP 80端口
无状态：同一个客户端的这次请求和上次请求没有对应关系，对HTTP服务器来说，它并不知道这两个请求是否来自同一个客户端
解决问题：引入了Cookie机制来维护连接的可持续状态来解决识别两个请求是否来自同一个客户端问题

### 客户端请求包——浏览器信息
```
GET /domains/example/ HTTP/1.1		//请求行: 请求方法 请求URI HTTP协议/协议版本
Host：www.iana.org				//服务端的主机名
User-Agent：Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4//浏览器信息
Accept：text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8	//客户端能接收的MIME
Accept-Encoding：gzip,deflate,sdch		//是否支持流压缩
Accept-Charset：UTF-8,*;q=0.5		//客户端字符编码集
//空行,用于分割请求头和消息体
//消息体Body,请求资源参数,例如POST传递的参数
```
####  与服务器交互的请求方法
GET,POST,PUT,DELETE->查，增，改，删

####  get与post区别

{% asset_img 3.1.http.png get请求 %} {% asset_img 3.1.httpPOST.png post请求 %}

1.  GET请求消息体为空，POST请求带有消息体
2.  GET提交的数据会放在URL之后，以?分割URL和传输数据，参数之间以&相连；POST方法是把提交的数据放在HTTP包的body中
3.  GET提交的数据大小有限制（因为浏览器对URL的长度有限制），而POST方法提交的数据没有限制
4.  GET方式提交数据，会带来安全问题，比如一个登录页面，通过GET方式提交数据时，用户名和密码将出现在URL上，如果页面可以被缓存或者其他人可以访问这台机器，就可以从历史记录获得该用户的账号和密码

> 浏览器对url长度限制:
> IE浏览器:2048字节
> 360极速浏览器:2118字节
> Firefox(Browser):65536字节
> Safari(Browser):80000字节
> Opera(Browser):190000字节
> Google(chrome):8182字节

###  服务器端响应包

```
HTTP/1.1 200 OK		//状态行=HTTP协议版本号+状态码+状态消息
Server: nginx/1.0.8	//服务器使用的WEB软件名及版本
Date:Date: Tue, 30 Oct 2012 04:14:25 GMT		//发送时间
Content-Type: text/html				//服务器发送信息的类型
Transfer-Encoding: chunked			//表示发送HTTP包是分段发的
Connection: keep-alive				//保持连接状态
Content-Length: 90					//主体内容长度
//空行 用来分割消息头和主体
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"... //消息体
```
####  状态码
- 1XX 提示信息 - 表示请求已被成功接收，继续处理
- 2XX 成功 - 表示请求已被成功接收，理解，接受
- 3XX 重定向 - 要完成请求必须进行更进一步的处理，302表示跳转
- 4XX 客户端错误 - 请求有语法错误或请求无法实现
- 5XX 服务器端错误 - 服务器未能实现合法的请求

### HTTP协议是无状态的和Connection: keep-alive的区别
从HTTP/1.1起，默认都开启了Keep-Alive保持连接特性
1.  无状态是指协议对于事务处理没有记忆能力，服务器不知道客户端是什么状态。
2.  无状态不代表HTTP不能保持TCP连接，更不能代表HTTP使用的是UDP协议（面对无连接）
3.  当一个网页打开完成后，客户端和服务器之间用于传输HTTP数据的TCP连接不会关闭，如果客户端再次访问这个服务器上的网页，会继续使用这一条已经建立的TCP连接
4.  Keep-Alive不会永久保持连接，它有一个保持时间，可以在不同服务器软件（如Apache）中设置这个时间


### 优化
1.  第一次请求url，服务器端返回的是html页面，然后浏览器开始渲染HTML
2.  当解析到HTML DOM里面的图片连接，css脚本和js脚本的链接，浏览器就会自动发起一个请求静态资源的HTTP请求，获取相对应的静态资源，然后浏览器就会渲染出来，最终将所有资源整合、渲染，完整展现在我们面前的屏幕上。
#### 网页优化：
减少HTTP请求次数，就是把尽量多的css和js资源合并在一起，目的是尽量减少网页请求静态资源的次数，提高网页加载速度，同时减缓服务器的压力。



##  Go与web
一个简单的web服务器
```go
package main

import (
	"fmt"
	"net/http"
	"strings"
	"log"
)

func sayhelloName(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()  //解析参数，默认是不会解析的
	fmt.Println(r.Form)  //这些信息是输出到服务器端的打印信息
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["url_long"])
	for k, v := range r.Form {
		fmt.Println("key:", k)
		fmt.Println("val:", strings.Join(v, ""))
	}
	fmt.Fprintf(w, "Hello astaxie!") //这个写入到w的是输出到客户端的
}

func main() {
	http.HandleFunc("/", sayhelloName) //设置访问的路由,注册了请求/的路由规则
	err := http.ListenAndServe(":9090", nil) //设置监听的端口,第二个参数默认为空则获取handler = DefaultServeMux
  // 上述 DefaultServeMux变量本质是一个路由器，用来匹配url跳转到其相应的handle函数
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
```
### 服务器端的基本概念
- Request:用户请求的信息，用来解析用户的请求信息，包括post、get、cookie、url等信息
- Response:服务器需要返回给客户端的信息
- Conn:用户的每次请求链接
- Handler:处理请求和生成返回信息的处理逻辑
### http包执行流程
{%  asset_img 3.3.http.png http包执行流程 %}
1. 创建Listen Socket，监听指定端口,等待客户端请求到来
2. Listen Socket接受客户端的请求, 得到Client Socket, 接下来通过Client Socket与客户端通信
3. 处理客户端的请求
    - 首先从Client Socket读取HTTP请求的协议头,
    - 如果是POST方法, 还可能要读取客户端提交的数据
    - 然后交给相应的handler处理请求
    - handler处理完毕准备好客户端需要的数据, 通过Client Socket写给客户端。
#### 关键点
- 如何监听端口:使用`net/http`包的`ListenAndServe`方法
- 如何接收客户端请求
- 如何分配handler
```go
// ListenAndServe方法实现
func ListenAndServe(addr string, handler Handler) error {
	server := &Server{Addr: addr, Handler: handler} //初始化一个Server对象
	return server.ListenAndServe()//调用Server对象的方法ListenAndServe
}
func ListenAndServe(addr string, handler Handler) error {
	server := &Server{Addr: addr, Handler: handler} //初始化Server对象
	return server.ListenAndServe()                  //调用Server对象的方法ListenAndServe
}
func (srv *Server) ListenAndServe() error {
	addr := srv.Addr
	ln, err := net.Listen("tcp", addr) //底层用TCP协议搭建了一个服务
	if err != nil {
		return err
	}
	return srv.Serve(ln) //调用srv.Serve监控我们设置的端口
}

func (srv *Server) Serve(l net.Listener) error {
	ctx := context.WithValue(baseCtx, ServerContextKey, srv)
	for {
		rw, err := l.Accept() //通过Listener接收请求
		c := srv.newConn(rw)  //创建一个Conn
		go c.serve(connCtx)   //单独开了一个goroutine，把这个请求的数据当做参数扔给这个conn去服务
		//高并发体现:用户的每一次请求都是在一个新的goroutine去服务，相互不影响。
    // 客户端的每次请求都会创建一个Conn，这个Conn里面保存了该次请求的信息，
    // 然后再传递到对应的handler，该handler中便可以读取到相应的header信息，这样保证了每个请求的独立性。
	}
}
func (c *conn) serve(ctx context.Context) {
	for {
		w, err := c.readRequest(ctx)                //解析request
		serverHandler{c.server}.ServeHTTP(w, w.req) //获取相应的handler去处理请求
	}
}
func (sh serverHandler) ServeHTTP(rw ResponseWriter, req *Request) {
	handler := sh.srv.Handler
	if handler == nil {
		handler = DefaultServeMux
	}
	handler.ServeHTTP(rw, req)
}
```
{% asset_img 3.3.illustrator.png 一个http连接处理流程 %}


##  Go的http包