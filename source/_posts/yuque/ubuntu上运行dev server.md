---
title: ubuntu上运行dev server
urlname: axvpa0
date: '2022-03-14 16:33:21 +0800'
tags: []
categories: []
---

1.安装 node.js

```bash
wget https://nodejs.org/dist/v16.1.0/node-v16.1.0-linux-x64.tar.xz
tar -xvf node-v16.1.0-linux-x64.tar.xz
pwd
ln /home/ubuntu/node-v16.1.0-linux-x64/bin/node /usr/local/bin/node
ln /home/ubuntu/node-v16.1.0-linux-x64/bin/npm /usr/local/bin/npm
ln /home/ubuntu/node-v16.1.0-linux-x64/bin/npx /usr/local/bin/npx

```

2.安装 yarn

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg |  apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt update && apt install yarn
```

3.安装依赖
4.yarn start 报错：
![1647247257(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1647247264428-974b325b-4c63-4ed0-b324-67ec76012023.png#clientId=u8858a88d-dd97-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=512&id=u3c3d9a7a&margin=%5Bobject%20Object%5D&name=1647247257%281%29.png&originHeight=768&originWidth=827&originalType=binary∶=1&rotation=0&showTitle=false&size=47782&status=done&style=none&taskId=ud045349a-8c8e-4ce9-adbf-4957cdb9056&title=&width=551.3333333333334)
解决方法：
![1647247701(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1647247708629-38528130-56e0-4bed-b94e-403f91120be3.png#clientId=u8858a88d-dd97-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=428&id=ub1d651bd&margin=%5Bobject%20Object%5D&name=1647247701%281%29.png&originHeight=642&originWidth=1260&originalType=binary∶=1&rotation=0&showTitle=false&size=225803&status=done&style=none&taskId=u3c536b28-6e6c-4de0-97ed-e37ced6df97&title=&width=840)
原因同上，就是 vite 默认是打开浏览器的，但是 linux 没有这个功能，所以需要修改 vite 配置

```bash
  server: {
    port: 5200,
    host: '0.0.0.0',
    open: false,//在linux上运行时候需要设置为false
    proxy: {
      '/v': {
        target: 'http://10.186.62.50:25799',
      },
    },
    cors: true,
  },
```
