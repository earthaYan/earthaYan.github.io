---
title: python基础语法
tags: [Python]
categories: Python
---

## c2. 解释器

前提：安装 python 并将安装路径添加到环境变量中

### 调用解释器

#### 启动解释器方式：

1. `py xx.py` 或者 `python xx.py`
2. `python -c command [arg] ...`,命令最好用引号包裹
3. `python -m module [arg] ...`,在命令行下直接运行 Python 模块

> 区别：方法 2 是执行 command 中的语句,类似于 shell -c,方法 3 会将模块作为主程序运行，模块通过名称区分

```py
# my_module.py
def greet(name):
    print(f"Hello, {name}!")

# 外部调用
python -m my_module
```

#### 退出解释器方法：

1. `CTRL+Z`+`Enter`
2. `exit()`

#### 交互模式

1. 主提示符`>>>`:提示输入下一条指令
2. 次要提示符`...`:提示输入连续行

> 输入多行架构的语句时，要用连续行

### 解释器和环境

默认编码：UTF-8
指定编码方式：通过注释实现：`# -*- coding: encoding -*-`

> 指定编码需要和 vscode 底部的编码方式保持一致，否则会报错 SyntaxError: encoding problem: GB2312 或者乱码

```py
#!/usr/bin/env python3
# -*- coding: gb2312 -*-
```

## c3. Python 非正式介绍

### 计算器

注释：python 注释以`#`开头，直到该行结束

#### 算术运算符：`+`,`-`,`*`,`/`

特殊算术运算符：

- `//`：取整 5//2=2
- `%`：取余 5%2=1
- `**`：乘方 5\*\*2=25
- `=`：赋值 a=3

> 1. 普通除法的返回值一直是浮点数。
> 2. 交互模式下，前一次输出的表达式会赋值给变量`_`,并且避免给这个变量显式赋值

#### 文本类型 str

单行字符串：使用单引号或者双引号包裹
多行字符串：使用三重引号包裹`"""..."""`或者`'''...'''`
转义：`\`+字符
不转义：`print(r'a\b')`
合并重复: +和\*
字符串长度：`len(str1)`

> 自动合并：相邻的两个或多个 字符串**字面值** （引号标注的字符）会自动合并。

> 支持下标(正负数)访问和切片`word[0:3]`:包含 0-2 的字符的子串
> word[0:],word[-2:]包含了`stop`下标,字符串中单个字符不可修改

```py
# 3 times 'un', followed by 'ium'
3 * 'un' + 'ium'
# 输出结果：'unununium'
s='Py' 'thon'
# 输出结果：Python
```

#### 列表类型 list

使用`[]`进行包裹，支持不同类型数据组合,可以嵌套
单个元素可以通过下标或者切片修改
获取列表长度：`len(list1)`
列表末尾添加新元素：`cubes.append(216) `
合并列表:`squares + [36, 49, 64, 81, 100]`

### python 编程第一步

缩进是 python 组织语句结构的方式
print()可以传多个参数，通过`,`分隔，比如 `print('a','b')`打印出来的结果是：`a b`

## c4. 控制流

### 条件语句

```py
x=input('请输入：')
x=int(x)
if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
else:
    print('More')
```

### for 循环

形式：`for item in 列表/字符串`
注意点：

- python 本身不支持通过下标进行迭代，即`for (int i = 0; i < 10; i++)`这样的形式，而是按顺序遍历可迭代对象（如列表、字符串等）中的元素。

```py
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))
```

- 如果需要下标进行迭代的话，可使用`enumerate`将列表或字符串作为参数

```py
words = ['cat', 'window', 'defenestrate']
for index,value in enumerate(words):
    print('index',index,'value',value)
```

#### 修改迭代对象中的内容

推荐方法：迭代多项集的副本或者创建新的多项集
不推荐：通过下标修改
原因：如果在循环体中修改了该集合的内容（增删改），可能会导致迭代过程出现意外的行为。因为修改集合后，原始集合的长度和结构发生了变化，而迭代器无法正确地处理这种变化。

```py
# 正确做法
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# Strategy:  迭代副本
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# Strategy:  创建一个新的集合
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

