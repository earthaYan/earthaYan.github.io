---
title: hexo-deploy-github-443
date: 2022-09-14 12:34:21
tags: [部署]
categories: hexo
---
>18 files changed, 191 insertions(+), 191 deletions(-)
> ERROR: Repository not found.
> fatal: Could not read from remote repository.
> Please make sure you have the correct access rights
and the repository exists.
> FATAL Something's wrong. Maybe you can find the solution here: https://hexo.io/docs/troubleshooting.html      
> error Command failed with exit code 2.
> info Visit https://yarnpkg.com/en/docs/cli/run for documentation about this command.
问题:使用了https
解决方法:
修改.config.yml文件,使用ssh
```yml
deploy:
  type: 'git'
  repo:
    github: git@github.com:earthaYan/earthaYan.github.io.git
  branch: master
```
对比图:
{% asset_img diff.jpg  对比 %}