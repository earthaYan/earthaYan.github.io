---
title: SQL必知必会笔记
date: 2023-07-17 13:13:47
tags: [SQL]
categories: 数据库
---

在运行数据库增删改查脚本前预期创建一个新的数据库，报错：

> Error Code：1044，Access denied for user 'root'@'%' to database 'dbName'(Mysql::Error)

解决方法：修改 mysql 数据库下的 user 表的 root 用户权限

```bash
UPDATE mysql.user SET Grant_priv='Y', Super_priv='Y' WHERE User='root';
FLUSH PRIVILEGES;
```
