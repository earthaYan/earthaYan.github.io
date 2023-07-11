---
title: RPC-API
date: 2022-12-16 13:33:54
tags: [GoLang]
categories: 后端
---

## RPC基本含义：
远程过程调用(Remote Procedure Call),属于计算机通信协议。
允许A计算机调用B计算机的子程序而不用为这个交互作用编程，屏蔽了底层的网络通信细节

{% asset_img RPC.webp RPC的调用过程%}
1. Client 通过本地调用，调用 Client Stub。
2. Client Stub 将参数打包（也叫 Marshalling）成一个消息，然后发送这个消息。
3. Client 所在的 OS 将消息发送给 Server。
4. Server 端接收到消息后，将消息传递给 Server Stub。
5. Server Stub 将消息解包（也叫 Unmarshalling）得到参数。
6. Server Stub 调用服务端的子程序（函数），处理完后，将最终结果按照相反的步骤返回给 Client。

> Stub 负责调用参数和返回值的流化（serialization）、参数的打包和解包，以及网络层的通信。Client 端一般叫 Stub，Server 端一般叫 Skeleton


## gRPC 
google RPC
1. 支持多种语言，比如用Go语言实现gRPC服务,可以通过Java客户端调用gRPC服务提供的方法
2. 基于IDL（Interface Definition Language）文件定义服务
  - gRPC服务预先定义好接口(名称/入参/返回值)。
  - 服务端实现定义的接口
  - 客户端,gRPC存根提供了跟服务端相同的方法
  - 通过 proto3 工具生成指定语言的数据结构、服务端接口以及客户端 Stub
3. 通信协议基于HTTP/2设计
4. 支持 Protobuf 和 JSON 序列化数据格式
  - Protobuf ：和语言无关的序列化框架，可以减少网络传输流量,提高通信效率

## Protocol Buffers
gRPC API接口常用的数据传输格式，对数据结构进行序列化。
既可以做数据通信协议，也可以作为数据格式
1. 数据传输速度快：传输时会把数据序列化为二进制数据
  - 相对于XML和JSON的文本传输格式可以节省大量IO操作，提高传输速度
2. 跨平台多语言
  - 自带的编译工具 protoc可以基于protobuf定义文件，编译出不同语言的客户端/服务端
3. 扩展性/兼容性
  - 不破坏原有程序的基础手上更新已有的数据结构
4. 基于 IDL 文件定义服务，通过 proto3 工具生成指定语言的数据结构、服务端和客户端接口

## Protocol Buffers在gRPC接口中的作用
1. 定义数据结构
```go
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
// 此处定义了一个Cache服务,服务包含ListSecrets和ListPolicies两个API接口
// Cache implements a cache rpc service.
service Cache{
  rpc ListSecrets(ListSecretsRequest) returns (ListSecretsResponse) {}
  rpc ListPolicies(ListPoliciesRequest) returns (ListPoliciesResponse) {}
}
```
3. 通过 protobuf 序列化和反序列化，提升传输效率



## gRPC使用
### 安装protoc
```bash

# 第一步：安装 protobuf
$ cd /tmp/
$ git clone -b v3.21.1 --depth=1 https://github.com/protocolbuffers/protobuf
$ cd protobuf
$ ./autogen.sh
$ ./configure
$ make
$ make install 
$ protoc --version # 查看 protoc 版本，成功输出版本号，说明安装成功
libprotoc 3.21.1

# 第二步：安装 protoc-gen-go
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

# 第三步:客户端和服务器代码
# 生成的 .pb.go 文件在输出目录中的放置位置取决于编译器标志
protoc   --go_out=. --go_opt=paths=source_relative  helloworld/helloworld.proto
protoc   --go-grpc_out=. --go-grpc_opt=paths=source_relative helloworld/helloworld.proto
```
编译器标志：输出模式
1. paths=import: 默认输出模式，输出文件将存放在以GO软件包的导入路径命名的目录中
输入文件:/root/protos/buzz.proto 
GO文件导入路径：example.com/project/protos/fizz
输出文件：/root/../example.com/project/protos/fizz/buzz.pb.go
2. paths=source_relative: 输出文件将与输入文件位于同一相对目录中
输入文件:protos/buzz.proto
输出文件:protos/buzz.pb.go。
3.  module=$PREFIX:输出文件会被放置在一个以 Go 软件包的导入路径命名的目录中，但指定的目录前缀会从输出文件名中移除
输入文件：protos/buzz.proto
go导入路径：example.com/project/protos/fizz
前缀：example.com/project 
输出文件：protos/fizz/buzz.pb.go

> Go 导入路径与 .proto 文件中的 package 说明符之间没有关联。后者只与 protobuf 命名空间相关，而前者仅与 >  Go 命名空间相关。此外，Go 导入路径与 .proto 导入路径之间没有任何关联。

### 报错
#### 执行./autogen.sh报错
1. ./autogen.sh: line 41: autoreconf: command not found
解决方法：yum安装 autoconf
2. Can't exec "aclocal": No such file or directory at /usr/share/autoconf/Autom4te/ FileUtils.pm line 326. 
解决方法：yum 安装automake
3. configure.ac:109: error: possibly undefined macro: AC_PROG_LIBTOOL.If this token and others are legitimate, please use m4_pattern_allow.See the Autoconf documentation.
解决方法：yum 安装libtool
#### 执行./configure报错
1. configure: error: in `/tmp/protobuf':configure: error: C++ preprocessor "/lib/cpp" fails sanity check  See 'config.log' for more details
解决方法：由于c++编译器的相关package没有安装，yum 安装`yum install glibc-headers gcc-c++`


## gRPC demo 实现

1. 定义gPRC服务
2. 生成客户端和服务器代码
3. 实现gRPC服务
4. 实现gRPC客户端

```go
tree
├── client
│   └── main.go
├── helloworld
│   ├── helloworld.pb.go
│   └── helloworld.proto
└── server
    └── main.go
```
client:存放客户端代码
helloworld:存放服务的IDL定义
server：存放server目录
### proto文件：定义服务
编译命令：
`protoc -I=$SRC_DIR --go_out=$DST_DIR $SRC_DIR/addressbook.proto`

### 服务方法类型
1. 简单模式:客户端发起一次请求，服务端响应一个数据
```go
rpc SayHello (HelloRequest) returns (HelloReply) {}
```
2. 服务端数据流模式:客户端发送一个请求，服务器返回数据流响应，客户端从流中读取数据直到为空
```go
rpc SayHello (HelloRequest) returns (stream HelloReply) {}
```
3. 客户端数据流模式：客户端将消息以流的方式发送给服务器，服务器全部处理完成之后返回一次响应。
```go
 rpc SayHello (stream HelloRequest) returns (HelloReply) {}
```
4. 双向数据流模式:客户端和服务端都可以向对方发送数据流，这个时候双方的数据可以同时互相发送
```go
rpc SayHello (stream HelloRequest) returns (stream HelloReply) {}
```




## 区别
{%asset_img grpc-vs-restful.webp 接口类型比较%}



























































































































