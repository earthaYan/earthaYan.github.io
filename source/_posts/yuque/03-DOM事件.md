
---

title: 03-DOM事件

urlname: wdrznp

date: 2019-12-13 15:21:44 +0800

tags: 
  - js
categories: 前端
---
<a name="hEMkj"></a>

### 问题描述：
谈谈你对DOM事件的理解

<a name="4FrGJ"></a>

### 解决方案or思路：

1. 基本概念：DOM事件的级别
2. DOM事件模型：捕获和冒泡
3. DOM事件流
4. DOM事件捕获的具体流程
5. Event对象的常见应用
6. 自定义事件

<a name="eJDvo"></a>

### DOM事件级别：

1. DOM0级：`element.onclick=function(){}`
2. DOM1级：没有设计跟事件相关的东西，所以只有0,2,3三个事件级别
3. DOM2级：`element.addEventListener('click',function(){},true/false)`,第三个参数指定了冒泡or捕获
4. DOM3级：`element.addEventListener（'keyup',function(){},true/false）`，形式同DOM2,区别是增加了很多事件类型

<a name="MXUeN"></a>

### DOM事件模型：

1. 捕获：由上至下到目标元素
2. 冒泡：由当前（目标）元素往上
3. 如果addEventListener的最后一个参数是true则表明事件在捕获阶段触发。默认false

<a name="HZ4TP"></a>

### DOM事件流：
捕获阶段-》目标阶段-》冒泡阶段

<a name="ywPTs"></a>

### DOM事件捕获的具体流程：

1. 第一个接收到事件对象的是window,然后传给document,第三个是html标签
2. body接收，然后按照html结构一层一层向下传到目标元素

<a name="4q7WF"></a>

### DOM事件冒泡的具体流程：
和事件捕获流程相反

<a name="3ZT0w"></a>

### 如何获取body元素和html元素：

1. document.body：获取body标签
2. document.documentElement：获取html标签

<a name="9iLWm"></a>

### Event 对象的常见应用：

- Event.preventDefault():阻止默认事件，如阻止链接跳转
- Event.stopPropagation():阻止冒泡，
  - 如果父元素和子元素都注册了点击事件，执行不同的功能，该事件可以让点击子元素的同时不会冒泡执行父元素的点击事件
- Event.stopImmiadatePropagation():事件响应优先级
  - 一个按钮绑定了两个click事件，正常情况下两个函数都会被执行，加上这个方法就会按照优先级的方式先执行a，而不同时执行b事件，
- Event.target:当前被点击的元素
- Event.currentTarget:当前绑定的事件对象，父级元素绑定实践，currentTarget指的就是该父元素
  - 事件委托
  - 一个for循环给一个DOM元素注册了N多事件如何优化？
  - 用事件代理，在父元素上绑定一次事件

<a name="H4x98"></a>

### Event自定义事件：

Event和CustomEvent都是事件，用法一样，但是后者可以跟Object来做指定参数,一般与其他事件一起使用
```javascript
var ev=new Event('custom')
domElement.addEventListener('custom',function(){
  console.log('cis)
})
 ev.dispatchEvent(domElement)//触发
```
//第二个参数为对象,event.detail可用来传参数，第一个参数为自定义事件的名称<br />_event_ = new CustomEvent(_typeArg_, _customEventInit_);detail用来传参数<br />_event_ = new Event(typeArg[, eventInit]);

<a name="x156w"></a>

### 示例代码：
```javascript
  var event=new Event('test')
  event.name="lili33"
  ev.addEventListener('test',function(ev){
      console.log("自定义事件",ev)
  },true)
  ev.onclick=function(){
      ev.dispatchEvent(event)
  }
```
```javascript
  // customeEvent
  var event=new CustomEvent('test',{detail:{hazcheeseburger: true}})
  event.detail.name="lili33"
  ev.addEventListener('test',function(ev){
      console.log("自定义事件",ev)
  },true)
  ev.onclick=function(){
      ev.dispatchEvent(event)
  }
```

