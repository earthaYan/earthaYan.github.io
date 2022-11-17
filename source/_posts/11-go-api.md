---
title: 11-go-api
date: 2022-10-18 10:29:23
tags: [golang, 后端, 实践]
categories: GoLang
---

## 常用的 API 风格

1. REST:表现层状态转移(REpresentational State Transfer)
2. RPC
3. GraphQL[不常用]
   {% asset_img http.webp%}

## REST API

以资源 (resource) 为中心，所有的东西都抽象成资源

- 资源
  - Collection:
    一堆资源的集合,比如用户(User)的集合就是 Collection。
    域名/资源名复数:`https://xxx.com/users`
  - Member
    单个特定资源
    域名/资源名复数/资源名称:`https://xxx.com/users/admin`

### 规范

1. URI 结尾不应包含/
2. URI 中不能出现下划线 \_，必须用中杠线 - 代替【不强制】
3. 路径用小写，不要用大写
4. 避免层级过深的 URI。超过 2 层的资源嵌套会很乱，建议将其他资源转化为?参数
5. 有些操作不能很好地映射为一个 REST 资源的时候,将一个操作变成资源的一个属性或者将操作当作是一个资源的嵌套资源
6. 返回格式统一【成功和失败】

```bash
/schools/tsinghua/classes/rooma/students/zhang # 不推荐
/students?school=qinghua&class=rooma # 推荐
/users/zhangsan?active=false # 禁用某个用户
PUT /gists/:id/star # github star action
DELETE /gists/:id/star # github unstar action
```

### 安全性和幂等性

安全性：不会改变资源状态，可以理解为只读的。
幂等性：执行 1 次和执行 N 次，对资源状态改变的效果是等价的。

{% asset_img safe.webp%}

### 批量删除

HTTP 的 DELETE 方法不能携带多个资源名
解决方法：

1.  发起多个 DELETE 请求。
2.  操作路径中带多个 id，id 之间用分隔符分隔, 例如：DELETE /users?ids=1,2,3 。
3.  直接使用 POST 方式来批量删除，body 中传入需要删除的资源列表。

### 版本管理

/v1/login

### API 命名

- 驼峰命名法 ：/resetUserPasswd
- 蛇形命名法 ：/reset_user_passwd
- 脊柱命名法 ：/reset-user-passwd

### 统一分页，排序，过滤

资源的查询接口，通常情况下都需要实现分页、过滤、排序、搜索功能，因为这些功能是每个 REST 资源都能用到的，所以可以实现为一个公共的 API 组件

- 分页：在列出一个 Collection 下所有的 Member 时，应该提供分页功能，例如/users?offset=0&limit=20（limit，指定返回记录的数量；offset，指定返回记录的开始位置）。
- 过滤：如果用户不需要一个资源的全部状态属性，可以在 URI 参数里指定返回哪些属性，例如/users?fields=email,username,address。
- 排序：用户很多时候会根据创建时间或者其他因素，列出一个 Collection 中前 100 个 Member，这时可以在 URI 参数中指明排序参数，例如/users?sort=age,desc。
- 搜索：当一个资源的 Member 太多时，用户可能想通过搜索，快速找到所需要的 Member，或着想搜下有没有名字为 xxx 的某类资源，这时候就需要提供搜索功能。搜索建议按模糊匹配来搜索。

---

## RPC API

服务端实现了一个函数，客户端使用 RPC 框架提供的接口，像调用本地函数一样调用这个函数，并获取返回值。RPC 屏蔽了底层的网络通信细节，使得开发人员无需关注网络编程的细节，可以将更多的时间和精力放在业务逻辑本身的实现上，从而提高开发效率。
{% asset_img RPC.webp %}

### 过程

1.  Client 通过本地调用，调用 Client Stub。
2.  Client Stub 将参数打包（也叫 Marshalling）成一个消息，然后发送这个消息。
3.  Client 所在的 OS 将消息发送给 Server。
4.  Server 端接收到消息后，将消息传递给 Server Stub。
5.  Server Stub 将消息解包（也叫 Unmarshalling）得到参数。
6.  Server Stub 调用服务端的子程序（函数），处理完后，将最终结果按照相反的步骤返回给 Client。

### gRPC

google Remote Procedure Call

#### Protocol Buffers

对数据结构进行序列化的方法，可用作（数据）通信协议、数据存储格式等，也是一种更加灵活、高效的数据格式，与 XML、JSON 类似。它的传输性能非常好，所以常被用在一些对数据传输性能要求比较高的系统中，作为数据传输格式

1. 定义数据结构

```go
// 定义一个 SecretInfo 数据结构

// SecretInfo contains secret details.
message SecretInfo {
  string name = 1;
  string secret_id  = 2;
  string username   = 3;
  string secret_key = 4;
  int64 expires = 5;
  string description = 6;
  string created_at = 7;
  string updated_at = 8;
}
```

2. 定义服务接口

```go
// Cache implements a cache rpc service.
service Cache{
  rpc ListSecrets(ListSecretsRequest) returns (ListSecretsResponse) {}
  rpc ListPolicies(ListPoliciesRequest) returns (ListPoliciesResponse) {}
}
```

3. 通过 protobuf 序列化和反序列化，提升传输效率

#### gRPC demo

- 定义 gRPC 服务。
- 生成客户端和服务器代码。
- 实现 gRPC 服务。
- 实现 gRPC 客户端。
