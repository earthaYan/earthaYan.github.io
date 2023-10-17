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

### break/continue 语句和循环上的 else 子句

### pass 语句

### match 语句

### 定义函数

### 定义函数 2

#### 默认参数值

#### 关键字参数

#### 特殊参数

#### 任意实参列表

#### 解包实参列表

#### lambda 表达式

#### 文档字符串

#### 函数注解

### 代码风格

## c5. 数据结构

## c6. 模块

## c7. 输入和输出

## c8. 错误和异常

## c9. 类

## c10. 标准库-part1

## c11. 标准库-part2

## c12. 虚拟环境和包
