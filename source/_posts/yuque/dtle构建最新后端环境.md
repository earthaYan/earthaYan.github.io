---
title: dtle构建最新后端环境
urlname: catgrp
date: '2022-07-19 13:45:11 +0800'
tags: [工作]
categories: [工作]
---

1.拉代码，切到对应分支 2.在项目目录下执行 make，生成 dist/dtle 文件 3.移动 dtle 文件到 dtle 所在的目录下，给 dtle 文件设置用户权限，重启 dtle
命令如下：
mv ~/workspace/dtle/dist/dtle /opt/dtle/usr/share/dtle/nomad-plugin/dtle
cd /opt/dtle/usr/share/dtle/nomad-plugin
chown dtle:dtle dtle
pkill dtle
