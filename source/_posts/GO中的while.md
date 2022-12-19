---
title: GO中的while
date: 2022-12-15 20:22:46
tags: [golang, 后端]
categories: GoLang
---

GO语言中没有while关键字，所以需要使用for代替
```go
package main

import "fmt"

func main() {
	sum := 1
	for sum < 1000 {
		sum += sum
	}
	fmt.Println(sum)
}

```
