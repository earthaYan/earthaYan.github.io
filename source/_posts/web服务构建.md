---
title: web服务构建
date: 2023-02-22 16:56:01
tags: [golang, web]
categories: GoLang
---

## iam-api-server 服务

本质：web 服务,通过一个名为 iam-api_server 的进程，对外提供 RESTful API 接口，完成用户、密钥、策略三种 REST 资源的增删改查。

### 功能

#### 认证相关接口

{%asset_img authn.webp %}

#### 用户相关接口

{%asset_img user.webp %}

#### 密钥相关接口

{%asset_img key.webp %}

#### 策略相关接口

{%asset_img policy.webp %}

### 使用方法

客户端【前端，API 调用，SDK,iamctl】都可以访问 iam-api_server，最终都会执行 HTTP 请求，调用 iam-api_server 提供的 RESTful API 接口,所以需要一个 REST API 客户端工具——curl 来执行 HTTP 请求。

```plain
-X/--request [GET|POST|PUT|DELETE|…]  指定请求的 HTTP 方法
-H/--header                           指定请求的 HTTP Header
-d/--data                             指定请求的 HTTP 消息体（Body）
-v/--verbose                          输出详细的返回信息
-u/--user                             指定账号、密码
-b/--cookie                           读取 cookie
-s/--silent                           安静模式
-S                                    强制展示错误
```

1. 登录 api-server,获取 token

```bash
$ curl -s -XPOST -H"Authorization: Basic `echo -n 'admin:Admin@2021'|base64`" http://127.0.0.1:8080/login | jq -r .token
# 将token设置为环境变量
TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJpYW0uYXBpLm1hcm1vdGVkdS5jb20iLCJleHAiOjE2MzUwNTk4NDIsImlkZW50aXR5IjoiYWRtaW4iLCJpc3MiOiJpYW0tYXBpc2VydmVyIiwib3JpZ19pYXQiOjE2MjcyODM4NDIsInN1YiI6ImFkbWluIn0.gTS0n-7njLtpCJ7mvSnct2p3TxNTUQaduNXxqqLwGfI
```

2. 创建一个名为 secret0 的 secret

```bash
curl -v -XPOST -H "Content-Type: application/json" -H"Authorization: Bearer ${TOKEN}" -d'{"metadata":{"name":"secret0"},"expires":0,"description":"admin secret"}' http://iam.api.marmotedu.com:8080/v1/secrets
```

3. 获取 secret0 的详细信息

```bash
curl -XGET -H"Authorization: Bearer ${TOKEN}" http://iam.api.marmotedu.com:8080/v1/secrets/secret0
```

4. 更新 secret0 的描述

```bash
curl -XPUT -H"Authorization: Bearer ${TOKEN}" -d'{"metadata":{"name":"secret"},"expires":0,"description":"admin secret(modify)"}' http://iam.api.marmotedu.com:8080/v1/secrets/secret0
```

5. 获取 secret 列表

```bash
curl -XGET -H"Authorization: Bearer ${TOKEN}" http://iam.api.marmotedu.com:8080/v1/secrets
```

6. 删除 secret0s

```bash
curl -XDELETE -H"Authorization: Bearer ${TOKEN}" http://iam.api.marmotedu.com:8080/v1/secrets/secret0
```

CRUD:
C：创建
R：获取数据
U：修改更新
D：删除

### 代码实现
