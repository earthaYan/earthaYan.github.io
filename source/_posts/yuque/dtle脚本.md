---
title: dtle脚本
urlname: hdgt1n
date: '2022-07-14 10:39:46 +0800'
tags: [工作]
categories: [工作]
---

FROM reg.actiontech.com/actiontech/yarn_build_v15:latest
RUN apk add git
ENV build_arg=""
CMD ["sh","-c","yarn install && yarn build $build_arg"]
