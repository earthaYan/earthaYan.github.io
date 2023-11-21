## 主要文件和文件夹

1. scaffolds 文件夹：新建文章时，Hexo 会根据 scaffold 来创建文件
2. source 文件夹：存放用户资源，该目录下除了\_post 其他以下划线开头的文件(夹)都会被忽略
3. themes 文件夹：存放主题，Hexo 根据主题生成静态页面
4. \_config.yml：网站的配置信息

## 配置

### 网站

| 参数     | 描述                                     |
| -------- | ---------------------------------------- |
| title    | 网站标题                                 |
| subtitle | 网站副标题                               |
| language | 网站使用的语言,常见的有 zh-Hans 和 zh-CN |

### 网址

| 参数               | 描述                          | 默认值                    | 备注                                 |
| ------------------ | ----------------------------- | ------------------------- | ------------------------------------ |
| url                | 网址                          |                           |                                      |
| root               | 网站根目录                    | url 的 pathname           |                                      |
| permalink          | 文章的永久链接格式            | :year/:month/:day/:title/ | 或者在每篇文章的 Front-matter 中指定 |
| permalink_defaults | 永久链接中各部分的默认值      |                           |                                      |
| pretty_urls        | 改写 permalink 的值来美化 URL |                           |                                      |

> 如果网站存放在子目录中，例如 http://example.com/blog,则 url 设为 http://example.com/blog, root 设为 /blog/。

### 目录

| 参数         | 描述                           | 默认值     |
| ------------ | ------------------------------ | ---------- |
| source_dir   | 资源文件夹                     | source     |
| tag_dir      | 标签文件夹                     | tags       |
| public_dir   | 公共文件夹，存放生成的站点文件 | public     |
| archive_dir  | 归档文件夹                     | archives   |
| category_dir | 分类文件夹                     | categories |

### 文章

| 参数              | 描述                         | 默认值    |
| ----------------- | ---------------------------- | --------- |
| new_post_name     | 新文章的文件名称             | :title.md |
| default_layout    | 预设布局                     | post      |
| auto_spacing      | 在中文和英文之间加入空格     | false     |
| render_drafts     | 显示草稿                     | false     |
| post_asset_folder | 启动 Asset 文件夹            | false     |
| relative_link     | 把链接改为与根目录的相对位址 | false     |
| highlight         | 代码块的高亮                 |           |
| prismjs           | 代码块的设置                 |           |
| external_link     | 在新标签中打开链接           | true      |

### 分类&标签

| 参数             | 描述     | 默认值        |
| ---------------- | -------- | ------------- |
| default_category | 默认分类 | uncategorized |
| category_map     | 分类别名 |               |
| tag_map          | 标签别名 |               |

### 日期时间格式

| 参数        | 描述     | 默认值     |
| ----------- | -------- | ---------- |
| date_format | 日期格式 | YYYY-MM-DD |
| time_format | 时间格式 | HH:mm:ss   |

### 分页

| 参数           | 描述             | 默认值 |
| -------------- | ---------------- | ------ |
| per_page       | 每页显示的文章量 | 10     |
| pagination_dir | 分页目录         | page   |

> per_page 设置为 0 则表示关闭分页功能

### 扩展

| 参数         | 描述           | 备注                                               |
| ------------ | -------------- | -------------------------------------------------- |
| theme        | 当前主题名称   | false 时禁用主题                                   |
| theme_config | 主题的配置文件 | 放置的配置会覆盖主题目录下的 \_config.yml 中的配置 |
| deploy       | 部署相关设置   |                                                    |

### 文件的包含与排除

1. include: 处理
2. exclude: 不处理
3. ignore: 忽略

> 1 和 2 只对 source/目录生效，3 会应用到所有文件夹

### 主题配置

通常情况下，Hexo 主题是一个独立的项目，并拥有一个独立的 \_config.yml 配置文件
优先级：
Hexo 配置文件中的 theme_config > \_config.[theme].yml 文件 > 主题目录下的 \_config.yml 文件

## 命令

- hexo init:新建 hexo 网站
- hexo new [layout] title：
  - 作用：新建一篇文章,默认的 layout 是 post
  - 注意点：如果标题包含空格的话，用引号括起来
- hexo new page -path about/me "About me"
  - 创建一个`source/about/me.md`文件，同时 Front Matter 中的 title 为 "About me"
- hexo generate：
  - 生成静态文件
  - (-d)参数表示文件生成后立刻部署网站
- hexo publish [layout] <fileName>:发表草稿
- hexo server:启动服务器
- hexo deploy:
  - 作用：部署网站
  - (-g)参数表示部署之前预先生成静态文件
- hexo render <file1> [file2]:渲染文件
- hexo clean:清理缓存文件(db.json)和已经生成的静态文件
- hexo list:列出网站数据
- hexo version:显示 hexo 版本
- hexo --draft:显示 source/\_drafts 文件夹中的草稿文章

## Layout

| 布局  | 路径            |
| ----- | --------------- |
| post  | source/\_posts  |
| page  | source          |
| draft | source/\_drafts |

> 用户自定义的其他布局和 post 相同，都将储存到 source/\_posts 文件夹

## Front-matter

文章最上方用`---`分隔的区域，用于指定当前文章的变量

| 参数       | 描述               |
| ---------- | ------------------ |
| layout     | 布局               |
| title      | 标题               |
| date       | 创建日期           |
| updated    | 更新日期           |
| updated    | 更新日期           |
| tags       | 标签               |
| categories | 分类               |
| permalink  | 覆盖文章的永久链接 |
| excerpt    | 纯文本的页面摘要   |
| published  | 文章是否发布       |

## 分类和标签

分类：具有顺序性和层次性,不支持同级多个标签
标签：不具备上述性质

```sh
categories:
- Diary
tags:
- PS3
- Games
```

## 资源文件夹

- Asset ：source 文件夹中除了文章以外的所有文件
- 文章资源文件夹：\_post/title 文件夹，`post_asset_folder:true`
  > 将所有与当前文章有关的资源放在这个关联文件夹中之后，就可以通过相对路径来引用它们，比如`{% asset_img slug [title] %}`

## 设置主题

使用 npm 方式安装，并新建`_config.themeName.yaml`文件