print(users,active_users)
```

### range()函数

作用：用于生成等差数列,生成的数列左闭右开

- ``range(num)`:从 0 开始生成 0 一直到 num-1 的数列
- `range(start,end)`:从 start 开始生成一直到 end-1 的数列
- `range(start,end,step)`:从 start 开始按照 step 步长生成一直到 end-1 的数列
  应用：按照索引迭代序列

```py
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])
```

### break/continue 语句和循环上的 else 子句

break 语句：跳出最近一层的 for/while 循环
continue 语句：执行循环的下一次迭代
else 子句：for 或 while 循环可以包括 else 子句

```py
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')
```

#### for/while 中的 else 子句

else 子句和 for/while 同级

```py
# for 循环中的 else 子句
for item in iterable:
    # 循环体
else:
    # 循环正常完成时执行的逻辑

# while 循环中的 else 子句
while condition:
    # 循环体
else:
    # 循环条件为假时执行的逻辑

```

执行时机不一样
for：如果 for 循环正常完成（即**没有通过 break 语句**提前退出），则执行 else 块中的代码

```py
# for 循环中的 else 子句
for i in range(5):
    print(i)
else:
    print("For loop completed")
# 结果
0
1
2
3
4
For loop completed
```

while：如果 while 循环的条件为假，即**终止了循环（不再满足循环条件）**，则执行 else 块中的代码.同样如果中途有 break 语句则不会执行 else 子句

```py
# while 循环中的 else 子句
x = 0
while x < 5:
    print(x)
    x += 1
else:
    print("While loop condition is false")
```

### pass 语句

不执行任何动作。
使用场景：语法上需要语句，但程序不需要执行任何动作

1. 在定义一个函数或类时，如果函数或类体内还没有具体的实现，可以使用 pass 语句来占位

```py
def my_function():
    pass

class MyClass:
    pass
```

2. 开发过程中，当你想跳过某些代码块的执行时，可以使用 pass 语句作为占位符，以后再进行实现

```py
if condition_1:
    # 处理condition_1的情况
elif condition_2:
    pass  # 暂时不需要处理condition_2的情况
else:
    # 处理其他情况
```

### match 语句

作用：接受一个表达式并把它的值与一个或多个 case 块给出的一系列模式进行比较
本质：模式匹配
如果都不匹配，会执行`case _`,这个相当于 js 中的 default 分支

```py
def http_error(status):
    match status:
        case 400|500:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"

def http_error2(point):
    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")
# http_error2((0,3)) =>Y=3
```

> Todo:此处需要二次学习

### 定义函数

形式：`def funcName(形参列表)`
函数体第一条语句为字符串的时候，它就是`docstring`。作用是自动生成在线文档或打印版文档，还可以让开发者在浏览代码时直接查阅文档

```py
def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

# Now call the function we just defined:
fib(2000)
```

- 返回值：return 语句返回函数的值。return 语句不带表达式参数时，返回 None。函数执行完毕退出也返回 None
- 实参：按值调用 进行传递

> 此处值指的始终是对象的 引用 而不是对象的值

### 定义函数 2

#### 默认参数值

用于：函数定义

```py
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)
```

调用方式：

1. 只给出必选实参：`ask_ok('Do you really want to quit?')`
2. 给出一个可选实参：`ask_ok('OK to overwrite the file?', 2)`
3. 给出所有实参：`ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')`

> 默认参数值只在函数定义之前生效

```py
i = 5

def f(arg=i):
    print(arg)

i = 6
f() #此时结果为5
```

#### 关键字参数

在函数调用中前面带有标识符（例如 name=）或者作为包含在前面带有 \*\* 的字典里的值传入
用于：函数调用

> positional 参数 vs keyword 参数

