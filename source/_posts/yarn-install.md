---
title: yarn-install
date: 2022-12-21 17:46:33
tags: ['工作', '常用功能']
categories: 缺陷修复
---

## yarn install 报错：

> Error: unable to verify the first certificate

      at TLSSocket.onConnectSecure (node:_tls_wrap:1539:34)
      at TLSSocket.emit (node:events:513:28)
      at TLSSocket._finishInit (node:_tls_wrap:953:8)
      at TLSWrap.ssl.onhandshakedone (node:_tls_wrap:734:12)

解决方法：暂时关闭 ssl 验证 `yarn config set strict-ssl false`

## yarn start 报错：

> node:internal/errors:478

    ErrorCaptureStackTrace(err);
    ^
    Error: ENOSPC: System limit for number of file watchers reached, watch '/root/umc-ui'

解决方法：

```go
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
cat /proc/sys/fs/inotify/max_user_watches //查看是否修改成功
```

## 全局安装 yarn

node -v

- > 16 执行`corepack enable`
- <16 执行`npm i -g corepack`

## yarn 常用操作

```bash
# 初始化项目
yarn init
# 安装所有依赖
yarn 
yarn install
# 添加单个依赖
yarn add [package]
yarn add [package]@[version]
yarn add [package]@[tag]
# 添加依赖到不同种类的依赖
yarn add [package] --dev  # dev dependencies
yarn add [package] --peer # peer dependencies
# 升级单个依赖
yarn up [package]
yarn up [package]@[version]
yarn up [package]@[tag]
# 移除依赖
yarn remove [package]
# 升级yarn 本身
yarn set version latest
yarn set version from sources
```
