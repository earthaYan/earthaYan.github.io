---
title: iam项目的部署
date: 2022-12-08 22:16:09
tags: [GoLang]
categories: 后端
---

## IAM的核心功能使用步骤
### 创建平台资源
1. 用户通过前端请求 iam-apiserver 提供的 RESTful API 接口完成用户、密钥、授权策略的增删改查
2. iam-apiserver 将这些资源持久化存储在MySQL中
3. 为了确保通信安全，客户端访问服务端都是通过HTTPS协议
### 请求API完成资源授权
1. 用户通过前端请求 iam-authz-server 提供的 /v1/authz 接口进行资源授权
  - 先通过密钥认证
  - 认证通过后,/v1/authz 接口会查询授权策略，决定资源请求是否被允许
2. iam-authz-server 将密钥和策略信息缓存在内存中，实现快速查询，提高/v1/authz接口性能
3. 如何实现密钥和策略信息的缓存
  - iam-authz-server 调用 iam-apiserver 提供的 gRPC接口，将上述信息缓存到内存中
  - 为了保持内存中的缓存和iam-apiserver保持一致，iam-apiserver有上述信息被更新的时候，iam-apiserver 会往特定的 Redis Channel（iam-authz-server 也会订阅该 Channel）中发送 PolicyChanged 和 SecretChanged 消息。
  - 当 iam-authz-server 监听到有新消息时就会获取并解析消息，根据消息内容判断是否需要重新调用 gRPC 接来获取密钥和授权策略信息，再更新到内存中。
### 授权日志分析
1. iam-authz-server将授权日志上报到redis高速缓存中
2. iam-pump异步消费授权日志，把清理后的数据保存在 MongoDB 中，供运营系统查询
  - iam-authz-server 将授权日志保存在 Redis 中，可以最大化减少写入延时。
  - 不保存在内存中是因为授权日志量我们没法预测，当授权日志量很大时，很可能会将内存耗尽，造成服务中断。
### 运营平台授权数据展示

{% asset_img iam-operating-system.webp  iam操作系统前后端分离架构%}

总结：
> 1. 首先，用户通过调用 iam-apiserver 提供的 RESTful API 接口完成注册和登录系统，
> 2. 再调用接口创建密钥和授权策略。
> 3. 创建完密钥对和授权策略之后，IAM 可以通过调用 iam-authz-server 的授权接口完成资源的授权。
>    - 具体来说，iam-authz-server 通过 gRPC 接口获取 iam-apiserver 中存储的密钥和授权策略信息，通过 JWT 完成认证之后，再通过 ory/ladon 包完成资源的授权。i
>    - iam-pump 组件异步消费 Redis 中的数据，并持久化存储在 MongoDB 中，供 iam-operating-system 运营平台展示。
>     - 最后，IAM 相关的产品、研发人员可以通过 IAM 的运营系统 iam-operating-system 来查看 IAM 系统的使用情况，进行运营分析。例如某个用户的授权 / 失败次数、授权失败时的授权信息等。



## iam主要功能
1. 认证：用来判断是否是平台的合法用户，比如使用用户名和密码
2. 授权：用来判断是否可以访问平台的某类资源