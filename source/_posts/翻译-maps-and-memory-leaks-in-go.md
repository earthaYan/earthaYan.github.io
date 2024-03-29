---
title: 翻译-maps-and-memory-leaks-in-go
date: 2022-12-10 16:39:30
tags: [GoLang]
categories: 翻译
---

# Go 中的 Maps 和内存泄漏

待完成
https://teivah.medium.com/maps-and-memory-leaks-in-go-a85ebe6e7e69

<b>长话短说：</b> map 在内存中会一直增长,不会缩小。因此如果它引起了一些内存问题，你可以尝试不同的选项：比如强制 GO 重新创建 map 或者使用指针。

使用 Go 语言的时候,我们需要了解 map 如何扩大和缩小的一些重要特征。深入了解这一点可以预防会导致内存泄漏的问题。

首先为了看这个问题的具体的例子，我们假设一个场景，在这个场景下我们会使用下面的 map:

```go
m:=make(map[int][128]byte)
```

m 的每一个值都是一个 128 byte 的数组。我们会执行下面的操作：

1. 分配一个空的 map
2. 添加一百万个元素
3. 移除所有元素,运行垃圾回收(GC)

在每一步完成后，我们想要打印堆的大小(使用工具函数 `printAlloc` )。这个程序向我们展示了这个例子里内存的变化:

```go
func main() {
	n := 1_000_000
	m := make(map[int][128]byte)
	printAlloc()

	for i := 0; i < n; i++ { // Adds 1 million elements
		m[i] = [128]byte{}
	}
	printAlloc()

	for i := 0; i < n; i++ { // Deletes 1 million elements
		delete(m, i)
	}

	runtime.GC() // Triggers a manual GC
	printAlloc()
	runtime.KeepAlive(m) // Keeps a reference to m so that the map isn’t collected
}

func printAlloc() {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("%d KB\n", m.Alloc/1024)
}
```

我们分配一个空的 map,添加了 100 万个元素,又移除了 100 万个元素,然后运行一个垃圾回收器。我们也使用了 `runtime.KeepAlive` 确保对 map 的引用，这样 map 也不会被回收。让我们运行这个例子：

> 0 MB <-- After m is allocated
> 461 MB <-- After we add 1 million elements
> 293 MB <-- After we remove 1 million elements

我们能够观察到什么呢?刚开始堆的大小是极小的。向 map 里面添加 100 万个元素之后,它开始明显增长。但是如果我们期望堆大小在移除所有元素之后有所减少，这在 GO 里是不可能的。最后，即使 GC 已经回收了所有元素,堆大小仍然还有 293M。尽管内存减少了,但是并没有达到我们的期望。根本原因是什么呢？我们需要深入了解 Go 语言中 map 是如何工作的。

map 会提供一个无序的键值对集合,并且里面的键名都不一样。在 Go 语言中,map 是基于哈希表数据结构：这是一个数组并且其中的每一个元素都是一个指针，指向一桶键值对,如图 1 所示。
{% asset_img hash_table.webp 图1-关注桶0的哈希表示例%}

每个桶都是一个大小固定的数组,有 8 个元素。在插入到一个满桶(桶溢出)的情况下,Go 会创建一个新的 8 个元素的桶并且连接到前面那个桶。图 2 展示了这个例子：
{%asset_img buket.webp 图2-在桶溢出的情况下，Go会分配一个新的桶并连接到前面的桶 %}

从底层来看,一个 Go map 就是一个指针,指向 `runtime.hmap` 结构。这个结构包含了多个域，如 B 域,它给出了 map 中桶的数量：

```go
type hmap struct {
    B uint8 // log_2 of # of buckets
            // (可以容纳 系数* 2^B 项)
    // ...
}
```

在添加 100 万个元素以后,B 的值为 18,这意味着有 2<sup>18</sup>=262144 个桶。当我们移除这些元素的时候,B 的值是多少呢?仍然是 18。所以 map 仍然包含了同样数量的桶。

原因就是 map 中的桶的数量不能减少。因此从 map 中移除元素并不影响已经存在的桶的数量;它只是把桶内的插槽归零。map 只会增长,出现更多的桶;但从来不会减少。

在之前的例子中,我们从 461M 到 293M,因为元素被回收了,但是运行 GC 并不影响 map 本身。即使是额外桶(因为桶溢出而创建的桶)的数量也会保持一样。

我们退一步讨论：map 不能缩小这个事什么时候会成为一个问题?假设使用 `map[int][128]byte` 构造一个 cache。这个 map 包含每个用户的 ID(int)，一个 128 byte 的序列。现在假设我们想要保存最后的 1000 个用户。map 的 size 将会保持为一个常量,所以我们不需要担心 map 不能缩小的问题。

但是,假如我们想要保存一小时内的数据呢。与此同时公司决定在黑色星期五开展一个大促销：在一小时内可能会有数以百万的用户连接我们的系统。但是之后的几天里,我们的 map 会包含和高峰期的时候同样数量的桶。这就解释了为什么在这种情况下我们会遇到内存消耗大但是并没有明显减少的情况。

如果我们不想要手动重启服务来清除被 map 消耗的内存数量有什么解决方案呢?一个解决方案是有规律的重建一个当前 map 的拷贝。例如,我们可以每隔一个小时构建一个新的 map,这个 map 会复制所有的元素并释放之前的那个 map。这个方案的主要缺陷是在复制和直到下一次垃圾回收之前，短期内我们可能会消耗当前内存的两倍。

另外一个解决方案是修改 map 类型来存储一个数组指针：`map[int]*[128]byte`。它并不能解决桶数量大的问题;但是每个桶的入口将会保留指针的大小,而不是128字节(64位系统上的8字节,32位系统上的4字节)。


回到最初的设想场景,让我们来比较一下每个步骤之后的每种map类型的内存消耗。结果如下面的表格所示：

| Step      | `map[int][128]byte` | `map[int]*[128]byte` |
| ----------- | ----------- | ----------- | 
| Allocate an empty map      | 0 MB       | 0 MB |
| Add 1 million elements  | 461 MB        | 182 MB |
| Remove all the elements and run a GC   | 293 MB        | 38 MB |


正如我们所看到的，移除所有元素之后,使用 `map[int]*[128]byte` 类型的需要的内存数量很明显更少。而且在这个案例中，由于做了一些优化来减少内存消耗，所以高峰期需要的内存数量也没那么重要了。

【注意】如果key或者valu超过128字节,GO就不会直接在map桶中存储它。而是储存一个指向key或者value的指针

## 总结
如我们所见,添加n个元素到map中，然后移除所有元素意味着在内存中保持相同的桶数量。所以必须记住：因为map在size上只会增长，所以内存消耗也只会增长。目前没有自动化策略去缩小它。如果因为这个引起了高内存消耗,我们可以尝试不同的方法去解决这个问题，比如重新创建map或者使用指针来检查它是否可以被优化。