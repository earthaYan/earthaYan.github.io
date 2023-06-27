---
title: 如何做自己的github介绍页面
date: 2023-06-27 20:03:55
tags: [github]
categories: github
---

## 流程

1. 新建同名仓库，比如 GitHub 的用户名是`earthaYan`，则新建仓库`earthaYan`，而不是`earthaYan.github.io`
2. 新建时仓库选择 public 并且生成 README.md
3. 编辑 README 文件

## 文章编辑

### 添加 banner 图片

```html
<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="https://github.com/earthaYan/earthaYan/blob/main/3072.webp"
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="https://github.com/earthaYan/earthaYan/blob/main/3072.webp"
  />
  <img
    alt="Shows an illustrated sun in light mode and a moon with stars in dark mode."
    src="https://github.com/earthaYan/earthaYan/blob/main/3072.webp"
  />
</picture>
```

### 添加 github stats

```md
[![earthaYan的 GitHub](https://github-readme-stats.vercel.app/api?username=earthaYan&show_icons=true&title_color=fff&icon_color=79ff97&text_color=9f9f9f&bg_color=151515)](https://github.com/earthaYan)
```
### 添加使用的语言
```md
<a href="#"><img src="https://github-readme-stats-crlnmfdzg-tifan.vercel.app/api/top-langs/?username=earthaYan&langs_count=8&layout=compact" height="160" /></a>
```

### 添加技能
```md
[![My Skills](https://skillicons.dev/icons?i=go,docker,express)](https://skillicons.dev)
```
## 参考链接

[manage github profile](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)
[github stats](https://github.com/anuraghazra/github-readme-stats)
[emoji](https://www.webfx.com/tools/emoji-cheat-sheet/)
[skills icon](https://github.com/tandpfun/skill-icons)