```py
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")

# 有效调用
parrot(1000)                                          # 1 positional argument
parrot(voltage=1000)                                  # 1 keyword argument
parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword
# 无效调用
parrot()                     # required argument missing
parrot(voltage=5.0, 'dead')  # non-keyword argument after a keyword argument
parrot(110, voltage=220)     # duplicate value for the same argument
parrot(actor='John Cleese')  # unknown keyword argument
```

##### 调用约定

1. 调用时，关键字参数必须跟在位置参数后面
2. 关键字参数都必须匹配定义时候的参数名称
3. 不能对同一个参数多次赋值
4. 最后一个形参为`**name`形式的时候，接收一个字典 dict
5. `**name` 形参可以与 `*name` 形参组合使用（`*name` 必须在 `**name` 前面）， `*name` 形参接收一个 元组，该元组包含形参列表之外的位置参数。

```py
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")
```

#### 特殊参数

1. 函数定义中未使用`/`和`*`时，参数按照位置或关键词传递给函数
2. 仅限位置传参：`/`
3. 仅限关键字传参：`*`

```py
# 正常传参
def standard_arg(arg):
    print(arg)
# 仅限使用位置形参
def pos_only_arg(arg, /):
    print(arg)
# 仅限关键词传参
def kwd_only_arg(*, arg):
    print(arg)
# 混合使用
def combined_example(pos_only, /, standard, *, kwd_only):
    print(pos_only, standard, kwd_only)

#报错：combined_example() takes 2 positional arguments but 3 were given
combined_example(1, 2, 3)
#正确：1，2，3
combined_example(1, 2, kwd_only=3)
#正确：1，2，3
combined_example(1, standard=2, kwd_only=3)
#报错：combined_example() got some positional-only arguments passed as keyword arguments: 'pos_only'
combined_example(pos_only=1, standard=2, kwd_only=3)

```

```bash
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        Positional or keyword   |
        |                                - Keyword only
         -- Positional only
```

#### 任意实参列表

`*args` 形参后的任何形式参数只能是仅限关键字参数，即只能用作关键字参数，不能用作位置参数：

```py
def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))
```

#### 解包实参列表

使用场景：函数调用要求独立的位置参数，但实参在列表或元组里
使用语法：

- `*参数`：列表/元组
- `**参数`：字典（对象）

```py
# 此处参数为列表
args = [3, 6] # args = (3, 6)也可以
list(range(*args))

# 解包字典
def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")
d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)
```

#### lambda 表达式

作用：用于创建匿名函数,常规函数定义的语法糖
语法：只能是单个表达式，返回值是是一个函数
不适合场景：创建逻辑复杂的函数
例子：
`lambda a, b: a+b`函数返回两个参数之和

```py
def make_incrementor(n):
    return lambda x: x + n
f = make_incrementor(42)
f(0) #42
f(1) #43
```

#### 文档字符串

特殊注释形式，对函数、类、模块等代码元素进行文档说明
访问：`__doc__`
作用：

1. 自动生成代码的 api 文档
2. 提供代码使用说明
3. 提供内部实现说明

docstring 约定：

- 多行时，隔一行应为空白行
- 必须以大写字符开头，以`.`结尾

#### 函数注解

作用：为函数参数和返回值添加元数据或类型提示

> 不会影响函数的实际行为，而是提供了额外的信息，可以被工具、IDE 和静态类型检查器等利用
> 函数注解使用`冒号（:）`后跟一个表达式来指定注解的内容。通常，注解可以是一个类型，也可以是任何其他有效的 Python 表达式。
> 和 TS 区别：这个不会影响运行，且不会强制执行

```py
def greet(name) :
    return f"Hello, {name}!"

def greet(name: str) -> str:
    return f"Hello, {name}!"
# 鼠标悬浮到函数名称上可发现第一个里面的name显示为any类型
# 第二个显示为str
```

## c5. 数据结构

### 列表

