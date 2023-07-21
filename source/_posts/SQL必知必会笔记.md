---
title: SQL必知必会笔记
date: 2023-07-17 13:13:47
tags: [SQL]
categories: 数据库
---

## 在运行数据库增删改查脚本前预期创建一个新的数据库，报错：

> Error Code：1044，Access denied for user 'root'@'%' to database 'dbName'(Mysql::Error)

解决方法：修改 mysql 数据库下的 user 表的 root 用户权限

```bash
UPDATE mysql.user SET Grant_priv='Y', Super_priv='Y' WHERE User='root';
FLUSH PRIVILEGES;
```

## 删除行数据的时候报错：

`DELETE FROM Customers WHERE cust_id = 1000000006`

> Error Code：1142 - DELETE command denied to user 'root'@'222.71.242.202' for table 'Customers'

解决办法：

1. 查看当前登录用户信息

```SQL
SELECT
 user,
 host,
 db,
 command
FROM
 information_schema.processlist
```

结果：
user:root
host:222.71.242.202:54120
db:10Minute

2. 增加权限 `Delete_priv='Y'`

## 获取系统时间

MySQL 的日期类型有 5 个，分别是： date、time、year、datetime、timestamp。
Now(),CURRENT_TIMESTAMP(),CURRENT_DATE()

### MySQL 的日期类型如何设置当前时间为其默认值

使用 timestamp 类型，且 默认值设为 now() 或 current_timestamp()

## 存储 url

mysql 版本
低于 5.0.3：TEXT
5.0.3 及其以上：varChar(2083)

## 创建存储过程

```sql
CREATE PROCEDURE MailingListCount (OUT listCount INT)
# 存储过程体开始
BEGIN
DECLARE v_rows INT;
SELECT COUNT(*) INTO v_rows
FROM Customers
WHERE NOT cust_email IS NULL;
SET listCount=v_rows;
END;
# 存储过程体结束
```

报错：Error code:1193,Unknown system variable 'listCount'
解决：
```sql
delimiter $$
CREATE PROCEDURE MailingListCount (OUT `listCount` INT)
BEGIN
DECLARE v_rows INT; 
SELECT COUNT(*) INTO v_rows
FROM Customers
WHERE NOT cust_email IS NULL;
SET listCount=v_rows;
END $$
delimiter ;
CALL MailingListCount(@result);
SELECT @result;
```
[注意]：out参数必须以`@`开头

### 创建一个新订单
```sql
delimiter $$
CREATE PROCEDURE NewOrder(IN `cust_id` VARCHAR(10))
BEGIN
#为订单号声明一个变量
DECLARE new_order_num INT; 
# 获取当前最大订单号,决定下一个订单号
SET  new_order_num= MAX(order_num)+1;
# 插入新订单
INSERT INTO Orders(order_num, order_date, cust_id) VALUES(new_order_num, CURRENT_TIMESTAMP(),@cust_id); 
END $$
delimiter ;
```