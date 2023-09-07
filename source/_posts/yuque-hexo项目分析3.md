---
title: yuque-hexo项目分析3
date: 2023-09-07 20:16:04
tags: [hexo]
categories: [hexo]
---

对象： clean 命令

### 主要步骤

1. 加载`package.json`,初始化配置
2. 清理生成的 post 目录
3. 清理 post 的数据缓存
4. 删除最新的时间戳文件

### 主要代码

```js
const Command = require("common-bin");
// initComnfig是一个包含加载的配置信息的对象
const initConfig = require("../config"); // 初始化 config
const cleaner = require("../lib/cleaner");
const out = require("../lib/out");

class CleanCommand extends Command {
  constructor(rawArgv) {
    super(rawArgv);
    this.usage = "Usage: yuque-hexo clean";
  }

  async run() {
    if (!initConfig) {
      process.exit(0);
    }
    cleaner.cleanPosts();
    cleaner.clearCache();
    cleaner.clearLastGenerate();
    out.info("yuque-hexo clean done!");
  }
}

module.exports = CleanCommand;
```

#### 引用的文件: lib/cleaner.js

- 删除 posts 文件夹

```js
cleanPosts() {
    // 从配置中获取post文件夹的路径
    const { postPath } = config;
    // 得到完整路径
    const dist = path.join(cwd, postPath);
    // 以同步阻塞的方式删除文件夹
    rimraf.sync(dist);
},
```

- 删除文章数据的缓存文件

```js
clearCache() {
    const cachePath = path.join(cwd, 'yuque.json');
    try {
        fs.unlinkSync(cachePath);
    } catch (error) {
        out.warn(`remove empty yuque.json: ${error.message}`);
    }
}
```

- 删除时间戳文件
```js
clearLastGenerate() {
    const { lastGeneratePath } = config;
    if (!lastGeneratePath) {
        return;
    }
    const dist = path.join(cwd, lastGeneratePath);
    rimraf.sync(dist);
}
```
