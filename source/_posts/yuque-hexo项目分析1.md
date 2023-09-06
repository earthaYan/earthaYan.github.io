---
title: yuque-hexo项目分析1
date: 2023-09-06 10:33:23
tags: [hexo]
categories: [hexo]
---

对象：package.json 文件

## 概念

本质就是一个 JSON 对象，对象中的每一个字段对应项目的一个设置

## 作用

1. 定义项目所需要的各种模块
2. 定义项目的配置信息(比如名称、版本、许可证等元数据)
3. `npm install`命令根据这个配置文件，自动下载所需的模块(配置项目所需的运行和开发环境)

## 普通字段

```json
{
  "name": "yuque-hexo", //项目名称
  "version": "1.9.5", //项目版本
  "author": "张三", //项目作者
  "description": "A downloader for articles from yuque", //项目简要描述
  "keywords": ["hexo", "sync"], //项目的关键字数组
  "homepage": "https://github.com/earthaYan/todo-with-go", //项目的主页地址
  "repository": "https://github.com/earthaYan/todo-with-go", //项目的代码仓库地址。
  "bugs": "https://github.com/earthaYan/todo-with-go/issues", //用于报告bug的地址,通常是github的issue
  "license": "MIT", //项目使用的许可证
  "contributors": [{ "name": "李四", "email": "lisi@example.com" }], //项目的贡献者列表
  "engines": {
    "node": ">=12.0.0"
  }, //指定项目运行所需的Node.js和npm版本范围
  "browserslist": ["last 2 versions", "> 5%", "not dead"], //指定项目支持的浏览器范围
  "peerDependencies": "" //指定项目对其他模块的依赖关系
}
```

### version

结构：`大版本.次要版本.小版本`

### keywords

作用：

1. 便于项目其他开发者理解
2. 更容易被搜索引擎发现
3. 发布项目到 npm 的时候，会使用该字段对包进行分类和标记，便于使用者搜索和筛选

### license

- MIT License(MIT): 宽松的许可证，允许用户以任何目的使用、复制、修改、合并、发布、分发和销售软件
- Apache License 2.0(Apache-2.0): 宽松的许可证，类似于 MIT License，但包含了对专利权的明确规定
- GNU General Public License (GPL-3.0): 强 copyleft 许可证，要求任何使用或修改了软件的派生作品也必须以相同的许可证方式进行发布
- BSD License(BSD-2-Clause): 灵活的许可证，提供了更多的自由度，允许用户在闭源产品中使用和分发软件
- Creative Commons Licenses(CC-BY、CC-BY-SA): 一系列不同类型的许可证，用于保护各种类型的作品，如文档、图片、音乐等

### engines

作用：规定项目运行的环境和版本
结构：对象，key 表示运行环境，value 表示最低版本，可以有多个

```json
"engines": {
  "node": ">=12.0.0",
  "npm": ">=6.0.0",
  "yarn":">=1.22.0"
}
```

使用对象：

1. 使用者：告诉使用者项目需要的最低运行环境和版本，让用户在安装和运行前检查自己的环境
2. 构建工具(npm、yarn 等)：利用 engines 字段进行环境检查和验证。当使用者尝试安装项目时，构建工具会检查运行环境是否满足 engines 字段指定的要求。如果不满足要求，构建工具通常会发出警告或阻止安装，以避免潜在的兼容性问题。

> 【注意】：engines 字段本身并不直接影响项目的运行。它只是为使用对象提供了一种指导和约束机制，确保项目在合适的环境下运行

### browserslist

作用：配置目标浏览器和环境，告诉相关工具(Autoprefixer、babel-preset-env 等)要支持哪些浏览器和环境

#### 配置语法

1. 指定浏览器名称
2. 指定浏览器版本范围
3. 市场份额以及区域条件
4. 逻辑运算符
5. 自定义查询规则

```json
"browserslist": [
  "last 2 versions",
  "> 5%",
  "Firefox >= 46",
  "IE 11",
  "not IE <= 10",
  "not dead"
]

// 自定义查询规则,必须在顶层 browserslist 字段之前定义
"customConfig": [
  "last 2 Chrome versions",
  "not Chrome < 60"
]
"browserslist": [
  "extends customConfig",
  "Firefox ESR"
]
```

