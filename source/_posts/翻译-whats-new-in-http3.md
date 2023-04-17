---
title: 翻译-whats-new-in-http3
date: 2023-04-16 14:24:22
tags: [翻译, http]
categories: 翻译
---

## HTTP/3 中的新特性?

### 漫游 HTTP/0.9, HTTP/1.0, HTTP/1.1, HTTP/2, and HTTP/3

> "超文本传输协议（HTTP）是应用层协议，用于分布式、协作式超媒体信息系统。它是一个通用的、无状态的协议，可以用于超文本以外的很多任务，比如：name server 和分布式对象管理系统。-[W3](https://www.w3.org/Protocols/rfc2616/rfc2616.html)

HTTP 使浏览器和服务器能够通信。它构成了 web 服务器执行最基础的操作所必须有的基础。HTTP 经历了多个阶段。最新的草案 [超文本传输协议版本 3](https://quicwg.org/base-drafts/draft-ietf-quic-http.html) (HTTP/3)在 2021 年 5 月 27 日发布。

接下来我们了解下 HTTP 的历史，并探索 HTTP/3 中的新特性。

## HTTP/0.9

[Sir Timothy John Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee) , 也被称为 TimBL,是英国的计算机科学家，同时也是万维网的发明者。他在 1989 年创建了一行的 HTTP 协议 . 简单地返回了一个网页。这个协议在 1991 年被命名为 HTTP/0.9。

它只是一个简单的[单页规范](https://www.w3.org/Protocols/HTTP/AsImplemented.html)。只有一种方法：GET,后面跟着文档地址和可选端口地址，以回车(CR)和换行(LF)作为结束：

```bash
    GET /aWebpage.html
```

响应可能是被请求的 HTML 文件:

```html
<html>
  The Webpage content
</html>
```

或者也有可能是一个错误页面:

```html
<html>
  Cannot get the page
</html>
```

HTTP/0.9 有 4 个术语：连接，断开连接，请求和响应。没有 HTTP 头，状态码、错误码，也没有 cookie 以及其他的现代特性。HTTP/0.9 是基于 TCP——传输控制协议 构建的。connection 会在响应后立刻终止。

## HTTP/1.0

1996 年 HTTP/1.0 发布。[规范](https://datatracker.ietf.org/doc/html/rfc1945)显著扩展，支持三种方法：GET, Head 和 POST。增加了术语： 消息, 资源, 实体, 客户端, 用户代理, 服务端, 源服务器, 代理, 网关, 隧道和 缓存。

下面是在 HTTP/0.9 基础上 HTTP/1.0 做出的改进：

- 每个请求都附加 HTTP 版本。
- 状态码在响应的开头被发送。
- 请求和响应都包括 HTTP 头。
- 头部的元数据让协议更加灵活和易扩展。
- 头部的 content type 使得 http 有能力传输 HTML 文件以外的文档。

但是，HTTP/1.0 不是官方标准。

## HTTP/1.1

HTTP 第一个标准化版本 HTTP/1.1 ([RFC 2068](https://datatracker.ietf.org/doc/html/rfc2068))发布于 1997 年初，距离 HTTP/1.0 只有几个月。 HTTP/1.1 支持 7 种方法：OPTIONS, GET, HEAD, POST, PUT, DELETE 和 TRACE。2010 年[RFC 5789](https://datatracker.ietf.org/doc/html/rfc5789)增加了 PATCH,2014 年[RFC 7231](https://datatracker.ietf.org/doc/html/rfc7231) 增加了 CONNECT。

HTTP/1.1 附加的术语：representation, content negotiation, variant, cachable, first-hand, explicit expiration time, heuristic expiration time, age, freshness lifetime, fresh, stale, semantically transparent 和 validator.

HTTP/1.1 是 HTTP 1.0 的增强版：

- 虚拟主机允许多个从单个 ip 提供多个域。
- 持久化和流水线连接使得 web 浏览器可以通过单个的持久化连接发送多个请求。
- 缓存能够支持节省带宽，让响应更加快速。
- 分块传输编码可以在知道总长度之前就发送响应。这使得动态生成页面成为可能。
- 包括语言，编码或者类型在内多种方式的内容协商，使得客户端和服务端就要交换的最适合的内容达成一致。

HTTP/1.1 在接下来的 15 年左右非常稳定。在那期间，HTTPS（安全超文本传输协议）出现了。它是 HTTP 的安全版本，使用 SSL/TLS 进行安全的加密通信。

2000 年以来，web API 的真实潜力被认可。Roy Fielding 带领一组专家发明了 REST：REpresentational State Transfer。 REST 是一种软件架构风格，定义了创建 web 服务时必须遵守的一系列的约束和标准。REST API 在 HTTP/1.1 及以上生效。

## HTTP/2

HTTP/2 旨在更高效的使用网络资源，减少对延迟的感知。它引入了新的二进制分帧，该层不能向后兼容 HTTP/1.x 的服务端和客户端。

HTTP/2 的第一个草案使用 SPDY 作为规范草案的工作基础。[这个规范](https://datatracker.ietf.org/doc/html/rfc7540)于 2015 年发布。增加了术语： connection error, endpoint, frame, peer, receiver, sender, stream, stream error, intermediary, 和 payload body。

HTTP/2 在流上构建了并行化、优先级和流量控制：

- stream 是在已建立的 TCP 连接中的双向字节流，可以携带一条或多条消息。
- 通信通过具有任意数量的双向流的单个TCP连接完成。
- 这是一个多路复用协议。可以让多个并行请求在同一个连接上处理。
- 它拥有优先排序一个资源而不是另一个资源的能力,因此可以把他放在响应行头部。
- 允许未经请求就将representation从服务端推送到客户端。
- 它使用了二进制协议而不是文本。这让它可以被机器读取,性能得到提高。同时也提高了总体上的安全性。
- 请求头和响应头都是被压缩的。
- 帧在流上传输,数据帧的载荷受到流控制。

## HTTP/3

As more smartphones and portable devices have emerged and more devices have gone wireless, the overall web response times have increased. HTTP/2’s head-of-line blocking issue results in a slow and unresponsive user experience. Since TCP guarantees the order of packets that are sent and received, a missing packet will stop all streams, even when it might affect only one of them. HTTP/2 does not have mandatory encryption, and it is vulnerable to stream reuse attacks as well as compression page headers and cookie attacks.

HTTP/3 can resolve these issues.

HTTP/3 is the third major revision after HTTP/1.1 and HTTP/2. Currently, it is still a draft. [The latest specification](https://quicwg.org/base-drafts/draft-ietf-quic-http.html) was published on May 27, 2021. It has additional terminologies: abort, HTTP/3 connection, and content.

HTTP/3 is a new, fast, reliable, and secure protocol across all forms of devices.

- Instead of TCP, HTTP/3 uses a new protocol, QUIC, developed by Google in 2012. QUIC runs over UDP, the User Datagram Protocol.

- QUIC provides native multiplexing, and lost packets only impact the streams where data has been lost. This resolves the head-of-line blocking issue in HTTP/2.

- QUIC provides flow control for stream data and all HTTP/3 frame types that are sent on streams. Therefore, all frame headers and payloads are subject to flow control.

- The request and response headers are compressed by QPACK instead of HPACK in HTTP/2.

- Several HTTP/3 frames are used to manage server push.

- HTTP/3 includes TLS 1.3 encryption. Effectively, it acts as HTTPS.

## HTTP/3 Support

HTTP/3 brings revolutionary changes to improve web performance and security. Setting up an HTTP/3 website requires both server and browser support.

### Server support

Currently, [Google Cloud](https://cloud.google.com/), [Cloudflare](https://www.cloudflare.com/), and [Fastly](https://www.fastly.com/) support HTTP/3.

### Browser support

Chrome, Firefox, Edge, Opera, and some mobile browsers support HTTP/3. We can go to https://caniuse.com/?search=http3 to check the updated browser’s supportability. The green cells list the supported browser versions.

![HTTP/3 browser support table by [Can I use...](https://caniuse.com/?search=http3)](https://cdn-images-1.medium.com/max/2896/1*3m1FjB_lXyS2y1kBiZ8sEg.png)

On Chrome, HTTP/3 is enabled as an experimental protocol. When we type chrome://flags in the browser URL, we can see QUIC is enabled by default.

![](https://cdn-images-1.medium.com/max/2000/1*KsBjkghHX0kQdeAEtjx-ow.png)

## Protocol Checking

A request/response’s protocol can be checked via the Network tab. Open Google Chrome Developer Tools and choose the Network tab. When right-clicking the table head, the Protocol column can be selected to show the column.

![](https://cdn-images-1.medium.com/max/2274/1*Km5elHxixk9Y5jhaFkRQbg.png)

According to https://w3techs.com/technologies/overview/site_element, 45.7% of websites are on HTTP/2 and 20% of websites are on HTTP/3 as of July 2021.

![An image generated by [W3Techs](https://w3techs.com/technologies/overview/site_element)](https://cdn-images-1.medium.com/max/2000/1*LvJFI64o1rI44tVyfNoffg.png)

### HTTP/1.1 example

There are not many public websites still using the HTTP/1.1 protocol. AT&T’s login page is one of them.

![AT&T login page](https://cdn-images-1.medium.com/max/2846/1*iJBck-4B0YoEgQigzxy8nQ.png)

### HTTP/2 example

Most public websites are on HTTP/2, and so is the AT&T official page:

![AT&T official page](https://cdn-images-1.medium.com/max/2846/1*oQ162JFnETIOGmkc3NpghQ.png)

### HTTP/3 example

YouTube pages are on HTTP/3.

![Youtube official page](https://cdn-images-1.medium.com/max/2846/1*QgDSM-J_oDAyKwfKtTXQKw.png)

## Conclusion

We have walked through HTTP/0.9, HTTP/1.0, HTTP/1.1, HTTP/2, and HTTP/3. HTTP/3 uses QUIC, which runs over UDP. It is a new, fast, reliable, and secure protocol across all forms of devices.

Are you considering moving your application to an HTTP/3 server or have you updated your browsers to view web applications via HTTP/3?

Thanks for reading. I hope this was helpful. If you are interested, check out [my other Medium articles](https://jenniferfubook.medium.com/jennifer-fus-web-development-publications-1a887e4454af).
