---
title: web服务构建
date: 2023-02-22 16:56:01
tags: [golang, web]
categories: GoLang
---

## iam-api-server 服务

本质：web 服务,通过一个名为 iam-apiserver 的进程，对外提供 RESTful API 接口，完成用户、密钥、策略三种 REST 资源的增删改查。

### 功能

#### 认证相关接口

{%asset_img authn.webp %}

#### 用户相关接口

{%asset_img user.webp %}

#### 密钥相关接口

{%asset_img key.webp %}

#### 策略相关接口

{%asset_img policy.webp %}
