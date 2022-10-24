---
title: 11-go-api
date: 2022-10-18 10:29:23
tags: [golang, 后端, 实践]
categories: GoLang
---

## 常用的 API 风格

1. REST:表现层状态转移（REpresentational State Transfer
2. RPC
3. GraphQL

## REST API 设计原则

将 URI 映射为 REST 资源

### URI 设计

1. 资源名使用名词而不是动词，并且用名词复数表示
2. URI 结尾不应包含/
3. URI 中不能出现下划线 \_，必须用中杠线 -代替
4. URI 路径用小写，不要用大写
5. 避免超过两层的 URI，可使用?参数表示较多的资源
6. 操作不能映射为一个 REST 资源,则可以将操作变成资源的属性或者将操作当作是一个资源的嵌套资源

```go
PUT /gists/:id/star  # github star action
DELETE /gists/:id/star  # github unstar action
```

#### 原则

1. 安全性：不会改变资源状态，可以理解为只读的
2. 幂等性：执行 1 次和执行 N 次，对资源状态改变的效果是等价的

### REST 资源操作映射为 Http 方法

{% asset_img http.webp REST 资源操作映射为 Http 方法 %}

### API 版本管理

必须做到向下兼容，即新老版本共存

#### 版本标识

1. URI 中，如`/v1/users`
2. HTTP Header 中,如 `Accept: vnd.example-com.foo+json; version=1.0`
3. Form 参数中，如`/users?version=v1`

### API 命名

1. 驼峰命名法 `serverAddress`
2. 蛇形命名法 `server_address`
3. 脊柱命名法 `server-address`

### 统一分页 / 过滤 / 排序 / 搜索功能

这些功能是每个 REST 资源都能用到的，所以实现为一个公共的 API 组件

1. 分页功能：减少 API 响应的延时，同时可以避免返回太多条目，导致服务器 / 客户端响应特别慢，甚至导致服务器 / 客户端 crash 的情况
2. 过滤功能：如果用户不需要一个资源的全部状态属性，可以在 URI 参数里指定返回哪些属性，例如`/users?fields=email,username,address`
3. 排序功能：在 URI 参数中指明排序参数，例如`/users?sort=age,desc`
4. 搜索功能：模糊匹配搜索

### 域名

1. `https://marmotedu.com/api`：适合 API 将来不会进一步扩展，域名下只有一套 API 系统
2. `https://iam.api.marmotedu.com`：如果域名下未来会新增另一个 API 系统 ，可设置为每个系统的 API 拥有专有的 API 域名

### 统一的返回格式

## 接口文档如何编写

1. 接口描述：描述接口实现了什么功能
2. 请求方法：接口的请求方法，格式为 HTTP 方法 请求路径，例如 `POST /v1/users`。在 通用说明中的请求方法部分，会说明接口的请求协议和请求地址
3. 输入参数：接口的输入字段，它又分为 Header 参数、Query 参数、Body 参数、Path 参数。每个字段通过：参数名称、必选、类型 和 描述 4 个属性来描述。如果参数有限制或者默认值，可以在描述部分注明
4. 输出参数：接口的返回字段，每个字段通过 参数名称、类型 和 描述 3 个属性来描述。
5. 请求示例：一个真实的 API 接口请求和返回示例。
