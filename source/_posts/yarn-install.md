---
title: yarn-install
date: 2022-12-21 17:46:33
tags: ['工作','常用功能']
categories: 缺陷修复
---

# yarn install 报错：
>   Error: unable to verify the first certificate
      at TLSSocket.onConnectSecure (node:_tls_wrap:1539:34)
      at TLSSocket.emit (node:events:513:28)
      at TLSSocket._finishInit (node:_tls_wrap:953:8)
      at TLSWrap.ssl.onhandshakedone (node:_tls_wrap:734:12)

解决方法：暂时关闭ssl验证 `yarn config set strict-ssl false`