1. list.append(x)：末尾添加元素，`a[len(a):] = [x] `
2. list.extend(iterable)：用可迭代对象的元素扩展列表。 `a[len(a):] = iterable `
3. list.insert(index, value):指定位置插入元素
4. list.remove(x):从列表中删除第一个值为 x 的元素。未找到指定元素时，触发 ValueError 异常
5. list.pop([index]):删除列表中指定位置的元素，并返回被删除的元素。未指定位置时，a.pop() 删除并返回列表的最后一个元素,[]表示这是个可选参数
6. list.clear():删除列表里的所有元素
7. list.index(x[, start[, end]]):返回列表中第一个值为 x 的元素的零基索引.未找到指定元素时，触发 ValueError 异常。
   > 可选参数 start 和 end 是切片符号，用于将搜索限制为列表的特定子序列。返回的索引是相对于整个序列的开始计算的，而不是 start 参数。
8. list.count(x):返回列表中元素 x 出现的次数
9. list.sort(\*, key=None, reverse=False):就地排序列表中的元素
10. list.reverse():反转列表元素
11. list.copy()：返回列表的浅拷贝。相当于 a[:]

#### 实现堆栈

特点：先进后出
借助 append 和 pop 方法

#### 实现队列

特点：先进先出
借助 collections.deque

#### 列表推导式

概念：通过对现有列表进行迭代和筛选，快速生成一个新的列表

```py
squares = []
for x in range(10):
    squares.append(x**2)

# squares->[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

语法：new_list = `[表达式 for 变量 in 列表 if 条件]`

```py
numbers = [1, 2, 3, 4, 5]
squared_numbers = [num**2 for num in numbers if num % 2 == 0]
print(squared_numbers)  # 输出: [4, 16]

