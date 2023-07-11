---
title: session vs cookie
date: 2023-01-13 13:09:49
tags: [GoLang]
categories: 后端
---
##  cookie
### 原理
在<font color=red>本地计算机【浏览器端】</font>保存用户操作的历史信息，如登录信息，并在用户再次访问该站点时浏览器通过HTTP协议将本地cookie内容发送给服务器，从而完成验证，或继续上一步操作。
{% asset_img 6.1.cookie2.png cookie原理 %}
### 特点
有时间限制，分为会话cookie和持久cookie
- 会话cookie:
    1.  不设置过期时间，生命周期为从创建到浏览器关闭为止,一般不保存在硬盘上而是保存在内存里
    2.  cookie是否可以在不同的浏览器进程间共享由不同浏览器决定
- 持久cookie:
    1.  设置过期时间,cookie保存到硬盘上，关闭后再次打开浏览器，这些cookie依然有效
    2.  cookie可以在不同的浏览器进程间共享
### go使用 
#### 设置cookie
`http.setCookie(w ResponseWriter, cookie *Cookie)`
> w表示需要写入的response，cookie是一个struct

```go
// cookie对象
type Cookie struct {
	Name       string //常用
	Value      string //常用，
	Path       string
	Domain     string
	Expires    time.Time//常用
	RawExpires string
  // MaxAge=0 means no 'Max-Age' attribute specified.
  // MaxAge<0 means delete cookie now, equivalently 'Max-Age: 0'
  // MaxAge>0 means Max-Age attribute present and given in seconds
	MaxAge   int
	Secure   bool
	HttpOnly bool
	Raw      string
	Unparsed []string // Raw text of unparsed attribute-value pairs
}

```
示例：
```go
expiration := time.Now()
expiration = expiration.AddDate(1, 0, 0)
cookie := http.Cookie{Name: "username", Value: "astaxie", Expires: expiration}
http.SetCookie(w, &cookie)
```
[maxAge和expires区别](https://jiapan.me/2017/cookies-max-age-vs-expires/)
#### 读取cookie
通过request获取cookie：`cookie, _ := r.Cookie("username")`

---

## session
### 原理
在<font color=red>服务器</font>上保存用户操作的历史信息。服务器使用session id来标识session，session id由服务器负责产生，相当于一个唯一的随机密钥，避免在握手或传输中暴露用户真实密码。但该方式下，仍然需要将发送请求的客户端与session进行对应，所以可以借助cookie机制来获取客户端的标识（即session id），也可以通过GET方式将id提交给服务器。

{% asset_img 6.1.session.png session原理 %}
###
session通过cookie，在客户端保存session id