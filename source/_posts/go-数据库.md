---
title: go-数据库
date: 2023-01-12 15:13:00
tags: [数据库, GoLang]
categories: [GoLang]
---
##   mysql

```go
package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}
func useMysql() {
	// 打开一个注册过的数据库驱动,第二个参数为data source name
	db, err := sql.Open("mysql", "root:123456@tcp(116.204.108.126:3306)/test?charset=utf8")
	checkErr(err)
	// 插入数据
	// 返回准备要执行的sql操作，然后返回准备完毕的执行状态
	stmt, err := db.Prepare("INSERT INTO userinfo SET username=?,department=?,created=?")
	checkErr(err)
	// 执行stmt准备好的SQL语句
	// 传入的参数都是=?对应的数据
	res, err := stmt.Exec("amy", "研发部门", "2012-12-09")
	checkErr(err)
	id, err := res.LastInsertId()
	checkErr(err)
	fmt.Println(id)
	// 修改数据
	stmt, err = db.Prepare("update userinfo set username=? where uid=?")
	checkErr(err)
	res, err = stmt.Exec("astaxieupdate", id)
	checkErr(err)
	affect, err := res.RowsAffected()
	checkErr(err)
	fmt.Println(affect)
	// 查询数据
	// 直接执行Sql返回Rows结果
	rows, err := db.Query("SELECT * FROM userinfo")
	checkErr(err)
	for rows.Next() {
		var uid int
		var username string
		var department string
		var created string
		err = rows.Scan(&uid, &username, &department, &created)
		checkErr(err)
		fmt.Println(uid)
		fmt.Println(username)
		fmt.Println(department)
		fmt.Println(created) 
	}
	// 删除数据
	stmt, err = db.Prepare("delete from userinfo where uid=?")
	checkErr(err)
	res, err = stmt.Exec(id)
	checkErr(err)
	affect, err = res.RowsAffected()
	checkErr(err)
	fmt.Println(affect)
	db.Close() //关闭数据库连接
}
```
### sql.Open第二参数形式
```bash
user@unix(/path/to/socket)/dbname?charset=utf8
user:password@tcp(localhost:5555)/dbname?charset=utf8
user:password@/dbname
user:password@tcp([de:ad:be:ef::ca:fe]:80)/dbname
```
### 常用方法
- sql.Open()：打开一个注册过的数据库驱动
- db.Prepare()：返回准备要执行的sql操作，然后返回准备完毕的执行状态
- db.Query()：用来直接执行Sql返回Rows结果
- stmt.Exec()：用来执行stmt准备好的SQL语句

> 传入的参数都是=?对应的数据，可以一定程度上防止SQL注入

#### 必须引入的两个包
1. 	"database/sql"
2.  _ "github.com/go-sql-driver/mysql" //驱动

## SQLite
### 必须导入的包
- "database/sql"
- _ "github.com/mattn/go-sqlite3" //驱动
### 和mysql区别
导入驱动：`db, err := sql.Open("sqlite3", "./foo.db")`

## PostgreSQL
### 必须导入的包
- "database/sql"
- _ "github.com/lib/pq" //驱动

### 和mysql区别
1. PostgreSQL是通过$1,$2这种方式来指定要传递的参数，而不是MySQL中的?
2. sql.Open中的dsn信息的格式也与MySQL的驱动中的dsn格式不一样

```go
func usePostgreSQL() {
	connStr := "postgres://postgres:123456@116.204.108.126:3306/test?sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	checkErr(err)
	// 插入数据
	stmt, err := db.Prepare("INSERT INTO userinfo(username,department,created) VALUES($1,$2,$3) RETURNING uid")
	checkErr(err)
	res, err := stmt.Exec("astaxie", "研发部门", "2012-12-09")
	checkErr(err)
	var lastInsertId int
	err = db.QueryRow("INSERT INTO userinfo(username,department,created) VALUES($1,$2,$3) returning uid;", "astaxie", "研发部门", "2012-12-09").Scan(&lastInsertId)
	checkErr(err)
	fmt.Println("最后插入id =", lastInsertId, res)
	// 修改数据
	stmt, err = db.Prepare("update userinfo set username=$1 where uid=$2")
	checkErr(err)
	res, err = stmt.Exec("astaxieupdate", lastInsertId)
	checkErr(err)
	affect, err := res.RowsAffected()
	checkErr(err)
	fmt.Println(affect)

	// 查看数据
	rows, err := db.Query("SELECT * FROM userinfo")
	checkErr(err)
	for rows.Next() {
		var uid int
		var username string
		var department string
		var created string
		err = rows.Scan(&uid, &username, &department, &created)
		checkErr(err)
		fmt.Println(uid)
		fmt.Println(username)
		fmt.Println(department)
		fmt.Println(created)
	}
	// 删除数据
	stmt, err = db.Prepare("delete from userinfo where uid=$1")
	checkErr(err)
	res, err = stmt.Exec(lastInsertId)
	checkErr(err)
	affect, err = res.RowsAffected()
	checkErr(err)
	fmt.Println(affect)
	db.Close()
}
```