tuple=[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
# tuple值：[(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```

列表推导式可嵌套

```py
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
a= [[row[i] for row in matrix] for i in range(4)]
# [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

#### 字典推导式

作用：从列表中构建字典
语法：`{key的表达式:值的表达式 for 变量 in 字典 if 条件}`

```py
mydic={num:num**2 for num in range(1,6) if num%2==0}
```

#### set 集合推导式

作用：从列表中构建集合
语法：`{表达式 for 变量 in 集合 if 条件}`

### del 语句

按索引而不是值从列表中移除条目

```py
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
# a:[1, 66.25, 333, 333, 1234.5]
del a[2:4]
# a:[1, 66.25, 1234.5]
del a[:]
# a:[]
del a
# 删除整个变量，之后不能再使用
```

### 元组和序列

序列：列表、字符串、元组、range
形式：元组由多个用逗号隔开的值组成

```py
t = 12345, 54321, 'hello!'
u = t, (1, 2, 3, 4, 5)
print(u)

```

元组可嵌套，所以上述最终结果为`((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))`

#### 元组和列表区别

1. 元组是不可变的，适合存储一些不希望被修改的数据，如坐标、日期等
2. 列表是可修改的，适合存储一些需要频繁修改的数据
3. 元素在内存占用和访问上更有优势

### 集合

概念：由不重复元素组成的无序容器
作用：

1. 消除重复元素

```py
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
print(basket)
# {'apple', 'pear', 'orange', 'banana'}
a = set('abracadabra')
print(a)
# {'c', 'a', 'b', 'd', 'r'}
```

2. 成员检测

```py
isExist='orange' in basket #True
```

打印出来的值去除了重复的 apple 元素

#### 创建集合

语法：使用`set()`函数或`{}`

> 创建空集合只能用 set()方法
> `{}`创建的是空字典

```py
basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}
a = set('abracadabra')
```

#### 集合操作

1. `a-b`：差集，从 a 中去除 b 后剩余的集合
2. `a|b`: 并集
3. `a&b`: 交集
4. `a^b`: 异或

#### 集合推导式

```py
a = {x for x in 'abracadabra' if x not in 'abc'}
# {r,d}
```

### 字典

本质：键值对 的集合，但键必须唯一
作用：通过 key 存取值
删除：使用 `del`，
返回所有键的列表：`list(dic)`,按插入次序排列
检查字典里是否有某个键：使用`in`关键字

#### 创建字典

1. 字面值创建
2. dict()函数：`dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])`

#### 字典推导式

{x: x\*\*2 for x in (2, 4, 6)}
结果：{2: 4, 4: 16, 6: 36}

### 循环技巧

1. items()方法：字典提取键及其对应的值

```py
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)
```

2. enumerate()方法：在集合中同时取出位置索引和对应的值

```py
for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)
```

3. zip()方法：同时循环两个或多个序列时，将其内的元素一一匹配

```py
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))
# q,a分别是2个列表的对应元素
```

### 条件控制 deep

1. in & not in：成员检测
2. is & is not：比较两个对象是否是同一个对象
3. 所有比较运算符优先级相同且低于任何数值运算符
4. 比较运算符支持链式操作
   > a < b == c 校验 a 是否小于 b，且 b 是否等于 c。
5. 比较操作可以用布尔运算符 `and` 和 `or` 组合，并且，比较操作（或其他布尔运算）的结果都可以用 `not` 取反。not 的优先级最高， or 的优先级最低。
6. and/or 是短路运算符，从左到右，一旦可以确定结果，求值就会立刻停止

赋值：

1. 普通赋值
2. 海象运算符：`:=`
   > 第二种主要用于同时存在赋值和比较的情况

## c6. 模块

### 什么是模块

把各种定义存入一个文件，在脚本或解释器的交互式实例中使用。这个文件就是 **模块**
使用：模块中的定义可以导入到其他模块或者主模块
命名：文件名=模块名+'.py'

### dir()函数

作用：查找模块定义的名称。返回结果是经过排序的字符串列表
有参数：查找指定模块定义的名称
无参数：列出当前已定义的名称

> 不会列出内置函数和变量的名称。这些内容的定义在标准模块 builtins 中

### 包

概念：通过使用“带点号模块名”来构造 Python 模块命名空间的一种方式
例子：模块名 `A.B` 表示名为 A 的包中名为 B 的子模块
作用：避免不同包的模块名冲突

#### 从包中导入

1. `import sound.effects.echo`
2. `from sound.effects import echo`
3. `from sound.effects import * `
   > 导入方式 3 中：模块中的所有公开对象和函数导入当前命名空间。这意味着可以直接使用模块中的对象和函数，而不需要使用模块前缀。

#### 相对导入

```py
# 绝对导入
import sound.effects.echo
import sound.effects.surround
from sound.effects import *
# 相对导入（对于 surround 模块）
from . import echo
from .. import formats
from ..filters import equalizer
```

## c7. 输入和输出

### 字符串

#### f-字符串

语法：{expression}并且在字符串前加前缀 f 或 F
例子：将 pi 舍入到小数点后三位：
`print(f'The value of pi is approximately {math.pi:.3f}.')`
特殊修饰符：
'!a' 应用 ascii()
'!s' 应用 str()
'!r' 应用 repr()
'=' 说明符可被用于将一个表达式扩展为表达式文本、等号再加表达式求值结果的形式

```py
bugs = 'roaches'
count = 13
area = 'living room'
print(f'Debugging {bugs=} {count=} {area=}')
```

#### format 方法

语法：str.format()
`print('We are the {} who say "{}!"'.format('knights', 'Ni'))`

```py
print('This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible'))
```

#### 手动格式化字符串

语法：
str.rjust():通过在左侧填充空格，对给定宽度字段中的字符串进行右对齐
str.ljust():
str.center():
str.zfill():在数字字符串左边填充零，且能识别正负号

```py
# 实现同一个平方和立方的表
for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    print(repr(x*x*x).rjust(4))

```

结果：

```sh
1   1    1
 2   4    8
 3   9   27
 4  16   64
 5  25  125
 6  36  216
 7  49  343
 8  64  512
 9  81  729
10 100 1000
```

### 文本

oepn()方法返回一个 file 对象
`f = open('workfile', 'w', encoding="utf-8")`
参数 1：文件名称
参数 2：模式，r,w,a，默认 r
借助 with 关键字，可以自动关闭文件，不需要调用 f.close()

```py
with open('workfile', encoding="utf-8") as f:
    read_data = f.read()
