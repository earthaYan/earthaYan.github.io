---
title: 翻译-maps-and-memory-leaks-in-go
date: 2022-11-23 16:39:30
tags: [翻译, Go]
categories: 翻译
---

# Go 中的 Maps 和内存泄漏

待完成
https://teivah.medium.com/maps-and-memory-leaks-in-go-a85ebe6e7e69

<b>长话短说：</b> map在内存中会一直增长,不会缩小。因此如果它引起了一些内存问题，你可以尝试不同的选项：比如强制GO