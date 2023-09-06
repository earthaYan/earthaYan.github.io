---
title: yuque-hexo项目分析2
date: 2023-09-06 22:31:36
tags: [hexo]
categories: [hexo]
---

对象：index.js 入口文件

```javascript
"use strict";

const path = require("path");
const Command = require("common-bin");

class MainCommand extends Command {
  constructor(rawArgv) {
    super(rawArgv);
    this.usage = "Usage: yuque-hexo <command>";

    //加载名为command的子命令并传递子命令所在文件的路径
    this.load(path.join(__dirname, "command"));
  }
}
module.exports = MainCommand;
```

用到的 nodejs 库：path,common-bin

## common-bin

### 作用：
快速创建和管理命令行工具
### 特点：
1. 自定义命令的类需要继承自 Command
2. 一个命令类包含两部分
   - 构造函数
   - run 函数
3. 尖括号（<>）常用于表示必需的参数或占位符
### 构造函数的参数rawArgv：
是一个表示原始命令行参数的数组，来源于`process.argv`属性
#### 例子：
```bash
node mycommand subcommand --option1 value1 --option2 value2
```
此时，`process.argv`的值如下，`rawArgv`参数值此时和它保持一致
```js
[
  'node',
  '/path/to/mycommand',
  'subcommand',
  '--option1',
  'value1',
  '--option2',
  'value2'
]
```
### 示例

```javascript
// 引入所需的模块
const { Command } = require("common-bin");
// 定义了一个名为MyCommand的类
class MyCommand extends Command {
  // 构造函数
  //  
  constructor(rawArgv) {
    super(rawArgv);
    // this.usage属性定义命令行工具的使用方法。
    this.usage = "Usage: mycommand <command>";
    // 定义子命令subcommand，并关联SubCommand类
    this.load("subcommand", SubCommand);
  }
  //   run函数处理命令行工具的主要逻辑
  *run({ argv }) {
    console.log("My command executed with args:", argv._);
  }
}
// 定义了另一个名为SubCommand的类
class SubCommand extends Command {
  constructor(rawArgv) {
    super(rawArgv);
    this.usage = "Usage: mycommand subcommand";
    // ...
  }
  *run({ argv }) {
    console.log("Sub command executed with args:", argv._);
  }
}
module.exports = MyCommand;
```