```

#### 文件对象的方法

读取：f.read(size),size 为负数或者不传递时，返回整个文件内容
读取单行数据：f.readLine()
读取多行数据：循环遍历
以列表形式读取整个文件的所有行：list(f)或者 f.readLines

```py
for line in f:
    print(line, end='')
```

写入：f.write(string) 把 string 的内容写入文件，并返回写入的字符数

> 写入其他类型的对象前，要先把它们转化为字符串（文本模式）或字节对象（二进制模式）

```py
value = ('the answer', 42)
s = str(value)  #将元组转换为字符串
f.write(s)
```

使用 json 保存结构化数据
json.dumps():

```py
import json
x = [1, 'simple', 'list']
json.dumps(x)
# 结果'[1, "simple", "list"]'
```

只将对象序列化为 text file:

```py
json.dump()
x = json.load(f)
```

## c8. 错误和异常

### 语法错误

运行前就可以触发
解析器会复现出现句法错误的代码行，并用小“箭头”指向行里检测到的第一个错误。错误是由箭头 上方 的 token 触发的（至少是在这里检测出的）

### 异常

运行时触发
不处理的情况下：
代码：`10 * (1/0)`

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

代码：`'2' + 2`

```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

最后一行说明程序遇到的类型错误

### 异常处理

#### try...except...else

1. 执行 try 子句（try 和 except 之间的语句）
2. 如果没有触发异常，则跳过 except 子句
3. 如果在执行 try 子句的时候发生了异常，则跳过剩下的部分。
4. 如果异常的类型和 except 关键字后指定的异常相匹配，则执行 except 子句
5. 如果不匹配，则会被传递到外部的 try 语句中，如果一直没找到，则属于未处理异常且执行将终止并输出报错信息

```py
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
```

try 语句可以有多个 except 子句处理不同的异常指定处理程序，但是最终只会执行一个。
指定多个异常：

```py
except (RuntimeError, TypeError, NameError):
```

如果发生的异常类型和 except 子句中的类是同一个类或是其基类，则两种类型兼容

```py
class B(Exception):
    pass
class C(B):
    pass
class D(C):
    pass
for cls in [B, C, D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B") # B-C-D

# ####################################
class B(Exception):
    pass
class C(B):
    pass
class D(C):
    pass
for cls in [B, C, D]:
    try:
        raise cls()
    except B:
        print("B")
    except D:
        print("D")
    except C:
        print("C")  # B-B-B

```

可选的 else 子句,必须放在 except 子句后面，适用于 try 子句 没有引发异常但又必须要执行的代码

```py
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
```

### 触发异常

raise 语句,后续的 error 必须继承自 Exception 类

```py
raise NameError('HiThere')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: HiThere
```

### 异常链

如果一个未处理的异常发生在 except 子句内，将会有被处理的异常附加到上面，并包括在错误信息中

```py
def func():
    raise ConnectionError
try:
    func()
except ConnectionError as exc:
    raise RuntimeError('Failed to open database') from exc
```

禁用自动异常链:`from None`

```py
try:
    open('database.sqlite')
except OSError:
    raise RuntimeError from None
```

### 自定义异常

1. 必须从 Exception 类继承
2. 异常类可以被定义成能做其他类所能做的任何事，但通常应当保持简单，它往往只提供一些属性，允许相应的异常处理程序提取有关错误的信息
3. 大多数异常命名都以 “Error” 结尾，类似标准异常的命名

### 定义清理操作

finally 子句,不论是否有异常，finally 都会被执行

```py
try:
    raise KeyboardInterrupt
finally:
    print('Goodbye, world!')
```

## c9. 类

作用：将数据和功能绑定在一起
特性：

1. 类的继承机制支持多个基类
2. 派生的类能覆盖基类的方法
3. 类的方法能够调用基类中的同名方法
4. 在运行时创建，创建后还可修改

