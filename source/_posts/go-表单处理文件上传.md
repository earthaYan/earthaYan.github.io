---
title: go-表单处理文件上传
date: 2023-01-11 16:09:58
tags: [表单,Go,Web]
categories: [Go]
---

## form的`enctype`属性
1.  application/x-www-form-urlencoded   表示在发送前编码所有字符（默认）
2.  multipart/form-data	  不对字符编码。在使用包含文件上传控件的表单时，必须使用该值。
3.  text/plain	  空格转换为 "+" 加号，但不对特殊字符编码。
