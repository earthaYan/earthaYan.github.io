---
title: 翻译-ES2015-Set
date: 2023-02-15 21:16:50
tags: [JavaScript]
categories: 翻译
---


原文地址：https://itnext.io/what-is-the-javascript-set-in-es2015-and-when-should-you-use-it-d7e3b8048891

# ES2015中的Set是什么以及什么时候可以使用它？
<strong>
ES2015规范引入了许多新特性，这些新特性会不断在所有新版本的浏览器中被采用，Set集合就是这些新特性之一。
</strong>


我的第一想法就是，好吧我可以使用一个普通的数组！但是这篇文章里我会展示可以用Set集合做什么。

##  什么是 ES2015 Set?
`Set`是什么？你可以用它来做什么？Mozilla文档关于这一点说得很清晰：

>  `Set` 集合可以存储任意类型的唯一值，无论是原始类型还是引用类型。

这个特殊对象可以像普通对象一样存储所有种类的值，但是他们必须是唯一的，重复的值会被过滤出去。

感谢Addy Osmani的推特,让我发现了 `Set()`!

>小提示: JavaScript的 `Array.from()` 接受第二个参数，是一个`map`函数 。用于调用你创建的数组的每个元素。 
> {% asset_img array_from.jpg %}


从JavaScript中过滤出重复值一直都很麻烦，你需要自己循环整个数组计算出来，现在`Set` 让这件事变得容易了 😁。

## 向 Set 中添加数据
目前有几种方法来向`Set`集合中添加数据。
### 作为参数传递
这是一个将数据作为参数添加到 `Set` 集合的例子：
```javascript
const numbersSet = new Set([1,2,3,4,5]);
const stringSet = new Set(['Jan', 'Rick', 'Raymon', 'Tim']);
const objectSet = new Set([{a: 1, b: 2}]);
const arraySet = new Set([['javascript', 'coffeescript'], ['css', 'sass']]);
```

###  通过add方法添加数据
另外一种传递数据到`Set`集合的方法是使用 `add()` 

```javascript
const newSetObject = new Set();
newSetObject.add('Raymon');
newSetObject.add({a: 1, b: 2});
newSetObject.add(1).add(2).add(3).add(4).add(5)
// Result: Raymon, {a: 1, b: 2}, 1, 2, 3, 4, 5
```

##  使用has()检查Set中值
`Set`集合有一个非常方便的方法用来检查对象内部是否有某个值

```javascript
const numbersSet = new Set([1,2,3,4,5]);
const stringSet = new Set(['Jan', 'Rick', 'Raymon', 'Tim']);
const objectSet = new Set([{a: 1, b: 2}]);
const arraySet = new Set([['javascript', 'coffeescript'], ['css', 'sass']]);
    
numberSet.has(4); // true
numberSet.has(6); // false
stringSet.has('Raymon'); // true
objectSet.has({a: 1, b: 2}); // false
arraySet.has('css'); // false
```

`has()` 方法在原始值上非常奏效，但是在像对象和数组这样的非原始值上不起作用。

关于非原始值不能和原始值一样起作用是有原因的。因为 `has()`方法不止比较值，他同时还会用===操作符比较引用。

如果你在变量中有对数组或者对象的引用，那么结果就会和预期一样：
```javascript
const exampleObject = {a: 1, b: 2};
const exampleArray1 = ['javascript', 'coffeescript']
const exampleArray2 = ['css', 'sass'];
const objectSet = new Set([exampleObject]);
const arraySet = new Set([exampleArray1, exampleArray2]);
    
objectSet.has({a: 1, b: 2}); // false
objectSet.has(exampleObject); // true
arraySet.has('css'); // false
arraySet.has(exampleArray1); // true
arraySet.has(exampleArray2); // true
```

所以记住：当你在`Set`集合中使用`has()`方法的时候,引用非原始值很重要。

## 从Set中移除数据
向 Set 集合中添加数据很简单，删除数据也很容易。

### 使用delete方法移除数据

如果想要移除`Set`集合中的单个元素，只需要简单地使用移除方法
```javascript
const numbersSetObject = new Set([1,2,3,4,5,6,7,8,9]);
numbersSetObject.has(2); // true
numbersSetObject.delete(2);
numbersSetObject.has(2); // false
console.log(numbersSetObject); // 1,3,4,5,6,7,8,9
```

### 用clear方法移除所有元素
但是如果你想要从Set集合中移除所有数据，只能使用clear方法
```javascript
const numbersSetObject = new Set([1,2,3,4,5,6,7,8,9]);
numbersSetObject.has(2); // true
numbersSetObject.clear();
console.log([...numbersSetObject]); // []
```
## 使用size属性检查元素数量

类似在数组中，使用length属性检查元素数量，Set集合也可以用size属性实现同样的目的
如果我们检查上一个例子中检查Set集合，他的size是7。
```javascript
newSetObject.size // 7
```
## 过滤重复的原始值

如果尝试把重复的原始值放入Set,最后保留下来的只有唯一的一个。

```javascript
const uniqueArray = new Set([1,2,2,2,3,4,5,5,6,7,9,9,8]);
console.log('uniqueArray: ', uniqueArray)
// unique: 1, 2, 3, 4, 5, 6, 7, 9, 8
```
## 过滤非原始类型值

在过滤重复的非原始值的时候情况有点不同.文档十分清晰,Set本身并没有比较对象，而是比较引用。

将它看作是使用==操作符比较值，但是使用===操作符会比较引用和值。

如果我们尝试向Set放入具有不同引用的两个相同的对象，是没有问题的。

```javascript
const objectSet = new Set([{a: 1, b: 2}, {a: 1, b: 2}]);
console.log('objectSet: ', objectSet);
// objectSet: {a: 1, b: 2}, {a: 1, b: 2};
```
但是如果我们放入相同引用的两个相同的对象会发生什么呢？
```javascript
const demoObject = {a: 1, b: 2};
const objectSet = new Set([demoObject, demoObject]);
console.log('objectSet: ', objectSet);
// objectSet: {a: 1, b: 2};
```
希望你已经猜到结果了：objectSet只包含了一个demoObject，去除了另外一个重复的😁

## 循环一个 Set
Set的好处之一就是你可以循环一个Set集合

这个文档解释了更多关于Set方法的细节：
> Set 是值的集合. 你可以按照插入顺序遍历其中的元素。

To loop over a Set collection we can use the for-of loop and the forEach method which is attached to the Set.

我们可以通过for-of和附加到Set集合的forEach 方法来循环一个Set集合。
### forEach 方法循环

通过`Set.forEach()`,你可以循环Set集合中的所有元素。

```javascript
const objectSet = new Set([{a: 1, b: 2}, {a: 1, b: 2}]);
objectSet.forEach(object => {
    console.log('Object: ', object);
})
    
// result:  
// Object:  {a: 1, b: 2}
// Object:  {a: 1, b: 2}
```


### 使用 for-of 
通过for-of循环，我们有一些方法可以遍历Set集合内部的所有元素。
-   entries()
-   keys()
-   values()

```javascript
const objectSet = new Set([{a: 1, b: 2}, {a: 1, b: 2}]);
for (let [key, value] of objectSet.entries())  {
   console.log(key);
}
    
// {a: 1, b: 2}
// {a: 1, b: 2}
```
唯一奇怪的事情是： entries, keys 和 values方法在Set上会返回完全相同的结果。也许是因为 Set 和 Map Api有许多共同之处。

## Set和Map的区别
map和set最大的区别是：Set看上去非常像一个数组，而map看上去更像一个对象。