## 重点字段

```json
{
  "bin": {
    "yuque-hexo": "bin/yuque-hexo.js"
  }, //指定各个内部命令对应的可执行文件的位置
  "main": "index.js",
  "scripts": {
    "build": "webpack",
    "test": "jest",
    "start": "node server.js"
  } //脚本命令
}
```

### bin

#### 作用：

1. 关联命令行工具(CLI)和特定的可执行文件
2. 在安装包时自动将命令添加到系统的 PATH 中，从而可以在终端中直接运行这些命令

#### 形式：

1. 字符串形式
   适用场景：包只提供一个全局命令，并且这个命令的名称与包的名称相同
   > 假设包名为 `"my-package"`，并且只有一个全局命令 `"my-command"`，它与可执行文件 `bin/my-command.js` 相关联。在这种情况下，bin 字段可使用字符串形式：
   > 语法：`"bin": "./bin/my-command.js"`
2. 对象形式
   适用场景：包提供多个命令或命令的名称与包的名称不同
   语法：
   ```json
   "bin": {
   "command1": "./bin/command1.js",
   "command2": "./bin/command2.js"
   }
   ```

#### 原理：

npm 会寻找该文件

1. 在运行 `npm install -g `或`yarn global add `安装包时，就会自动将 `my-command` 命令添加到系统的 `PATH `中。可以在终端中直接使用 `my-command` 命令来调用这个文件
2. 在运行`npm install xx`时，在 node_modules/.bin/目录下建立符号链接。由于`node_modules/.bin/`目录会在运行时加入系统的`PATH`变量，因此在运行`npm run xx`时，就可以不带路径，直接通过命令来调用这些脚本

### main

#### 作用：

当前项目作为一个包被其他项目引用时,指定模块的入口文件，比如项目读取到`require('moduleName')`就会加载这个文件

> [注意]：对于当前项目内部而言，main 字段并不是必须的。开发者可以直接通过指定文件路径来运行项目的入口文件

#### 形式

1. 字符串形式:`"main": "src/index.js"`
2. 默认值：`index.js`、`index.json`、`index.node`

### scripts

#### 作用：

指定了运行脚本命令的 npm 命令行缩写

#### 形式：

键值对形式,多个命令通过`&&`串联

### dependencies vs devDependencies

dependencies：核心依赖项，项目在运行时所依赖的包。包括框架、库、工具等
devDependencies：只在开发过程中需要的包，通常是开发工具、测试框架、代码检查工具等
区别:npm install --production 会只安装核心依赖 dependencies

#### 版本限定

1. 指定版本：1.2.2
2. ~1.2.2：安装时不改变大版本号和次要版本号，只升级最后一位的小版本，即安装 1.2.x 的最新版
3. ^1.2.3: 安装时不改变大版本号，只升级最后的小版本，即安装 1.x.x 的最新版
4. latest: 安装最新版本

> 通过`package-lock.json`或者`yarn.lock`可以保证每个开发环境都安装相同的依赖项

### peerDependencies

#### 作用

指定项目所依赖的外部包或库的最低版本

1. 声明对其他包或库的依赖关系：通过列出需要的外部包或库的名称和版本范围，peerDependencies 告诉用户或开发者你的包需要依赖这些特定版本的包或库。
2. 避免重复安装：如果一个包已经被项目的上层依赖项安装了，那么在当前包的 peerDependencies 中声明依赖可以避免重复安装该包的多个副本
3. 提示用户手动安装依赖项：如果用户在安装你的包时没有安装它所依赖的外部包或库，npm 会提醒用户手动安装这些依赖项

#### 适用场景：项目的包需要依赖特定版本的依赖，但是又不希望其包含在自身的 dependencies
1. 开发库或者插件
2. 开发框架或者工具
```json
  "peerDependencies": {
    "react": ">=16.0.0",
    "react-dom": ">=16.0.0"
  }
```

