---
title: yuque-hexo项目分析4
date: 2023-09-07 21:57:43
tags: [hexo]
categories: [hexo]
---

对象： sync 命令

## 主流程

1. 判断是否有合法配置
2. 删除之前生成的 posts 目录
3. 从语雀或者缓存中获取文章
   - 新建 Yuque 客户端实例
   - 根据配置初始化变量
   - 拉取文章详情
   - 生成一篇 markdown 文章
   - 获取读取文件的时间戳

## 如何从语雀或者缓存中获取文章

### 新建一个 Downloader 实例

```js
const downloader = new Downloader(initConfig);
  constructor(config) {
    this.client = new YuqueClient(config);
    // ....
    this._cachedArticles = [];
    // 拉取文章详情
    this.fetchArticle = this.fetchArticle.bind(this);
    // 全量生成所有 markdown 文章
    this.generatePost = this.generatePost.bind(this);
    this.lastGenerate = 0;
    // 读取特定路径下的文件内容，并将其解析为数字
    if (this.lastGeneratePath !== '') {
        this.lastGenerate = Number(
          fs.readFileSync(this.lastGeneratePath).toString()
        );
    }
  }
```

### YuqueClient 类

```js
constructor(config) {
    const { baseUrl, login, repo, token } = config;
    this.config = Object.assign({}, config);
    this.token = token;
    // 获取知识库地址
    this.config.namespace = `${login}/${repo}`;
    // ...
}
```

### fetchArticle 函数

作用:下载文章详情
入参:

- item:文章概要
- index:所在缓存数组下标记

返回值:
data:Promise

```js
fetchArticle(item, index) {
    const { client, _cachedArticles } = this;
    return function() {
        // ...
        return client.getArticle(item.slug).then(({ data: article }) => {
        // 修改缓存数组
        _cachedArticles[index] = article;
        });
    };
}
```

### yuqueClient 的 getArticle 函数

```js
async getArticle(slug) {
    const api = `/docs/${slug}?raw=1`;
    // 调用this._fetch方法
    const result = await this._fetch('GET', api);
    return result;
}
    // 实际请求数据函数
  async _fetch(method, api, data) {
    const { baseUrl, namespace, timeout = 10000 } = this.config;
    // 实际请求url
    const path = `${baseUrl}/repos/${namespace}${api}`;
    // ...
    try {
      const result = await urllib.request(path, {
        dataType: 'json',
        method,
        data,
        timeout,
        headers: {
          'User-Agent': 'yuque-hexo',
          'X-Auth-Token': this.token,
        },
      });
      return result.data;
    } catch (error) {
      throw new Error(`请求数据失败: ${error.message}`);
    }
  }
```

### generatePost 函数

作用:生成一篇 markdown 文章
入参:
post:文章详情

```js
  async generatePost(post) {
    if (!isPost(post)) {
        // ...不是post的处理
    }

    if (new Date(post.published_at).getTime() < this.lastGenerate) {
      //  页面没有更新,跳过
      return;
    }

    const { postBasicPath } = this;
    const { mdNameFormat, adapter } = this.config;
    // 下载的单篇最终生成的路径
    const postPath = path.join(postBasicPath, `${fileName}.md`);
    const internalAdapters = [ 'markdown', 'hexo' ];
    // 获取adapter路径
    const adpaterPath = internalAdapters.includes(adapter)
      ? path.join(__dirname, '../adapter', adapter)
      : path.join(process.cwd(), adapter);

    let transform;
    try {
      transform = require(adpaterPath);
    } 
    // 获取文章内容
    const text = await transform(post);
    // 实际写入文件
    fs.writeFileSync(postPath, text, {
      encoding: 'UTF8',
    });
  }
```
### transform函数
```js
async function(post) {
  // 语雀img转成自己的cdn图片
  if (config.imgCdn.enabled) {
    post = await img2Cdn(post);
  }
  // matter 解析
  const parseRet = parseMatter(post.body);
  const { body, ...data } = parseRet;
  const { title, slug: urlname, created_at } = post;
  const raw = formatRaw(body);
  const date = data.date || formatDate(created_at);
  const tags = data.tags || [];
  const categories = data.categories || [];
  const props = {
    title: title.replace(/"/g, ''), // 临时去掉标题中的引号，至少保证文章页面是正常可访问的
    urlname,
    date,
    ...data,
    tags,
    categories,
  };
  const text = ejs.render(template, {
    raw,
    matter: FrontMatter.stringify(props),
  });
  return text;
};
```