### 作用域和命名空间

TODO:需要二次学习理解

### 类定义语法

```py
class 类名:
    语句
```

> TODO:与函数定义 (def 语句) 一样，类定义必须先执行才能生效。把类定义放在 if 语句的分支里或函数内部试试。[没理解]

进入类定义时，会创建一个新的命名空间，将它作为局部作用域。

### Class 对象

类对象包括两种操作：

- 属性引用：`obj.name`
- 实例化：`obj()`

```py
class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'
```

上述代码，可以通过`MyClass.i`或者`MyClass.f`进行属性引用，分别返回一个 number 和一个 function，可以通过`MyClass.i=newValue`来修改它的值，但修改后会影响实例对应的值。
可以通过`MyClass()`进行实例化,返回一个类对象，可赋值给变量。本质是创建一个空对象。

#### 希望通过指定初始状态创建实例

方法：定义`__init__()`方法

```py
class A:
    def __init__(self,data):
        self.data=data
```

### 实例对象

作用:属性引用-数据属性+方法

### 方法对象

MyClass.f：函数对象
m.f:方法对象
区别：实例对象会作为函数的第一个参数被传入

### 类和实例变量

实例变量用于每个实例的唯一数据，而类变量用于类的所有实例共享的属性和方法
如果类定义中有同名的实例变量和类变量，各个实例将共享该变量，比如

```py
class Dog:
    tricks = []             # mistaken use of a class variable
    def __init__(self, name):
        self.name = name
    def add_trick(self, trick):
        self.tricks.append(trick)

d = Dog('Fido')
e = Dog('Buddy')
d.add_trick('roll over')
e.add_trick('play dead')
d.tricks
```

此时类的实例对象 d 和 e 共享 tricks 这个变量

#### 例外情况

如果同样的属性名称同时出现在实例和类中，则属性查找会优先选择实例:

```py
class Warehouse:
   purpose = 'storage'
   region = 'west'


w1 = Warehouse()
print(w1.purpose, w1.region)

w2 = Warehouse()
w2.region = 'east'
print(w2.purpose, w2.region)
print(w1.purpose, w1.region)
```

此时第二次的 w1.region 依旧为 west

### 继承

语法：

```py
class 类名(基类模块名.基类名):
class 类名(基类名):
    <statement-1>
    <statement-N>
```

查询属性：
如果请求的属性在类中找不到，搜索将转往基类中进行查找。 如果基类本身也派生自其他某个类，则此规则将被递归地应用。
内置函数：

1. isinstance() ：检查一个实例的类型: isinstance(obj, int) 仅会在 obj.**class** 为 int 或某个派生自 int 的类时为 True。

2. issubclass() ：检查类的继承关系: issubclass(bool, int) 为 True，因为 bool 是 int 的子类。 但是，issubclass(float, int) 为 False，因为 float 不是 int 的子类

#### 多重继承

含义：一个类继承自多个类

```py
class DerivedClassName(Base1, Base2, Base3):
    <statement-1>
    <statement-N>
```

理论上：D->B1->B1-super->B2->B2-super
实际上：方法解析顺序会动态改变以支持对 super() 的协同调用，只调用每个父类一次，并且保持单调

### 私有变量

python 不存在实际意义上的私有变量（仅限一个对象内部访问）
日常开发中会以一个**带下划线的名称**，比如`_var`来表示这个函数/方法/数据成员应该被看作是非公有部分

```py
class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)
    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # 私有化拷贝

class MappingSubclass(Mapping):
    def update(self, keys, values):
        # 提供update（）的新签名
        # 不会破坏 __init__()
        for item in zip(keys, values):
            self.items_list.append(item)
```

上面的代码中，

> 名称改写：任何形式为 `__spam` 的标识符的文本将被替换为`_classname__spam`，其中`_classname`为去除了前缀下划线的当前类名称。支持需要私有变量的场景，避免父类和子类的名称冲突

### 迭代器 iterator

{% asset_img iterator.png%}
iterable:可迭代对象
iterator:迭代器