当其他开发者安装当前项目时，如果他们没有已经安装过符合要求的 react 和 react-dom，则会收到 npm 的提示，告诉他们手动安装这些依赖项

> 在运行 yarn install 命令时，peerDependencies 中的依赖项不会被自动安装到 node_modules 目录下

## 关于项目

- bin 字段配置为`bin/yuque-hexo.js`说明执行`yuque-hexo xx`命令的时候会执行 bin 目录下的`yuque-hexo.js`文件
- main 字段配置为`index.js`说明该模块的入口文件是根目录下的`index.js`文件

### scripts 字段

```json
{
  "scripts": {
    "clean": "rimraf coverage",
    "lint": "eslint .",
    "test": "npm run lint -- --fix && npm run test-local",
    "test-local": "egg-bin test",
    "cov": "egg-bin cov",
    "ci": "npm run clean && npm run lint && egg-bin cov"
  }
}
```

本项目定义了 6 个脚本命令，其中最后一个 ci 命令是前几个命令的串联。

#### clean 命令

`rmiraf`是一个 nodejs 模块，用于删除文件和目录，类似于 Linux 系统的 `rm -rf`,此处指的是删除 coverage 这个文件夹

#### lint 命令

执行`eslint .`命令，根据项目根目录下的`.eslintrc`文件对当前目录下的所有 JS 文件执行 ESLint 检查，给出相应的警告或错误信息，找到代码中的潜在问题

#### test 命令

串联了 lint 命令和 test-local 命令，其中 lint 命令带了`--fix`参数,表示会自动修复一些问题。然后执行 test-local 命令

#### test-local 命令

使用了`egg-bin`命令行工具，`egg-bin test`主要用于运行 Egg.js 框架的测试,内部使用的是 mocha。

#### cov 命令

`egg-bin cov`生成和报告代码的覆盖率信息,会生成 coverage 目录。不带参数默认会执行项目中所有的测试文件(以.test.js,.spec.js 结尾的文件)


## 依赖项

**dependencies:**
- `@yuque/sdk`: 版本号为1.1.1的yuque SDK。
- `ali-oss`: 版本号为6.17.0的阿里云 OSS SDK。
- `chalk`: 版本号为2.4.1的终端样式库。
- `common-bin`: 版本号为2.7.3的通用命令行库。
- `cos-nodejs-sdk-v5`: 版本号为2.11.6的腾讯云 COS SDK。
- `debug`: 版本号为3.1.0的调试工具。
- `depd`: 版本号为2.0.0的轻量级依赖包。
- `ejs`: 版本号为3.1.6的模板引擎。
- `filenamify`: 版本号为4.1.0的文件名处理工具。
- `hexo-front-matter`: 版本号为0.2.3的Hexo前置元数据解析器。
- `html-entities`: 版本号为1.2.1的HTML实体编码和解码工具。
- `lodash`: 版本号为4.17.10的实用工具库。
- `mkdirp`: 版本号为1.0.0的递归创建目录工具。
- `moment`: 版本号为2.22.2的日期时间处理库。
- `prettier`: 版本号为2.0.4的代码格式化工具。
- `qiniu`: 版本号为7.4.0的七牛云 SDK。
- `queue`: 版本号为4.5.0的队列操作库。
- `rimraf`: 版本号为2.6.2的递归删除文件和目录工具。
- `superagent`: 版本号为7.0.2的HTTP请求库。
- `update-check`: 版本号为1.5.3的更新检查工具。
- `upyun`: 版本号为3.4.6的又拍云 SDK。
- `urllib`: 版本号为2.29.1的HTTP请求库。

**devDependencies:**
- `coffee`: 版本号为5.1.0的CoffeeScript编译器。
- `egg-bin`: 版本号为4.8.3的Egg.js命令行工具。
- `egg-ci`: 版本号为1.8.0的Egg.js持续集成工具。
- `eslint`: 版本号为5.4.0的ESLint代码规范工具。
- `eslint-config-egg`: 版本号为7.1.0的Egg.js的ESLint配置。
