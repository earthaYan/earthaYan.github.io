---
title: Grid 布局
urlname: gnxnnl
date: '2022-01-06 10:33:56 +0800'
tags: [工作]
categories: [工作]
---

## 背景：

平时在项目中用的比较多的布局方式是 flex，position,或者浮动，但是这些都是一维的，一次只能处理一个维度上的元素布局，一行或者一列。而要同时控制元素的行和列，就需要用到我们今天介绍的 Grid-网格布局
![](https://cdn.nlark.com/yuque/0/2022/png/115484/1641522310987-91b414d2-7f9e-4e78-be31-88cd3ece3dde.png#clientId=u07d452aa-ccdd-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=293&id=qGmLk&margin=%5Bobject%20Object%5D&originHeight=456&originWidth=764&originalType=url∶=1&rotation=0&showTitle=false&status=done&style=none&taskId=ucc934443-82d5-47ca-8e12-8cc51c4452a&title=&width=491)

## 基础知识：

### fr:

fr 是网格布局中的特定的长度单位,1fr 含义是网格容器中的可用空间的一等分
![1641523404(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641523407503-a7533b62-cff3-41e1-9360-50a66abd10d3.png#clientId=ud3afbf49-d6a8-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=89&id=u4760a4c7&margin=%5Bobject%20Object%5D&name=1641523404%281%29.png&originHeight=177&originWidth=920&originalType=binary∶=1&rotation=0&showTitle=false&size=4414&status=done&style=none&taskId=u478e3827-1ff4-4fa6-a42f-ce511674f59&title=&width=460)

### repeat(重复次数,网格轨道列表):

顾名思义就是重复，它是用来重复部分或整个轨道列表，比如当我们写十二列布局的时候，按照第一种方法写很麻烦，这时候就可以使用 repeat(12,1fr)来表示

```css
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 2fr;
}
//这样写比较啰嗦,可以使用repeat()
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr) 2fr;
}
```

### auto-fit:

当网格容器大小未知的时候,重复次数可以使用 auto-fit 代替,表示自动填充

### minmax(min,max):

表示列或者行的最小值和最大值

### 网格容器:

- display:grid /subgrid
  - 容器设置为 grid 布局以后,容器的直接子元素都会成为网格项
  - 非直接子元素不会参与网格布局，而是显示为正常的文档流
  - subgrid 目前还没有浏览器实现
- grid-template-areas:容器整体布局,容器项的 grid-area 可以从这里取值

```css
.container {
  /* 两行 三列 */
  grid-template-areas:
    "a b b"
    "a c d";
}
.item {
  grid-area: a;
}
```

- grid-auto-flow：设置没有指定位置的 grid 子项的放置方式，默认是 row，自动布局的时候通过逐行填充来排列元素，在必要时增加新行，column 是逐列填充来排列元素，在必要时增加新列

![1641526415(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641526418357-13886361-ef1d-4bb4-933c-353a92900610.png#clientId=u8a7fe8a4-613d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=79&id=u1570493c&margin=%5Bobject%20Object%5D&name=1641526415%281%29.png&originHeight=205&originWidth=891&originalType=binary∶=1&rotation=0&showTitle=true&size=4081&status=done&style=none&taskId=u3eb957df-3591-48d3-8616-5cc5d68c7b2&title=row&width=341.5 "row")![1641526459(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641526463782-2a416491-3086-4665-9267-abd35d138349.png#clientId=u8a7fe8a4-613d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=60&id=ue06ce0dd&margin=%5Bobject%20Object%5D&name=1641526459%281%29.png&originHeight=181&originWidth=899&originalType=binary∶=1&rotation=0&showTitle=true&size=4175&status=done&style=none&taskId=uad423bd0-33ee-4dfa-b085-c333da3c124&title=column&width=296.5 "column")

- 网格间距:
  - grid-column-gap:列间距
  - grid-row-gap:行间距
- 网格轨道:
  - 显式网格:
    - grid-template-columns:设置列数和大小
    - grid-template-rows:设置行数和大小
  - 隐式网格:
    - 定义一个设置好大小尺寸的容器项

```css
.container {
  display: grid;
  width: 150px;
  //这里只设置了两列
  grid-template-columns: 60px 60px;
  grid-template-rows: 30px 90px;
  grid-auto-columns: 60px;
}
.item-a {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}
.item-b {
  //网格线设置了该容器项开始于第三列，结束于容器并不存在的第四列
  grid-column: 3 / 4;
  grid-row: 2 / 3;
  background-color: rgba(255, 255, 0, 0.5);
}
```

![1641522070(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641522080339-8e3b1f7f-58ef-40f2-b31e-f03b0df703ba.png#clientId=u07d452aa-ccdd-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=137&id=uefaa4790&margin=%5Bobject%20Object%5D&name=1641522070%281%29.png&originHeight=273&originWidth=416&originalType=binary∶=1&rotation=0&showTitle=true&size=5165&status=done&style=none&taskId=u7dc93334-482f-4d57-8c2d-4d0801029bf&title=%E6%9C%AA%E8%AE%BE%E7%BD%AEgrid-auto-columns&width=208 "未设置grid-auto-columns")![1641522130(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641522134627-28dd54b5-8fd4-4105-9098-e3516dcabc2d.png#clientId=u07d452aa-ccdd-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=124&id=uc6d08697&margin=%5Bobject%20Object%5D&name=1641522130%281%29.png&originHeight=247&originWidth=409&originalType=binary∶=1&rotation=0&showTitle=true&size=2995&status=done&style=none&taskId=ue7851803-960d-4186-ba79-e4f43b96b38&title=%E8%AE%BE%E7%BD%AE%E4%BA%86grid-auto-columns&width=204.5 "设置了grid-auto-columns")

      - grid-auto-columns:设置隐式网格的列宽
      - grid-auto-rows:设置隐式网格的行高

### 网格项:

- 网格线
  - **网格项的位置不是取决于网格轨道,而是由网格线决定的**

![](https://cdn.nlark.com/yuque/0/2022/png/115484/1641522310987-91b414d2-7f9e-4e78-be31-88cd3ece3dde.png#clientId=u07d452aa-ccdd-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=293&id=JzCcN&margin=%5Bobject%20Object%5D&originHeight=456&originWidth=764&originalType=url∶=1&rotation=0&showTitle=false&status=done&style=none&taskId=ucc934443-82d5-47ca-8e12-8cc51c4452a&title=&width=491)

- grid-row-start:定义单个网格项开始的行位置
- grid-row-end:定义单个网格项结束的行位置
- grid-column-start:定义单个网格项开始的列位置
- grid-column-end:定义单个网格项结束的列位置
- span：跨越网格数目，比如 grid-row： 1/span 2 代表该网格项行开始线位置在 1，行结束线是跨越 2 个网格项

![1641525191(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641525196792-052a5661-fe4f-445b-ab52-a36dfdda97e7.png#clientId=u8a7fe8a4-613d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=117&id=u7fa3f5b8&margin=%5Bobject%20Object%5D&name=1641525191%281%29.png&originHeight=233&originWidth=903&originalType=binary∶=1&rotation=0&showTitle=true&size=6894&status=done&style=none&taskId=u33dacce1-a7bc-41f7-babc-ee27a26e2b5&title=%E6%B2%A1%E6%9C%89%E8%AE%BE%E7%BD%AE%E5%8D%95%E4%B8%AA%E5%AE%B9%E5%99%A8%E9%A1%B9%E7%9A%84%E4%BD%8D%E7%BD%AE&width=451.5 "没有设置单个容器项的位置")![1641525260(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641525263167-9b8712f1-1cd5-41ce-8d48-f82586555975.png#clientId=u8a7fe8a4-613d-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=112&id=ufb743810&margin=%5Bobject%20Object%5D&name=1641525260%281%29.png&originHeight=224&originWidth=872&originalType=binary∶=1&rotation=0&showTitle=true&size=3115&status=done&style=none&taskId=u0b1c1a5f-495d-4db5-9d95-7afcd821a01&title=grid-row%EF%BC%9A%201%2Fspan%202&width=436 "grid-row： 1/span 2")

- grid-area: 上面四个属性的缩写,通过基线（line）,跨度（span）或没有（自动）的网格确定位置，也可以通过容器的 grid-template-areas 取值
- 层级控制
  - z-index:因为网格项位置是由网格线决定的,所以可以设置为有重叠,此时可以用 z-index 属性来决定显示哪一个

## 与 flex 的关系:

- grid 与 flex 之间的关系并不是 a 取代 b,而是与 flex 布局互相配合，flex 是一维布局,适合局部,比如导航栏这种;而 grid 是二维布局,适合用来用整体的页面布局

## 实际应用:

### 快速实现水平垂直居中对齐

```css
.wrapper {
  height: 300px;
  border: 1px solid red;
  display: grid;
  //place-content是justify-content和align-conetent缩写
  place-content: center;
}
```

### 基本响应式

无论浏览器窗口大小,内容始终按固定比例和列数填充容器
实现:将容器设置为网格布局,设置列数,使用 grid 布局特定单位 fr 自动等分可用空间
同理:用这种方法也可以实现常见的一些两栏布局或三栏布局

```css
.container {
  border: 1px solid red;
  display: grid;
  grid-template-columns: 100px 1fr;
  grid-template-rows: 1fr;
  grid-auto-flow: column;
}
.item-a {
  background-color: aquamarine;
}
.item-b {
  background-color: rgba(255, 255, 0, 0.5);
}
```

### 容器大小未知，列根据容器宽度自动变化

实现:使用 repeat()和 auto-fit 实现容器内自动填充

```css
#wrapper {
  border: 1px solid red;
  display: grid;
  //列块自动填充
  grid-template-columns: repeat(auto-fit, 200px);
  grid-template-rows: repeat(2, 50px);
}
```

### 去除空白的响应式布局

实现:设置每个项的最小宽度是 100px,如果可用空间比这个大的话就进行等分

```css
#wrapper {
  border: 1px solid red;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  grid-template-rows: repeat(auto-fit, 50px);
  grid-auto-rows: 50px;
}
```

### 网站的整体布局

## 兼容性：

![1641453700(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1641453725555-3b34de49-ff08-4657-9bdb-2470d7b42ac5.png#clientId=u4318384d-347a-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=213&id=uf27c0c98&margin=%5Bobject%20Object%5D&name=1641453700%281%29.png&originHeight=426&originWidth=1538&originalType=binary∶=1&rotation=0&showTitle=false&size=73537&status=done&style=none&taskId=ufd416410-00da-4b62-9502-337f543e514&title=&width=769)

## 更多实例：

[https://gridbyexample.com/examples/](https://gridbyexample.com/examples/)

##