### 生成器

```py
def func(n):
    while True:
        if n>10:
            break
        print(n)
        n+=1
func(0)
```

此时 func 函数会执行并直接输出 0-10。如果想要暂停函数并使其可以再恢复，代码修改为

```py
def func(n):
    while True:
        yield(n)
        if n>10:
            break
        print(n)
        n+=1
func(0)
```

此时执行 func 函数并不会打印出预期的内容，而是会显示信息：

> generator object func at 0x7fxxxxx

通过`type(func(0))`可以发现我们创建了一个新的对象即生成器，所以需要把返回值赋值给另一个对象保存起来，将其作为 next 函数的参数
用法：

```py
def func():
    while True:
        yield(n)
        if n>10:
            break
        n+=1

for i in func(0):
    print(i)
```

输出 0-11
结论：yield 执行之后，这个函数会立刻返回一个生成器对象，将提供给 yield 的值返回给调用者，下一次调用这个生成器对象的时候，生成器对象从 yield 之后开始执行，直到遇到下一个 yield

#### 可以做什么

还没想到

## c10. 标准库-part1

### 操作系统

来源：os 模块
作用：与操作系统交互

- os.getcwd():获取当前工作目录
- os.chdir('/server/accesslogs')：切换当前工作目录
- os.system('mkdir today')：执行系统命令
- dir(os):返回所有模块函数的列表
- help(os):返回来源模块的 docstring 的帮助页

### 文件通配符

#### 日常文件和目录管理任务：shutil

- shutil.copyfile('data.db', 'archive.db') 复制文件
- shutil.move('/build/executables', 'installdir') 移动文件

#### 通配符

glob 模块:提供了一个在目录中使用通配符搜索创建文件列表的函数
`glob.glob('*.py')`

### 命令行参数

语法：`sys.argv`
`python demo.py one two three `
结果：['demo.py', 'one', 'two', 'three']

### 错误输出重定向和程序终止

错误输出：`sys.stderr.write('Warning, log file not found starting a new one\n')`
程序终止：`sys.exit()`

### 字符串模式匹配

来源：re 模块
`re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')`
如果知识需要简单的功能，首选还是 str 模块

### 数学

math 模块：提供对浮点数学的底层 C 库函数的访问:
random 模块：提供了进行随机选择的工具
statistics 模块：计算数值数据的基本统计属性（均值，中位数，方差等

### 互联网访问

urllib.request 模块：从 URL 检索数据
smtplib 模块：用于发送邮件

### 日期和时间

datetime 模块

### 数据压缩

模块：zlib, gzip, bz2, lzma, zipfile 和 tarfile

### 质量控制

doctest 模块

```py
def average(values):
    """Computes the arithmetic mean of a list of numbers.

    >>> print(average([20, 30, 70]))
    40.0
    """
    return sum(values) / len(values)

import doctest
doctest.testmod()   #自动校验内嵌的测试
```

unittest 模块

## c11. 标准库-part2

### 格式化输出

reprlib 模块
pprint 模块
textwrap 模块
locale 模块

### 模板

string.Template:允许用户在不更改应用逻辑的情况下定制自己的应用
占位符由 $ 加上合法的 Python 标识符（只能包含字母、数字和下划线）构成。一旦使用花括号将占位符括起来，就可以在后面直接跟上更多的字母和数字而无需空格分割。$$ 将被转义成单个字符 $:

```py
t = Template('${village}folk send $$10 to $cause.')
t.substitute(village='Nottingham', cause='the ditch fund')
# Nottinghamfolk send $10 to the ditch fund.
```

### 使用二进制数据记录格式

struct 模块

### 多线程

queue 模块
threading 模块

### 日志记录

logging 模块

### 弱引用

会自动进行内存管理
场景：在对象持续被其他对象所使用时跟踪它们
weakref 模块

### 用于操作列表的工具

array 模块
collections 模块
bisect 模块
heapq 模块

### 十进制浮点运算

decimal 模块
