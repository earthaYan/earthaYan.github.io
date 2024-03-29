---
title: gorm学习笔记
date: 2023-03-21 12:58:53
tags: [GoLang]
categories: 后端
---

## 安装

```bash
go get -u gorm.io/gorm
# 安装对应数据库驱动，比如mysql,sqlite
go get -u gorm.io/driver/mysql
```

## 常见用法

```go
package main

import (
  "gorm.io/gorm"
  "gorm.io/driver/sqlite"
)

type Product struct {
  gorm.Model
  Code  string
  Price uint
}

func main() {
  // 连接数据库
  db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
  if err != nil {
    panic("failed to connect database")
  }

  // 迁移 schema：保持数据库和程序数据结构始终保持一致
  db.AutoMigrate(&Product{})

  // Create ：创建一条数据库记录
  db.Create(&Product{Code: "D42", Price: 100})

  // Read ：查询数据库记录
  var product Product
  db.First(&product, 1) // 根据整型主键查找
  db.First(&product, "code = ?", "D42") // 查找 code 字段值为 D42 的记录

  // Update ：修改数据库单条记录，将 product 的 price 更新为 200
  db.Model(&product).Update("Price", 200)
  // Update - 更新多个字段
  db.Model(&product).Updates(Product{Price: 200, Code: "F42"}) // 仅更新非零值字段
  db.Model(&product).Updates(map[string]interface{}{"Price": 200, "Code": "F42"})
  // Delete：软删除数据库单条记录， 删除 product
  db.Delete(&product, 1)
}
```

## 约定

约定优于配置

1. GORM 使用 ID 做主键
2. GORM 使用结构体名称`UserTable`的蛇形复数`user_tables`作为表名，字段名的蛇形`created_at`作为列名
3. GORM 使用 CreatedAt,UpdatedAt 字段追踪创建时间和更新时间
4. 可修改默认配置,具体见[修改默认配置](https://gorm.io/zh_CN/docs/conventions.html)

## gorm.Model

本质：一个 struct 结构体

```go
// gorm.Model 的定义
type Model struct {
  ID        uint           `gorm:"primaryKey"`
  CreatedAt time.Time   //在创建、更新、删除时自动填充当前时间
  UpdatedAt time.Time
  DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

## 控制字段级的读写权限

默认可导出字段在进行 CRUD 的时候拥有全部权限。使用自动迁移创建表的时候，不会创建被忽略的字段

```go
type User struct {
  Name string `gorm:"<-:create"` // 允许读和创建
  Name string `gorm:"<-:update"` // 允许读和更新
  Name string `gorm:"<-"`        // 允许读和写（创建和更新）
  Name string `gorm:"<-:false"`  // 允许读，禁止写
  Name string `gorm:"->"`        // 只读（除非有自定义配置，否则禁止写）
  Name string `gorm:"->;<-:create"` // 允许读和写
  Name string `gorm:"->:false;<-:create"` // 仅创建（禁止从 db 读）
  Name string `gorm:"-"`  // 通过 struct 读写会忽略该字段
  Name string `gorm:"-:all"`        // 通过 struct 读写、迁移会忽略该字段
  Name string `gorm:"-:migration"`  // 通过 struct 迁移会忽略该字段
}
```

## 嵌入结构体

### 匿名字段

```go
type User struct {
  gorm.Model
  Name string
}
// 等效于
type User struct {
  ID        uint           `gorm:"primaryKey"`
  CreatedAt time.Time
  UpdatedAt time.Time
  DeletedAt gorm.DeletedAt `gorm:"index"`
  Name string
}
```

### 正常结构体字段

1. 通过标签 `embedded` 将其嵌入

```go
type Author struct {
    Name  string
    Email string
}

type Blog struct {
  ID      int
  Author  Author `gorm:"embedded"`
  UpVotes int32
}
// 等效于
type Blog struct {
  ID    int64
  Name  string
  Email string
  UpVotes  int32
}
```

2. 使用标签 embeddedPrefix 来为 db 中的字段名添加前缀

```go
type Author struct {
    Name  string
    Email string
}
type Blog struct {
  ID      int
  Author  Author `gorm:"embedded;embeddedPrefix:author_"`
  UpVotes  int32
}
// 等效于
type Blog struct {
  ID          int64
  AuthorName string
  AuthorEmail string
  UpVotes  int32
}
```

## 字段标签 tag

声明 model 时，tag 是可选的,使用`camelCase`风格
标签名|说明|
-|-|
column| 指定 db 列名
type| 列数据类型，推荐使用兼容性好的通用类型，例如：所有数据库都支持 bool、int、uint、float、string、time、bytes 并且可以和其他标签一起使用，例如：not null、size, autoIncrement… 像 varbinary(8) 这样指定数据库数据类型也是支持的。在使用指定数据库数据类型时，它需要是完整的数据库数据类型，如：MEDIUMINT UNSIGNED not NULL AUTO_INCREMENT
serializer| 指定将数据序列化或反序列化到数据库中的序列化器, 例如: serializer:json/gob/unixtime
size| 定义列数据类型的大小或长度，例如 size: 256
primaryKey| 将列定义为主键
unique| 将列定义为唯一键
default| 定义列的默认值
precision| 指定列的精度
scale| 指定列大小
not null| 指定列为 NOT NULL
autoIncrement| 指定列为自动增长
autoIncrementIncrement| 自动步长，控制连续记录之间的间隔
embedded| 嵌套字段
embeddedPrefix |嵌入字段的列名前缀
autoCreateTime |创建时追踪当前时间，对于 int 字段，它会追踪时间戳秒数，您可以使用 nano/milli 来追踪纳秒、毫秒时间戳，例如：autoCreateTime:nano
autoUpdateTime |创建/更新时追踪当前时间，对于 int 字段，它会追踪时间戳秒数，您可以使用 nano/milli 来追踪纳秒、毫秒时间戳，例如：autoUpdateTime:milli
index |根据参数创建索引，多个字段使用相同的名称则创建复合索引，查看 索引 获取详情
uniqueIndex |与 index 相同，但创建的是唯一索引
check |创建检查约束，例如 check:age > 13，查看 约束 获取详情
<- |设置字段写入的权限， <-:create 只创建、<-:update 只更新、<-:false 无写入权限、<- 创建和更新权限
-> |设置字段读的权限，->:false 无读权限
\- |忽略该字段，- 表示无读写，-:migration 表示无迁移权限，-:all 表示无读写迁移权限
comment| 迁移时为字段添加注释

## 连接到数据库

目前支持数据库类型：MySQL, PostgreSQL, SQLite, SQL Server,clickHouse 和 TiDB

### 以 mysql 为例

#### 简单型

```go
  dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
  db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
```

#### 高级配置型

DNS 参数配置参考[go-sql-driver](https://github.com/go-sql-driver/mysql#parameters)
mysql 配置可参考[go-gorm/mysql](https://github.com/go-gorm/mysql)

```go
db, err := gorm.Open(mysql.New(mysql.Config{
  // 此处
  DSN: "gorm:gorm@tcp(127.0.0.1:3306)/gorm?charset=utf8&parseTime=True&loc=Local", // DSN data source name
  DefaultStringSize: 256, // string 类型字段的默认长度
  DisableDatetimePrecision: true, // 禁用 datetime 精度，MySQL 5.6 之前的数据库不支持
  DontSupportRenameIndex: true, // 重命名索引时采用删除并新建的方式，MySQL 5.7 之前的数据库和 MariaDB 不支持重命名索引
  DontSupportRenameColumn: true, // 用 `change` 重命名列，MySQL 8 之前的数据库和 MariaDB 不支持重命名列
  SkipInitializeWithVersion: false, // 根据当前 MySQL 版本自动配置
  DriverName:"自定义mysql驱动名称"
}), &gorm.Config{})
```

#### 通过一个现有的数据库连接来初始化 \*gorm.DB

```go
import (
  "database/sql"
  "gorm.io/driver/mysql"
  "gorm.io/gorm"
)

sqlDB, err := sql.Open("mysql", "mydb_dsn")
gormDB, err := gorm.Open(mysql.New(mysql.Config{
  Conn: sqlDB,
}), &gorm.Config{})

```

## 增加

### 通过数据的指针创建

```go
user:=User{Name:"yueyueyan",Age:19,Birthday:time.Now()}
result:=db.Create(&user)
```

返回结果
user.ID：返回插入数据的主键
result.Error ：返回 error
result.RowsAffected ： 返回插入记录的条数

### 用指定的字段创建记录

```go
db.Select("Name", "Age", "CreatedAt").Create(&user)//创建指定字段的记录
// INSERT INTO `users` (`name`,`age`,`created_at`) VALUES ("j", 18, "2020-07-04 11:05:21.775")
db.Omit("Name", "Age", "CreatedAt").Create(&user)//创建忽略指定字段的记录
// INSERT INTO `users` (`birthday`,`updated_at`) VALUES ("2020-01-01 00:00:00.000", "2020-07-04 11:05:21.775")
```

### 批量添加

原理:将切片传给 Create 方法
注意：使用 CreateBatchSize 选项初始化 GORM 时，所有的创建& 关联 INSERT 都将遵循该选项

> 比如 gorm.Config 中 CreateBatchSize 设置为 1000，则之后所有数据插入都要遵循这个值
> `users = [5000]User{{Name: "jinzhu", Pets: []Pet{pet1, pet2, pet3}}...}`
> 则 users 需要批量插入 5 次,pets 需要批量插入 15 次

```go
var users = []User{{Name: "j1"}, {Name: "j2"}, {Name: "j3"}}
db.Create(&users)

for _, user := range users {
  user.ID // 1,2,3
}
```

### 创建钩子

支持的钩子函数：BeforeSave, BeforeCreate, AfterSave, AfterCreate
跳过钩子函数：`DB.Session(&gorm.Session{SkipHooks: true}).Create(&user)`

#### 根据 Map 创建

- 根据`map[string]interface{}`创建

```go
db.Model(&User{}).Create(map[string]interface{}{
  "Name": "jinzhu", "Age": 18,
})
```

- 根据`[]map[string]interface{}{}`创建

```go
db.Model(&User{}).Create([]map[string]interface{}{
  {"Name": "jinzhu_1", "Age": 18},
  {"Name": "jinzhu_2", "Age": 20},
})
```

### 使用 SQL 表达式、Context Valuer 创建记录

暂时忽略

## 查询

### 获取单条记录：

- First() 获取第一条记录[主键升序]
- Take() 获取一条记录
- Last（）获取最后一条记录[主键降序]
- 检查 ErrRecordNotFound 错误
  `errors.Is(result.Error, gorm.ErrRecordNotFound)`
- 避开 ErrRecordNotFound 错误
  `db.Limit(1).Find(&user)`
- Fist 和 Last 方法生效条件
  1. 指向目标 struct 的指针作为参数传入方法
  2. 使用`db.Model()`指定 model
- 如果没有定义主键,则按照第一个字段排序

```go
var user  User
var users []User
// 生效，满足条件1
// 查询users表中按user struct 主键id排列的第一条记录
db.First(&user)
// 生效，满足条件2
result := map[string]interface{}{}
db.Model(&User{}).First(&result)
// 不生效
result := map[string]interface{}{}
db.Table("users").First(&result)
// 使用Take生效
result := map[string]interface{}{}
db.Table("users").Take(&result)

```

### 按照主键获取

1. 主键是数值:使用内联条件

```go
db.First(&user, 10)
db.First(&user, "10")//查询id为10的第一条记录
db.Find(&users, []int{1,2,3}) //查询id在1,2,3中的记录
```

2. 主键是字符串:有 sql 注入风险

```go
// 搜索id为1bxx-xx-xx的用户记录
db.First(&user, "id = ?", "1b74413f-f3b8-409f-ac47-e8c062e3472a")
```

### 检索全部对象

```go
// result.RowsAffected :返回找到的记录条数
// result.Error: 返回错误
result := db.Find(&users)
```

### 条件

#### string 条件

```go
//查询name等于jinzhu的第一条记录
db.Where("name = ?", "jinzhu").First(&user)
// 查询name不等于jinzhu的所有记录
db.Where("name <> ?", "jinzhu").Find(&users)
// 查询name为jinzhu或者 jinzhu 2的所有记录
db.Where("name IN ?", []string{"jinzhu", "jinzhu 2"}).Find(&users)
// 模糊匹配,查询name包含jin的所有记录
db.Where("name LIKE ?", "%jin%").Find(&users)
// 查询name为jinzhu并且age>=22的所有记录
db.Where("name = ? AND age >= ?", "jinzhu", "22").Find(&users)
// 查询更新时间大于上周的所有记录
db.Where("updated_at > ?", week(now())-1).Find(&users)
// 查询上周和今天之间创建的所有记录
db.Where("created_at BETWEEN ? AND ?", lastWeek, today).Find(&users)
```

如果设置了对象的主键,则与查询条件构成 AND 关系

#### struct&Map 条件

```go
// struct:查询Name为jinzhu,年龄为20的按主键id升序的第一条记录
db.Where(&User{Name: "jinzhu", Age: 20}).First(&user)
// Map：查询name为jinzhu,年龄为20的所有记录
db.Where(map[string]interface{}{"name": "jinzhu", "age": 20}).Find(&users)
// 查询id为20/21/22的所有记录
db.Where([]int64{20, 21, 22}).Find(&users)
// 不支持零值,查询name为jinzhu的所有记录
db.Where(&User{Name: "jinzhu", Age: 0}).Find(&users)
// 支持零值
db.Where(map[string]interface{}{"Name": "jinzhu", "Age": 0}).Find(&users)

```

#### 指定结构体查询字段

```go
// 查询名称为jinzhu,Age为0的用户
db.Where(&User{Name: "jinzhu"}, "name", "Age").Find(&users)
// 查询年龄为0的所有记录
db.Where(&User{Name: "jinzhu"}, "Age").Find(&users)
// SELECT * FROM users WHERE age = 0;

```

#### 内联条件

内联指的是将查询条件嵌入到 First 等方法中,达到与 where 相似的效果

```go
db.First(&user, "id = ?", "string_primary_key")
db.Find(&user, "name = ?", "jinzhu")
db.Find(&users, "name <> ? AND age > ?", "jinzhu", 20)
// struct
db.Find(&users, User{Age: 20})
// map
db.Find(&users, map[string]interface{}{"age": 20})
```

#### Not 条件 和 Or 条件

```go
// Not
// 查询name不为jinzhu的第一条记录
db.Not("name = ?", "jinzhu").First(&user)
// 查询name不为jinzhu或者jinzhu 2的所有记录
db.Not(map[string]interface{}{"name": []string{"jinzhu", "jinzhu 2"}}).Find(&users)
// 查询name不为jinzhu并且Age不为18的第一条记录
db.Not(User{Name: "jinzhu", Age: 18}).First(&user)
// 查询主键id不在1,2,3的第一条记录
db.Not([]int64{1,2,3}).First(&user)
// Or
// 查询role是admin或者role是super_admin的第一条记录
db.Where("role = ?", "admin").Or("role = ?", "super_admin").Find(&users)
// 查询name为jinzhu,或者name为jinzhu2并且Age为18的所有记录
// struct:
db.Where("name = 'jinzhu'").Or(User{Name: "jinzhu 2", Age: 18}).Find(&users)
// map:
db.Where("name = 'jinzhu'").Or(map[string]interface{}{"name": "jinzhu 2", "age": 18}).Find(&users)

```

#### 选择特定字段 Select 方法

```go
// 从users表中查询name,age字段
db.Select("name", "age").Find(&users)
db.Select([]string{"name", "age"}).Find(&users)
db.Table("users").Select("COALESCE(age,?)", 42).Rows()
```

### 排序

默认升序

```go
// age降序,name升序返回所有记录
db.Order("age desc, name").Find(&users)
db.Order("age desc").Order("name").Find(&users)
// SQL语句：不常用~SELECT * FROM users ORDER BY FIELD(id,1,2,3)
db.Clauses(clause.OrderBy{
  Expression: clause.Expr{SQL: "FIELD(id,?)", Vars: []interface{}{[]int{1, 2, 3}}, WithoutParentheses: true},
}).Find(&User{})
```

### Limit&Offset

#### Limit

作用:指定返回记录的最大值
Limit(-1):取消 limit 限制

```go
// 从users表查询3条记录
db.Limit(3).Find(&users)
// 从users1表查询10条记录，从users2表中查询所有记录
db.Limit(10).Find(&users1).Limit(-1).Find(&users2)

```

#### Offset

作用:指定在开始返回记录之前要跳过的记录数量
Offset(-1)：取消 Offset 限制

```go
// 从第四条开始返回记录
db.Offset(3).Find(&users)
db.Limit(10).Offset(5).Find(&users)
db.Offset(10).Find(&users1).Offset(-1).Find(&users2)
```

offset 具体效果：

{% asset_img no_offset.jpg %}
{% asset_img offset.jpg %}

### Group By &Having

#### Group By：Group()

作用：将具有相同值的行分组到汇总行中，例如“查找每个国家的客户数”。

```go
type result struct {
  Date  time.Time
  Total int
}
// SELECT name, sum(age) as total FROM `users` WHERE name LIKE "group%" GROUP BY `name` LIMIT 1
// as关键字用于重命名列或表
db.Model(&User{}).Select("name, sum(age) as total").Where("name LIKE ?", "group%").Group("name").First(&result)
rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Rows()
```

#### Having

作用：where 的替代品，因为 where 不能和聚合函数一起使用,所以使用 having 子句来设置条件
聚合函数：

- AVG - 计算一组值或表达式的平均值。
- COUNT - 计算表中的行数。
- INSTR - 返回字符串中第一次出现的子字符串的位置。
- SUM - 计算一组值或表达式的总和。
- MIN - 在一组值中找到最小值
- MAX - 在一组值中找到最大值

```go

db.Model(&User{}).Select("name, sum(age) as total").Group("name").Having("name = ?", "group").Find(&result)
db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Scan(&results)
rows, err := db.Table("orders").Select("date(created_at) as date, sum(amount) as total").Group("date(created_at)").Having("sum(amount) > ?", 100).Rows()

```

### Distinct

作用：查询去重,只保留一个
只根据查询字段去重:
{% asset_img distinct1.jpg %}{% asset_img distinct2.jpg %}{% asset_img distinct3.jpg %}{% asset_img distinct4.jpg %}

```go
db.Distinct("name", "age").Order("name, age desc").Find(&results)
```

### Join

外键列：数据库中的公共列
作用：指定 joins 条件，基于表之间的公共列的值在一个（自连接）或更多表之间链接数据
存在表：t1,t2

- cross join 笛卡尔积 —— 结果集包括 t1 表中行和 t2 表中行的组合->`SELECT t1.id, t2.id FROM t1 CROSS JOIN t2; `
- inner join —— 必须有一个连接字段条件,结果集包括满足该条件的 t1 和 t2 行的组合-> `SELECT t1.id, t2.id FROM t1 INNER JOIN t2 ON t1.pattern = t2.pattern; `
- left join —— 必须有一个条件,结果集包含左表 t1 的所有数据和满足条件的 t2 的行的组合 `SELECT t1.id, t2.id FROM t1 LEFT JOIN t2 ON t1.pattern = t2.pattern;`,此处比 inner join 多一个 1,null
- right join —— 同 left join 相反，结果集包含右表 t2 的所有数据

```go
type result struct {
  Name  string
  Email string
}
db.Model(&User{}).Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&result{}) //users表，左连接
rows, err := db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Rows()//users表，右连接
db.Table("users").Select("users.name, emails.email").Joins("left join emails on emails.user_id = users.id").Scan(&results)
// 带参数的多重join
db.Joins("JOIN emails ON emails.user_id = users.id AND emails.email = ?", "jinzhu@example.org").Joins("JOIN credit_cards ON credit_cards.user_id = users.id").Where("credit_cards.number = ?", "411111111111").Find(&user)
```

#### Join 预加载

```go
// SELECT users.id,users.name,users.age,Company.id AS Company__id,Company.name AS Company__name FROM users LEFT JOIN companies AS Company ON users.company_id = Company.id;
db.Joins("Company").Find(&users)
// SELECT users.id,users.name,users.age,Company.id AS Company__id,Company.name AS Company__name FROM users INNER JOIN  companies AS Company  ON users.company_id = Company.id;
db.InnerJoins("Company").Find(&users)
// 条件连接
// SELECT users.id,users.name,users.age,Company.id AS Company__id,Company.name AS Company__name FROM users LEFT JOIN companies AS Company  ON users.company_id = Company.id AND Company.alive = true;
db.Joins("Company", db.Where(&Company{Alive: true})).Find(&users)
```

#### Scan()

把结果扫描到一个 struct,和 Find()方法类似

```go
type Result struct {
  Name string
  Age  int
}
var result Result
db.Table("users").Select("name", "age").Where("name = ?", "Antonio").Scan(&result)
// Raw SQL
db.Raw("SELECT name, age FROM users WHERE name = ?", "Antonio").Scan(&result)
```

## 高级查询

### 自动选择字段

手动：使用 Select()方法选择特定字段
自动：将需要选择的字段放在一个 struct 中

```go
type User struct {
  ID     uint
  Name   string
  Age    int
  Gender string
  // 假设后面还有几百个字段...
}
type APIUser struct {
  ID   uint
  Name string
}
// 查询时会自动选择 `id`, `name` 字段
db.Model(&User{}).Limit(10).Find(&APIUser{})
// SELECT id, name FROM users LIMIT 10

```

### Locking

Gorm 支持多种类型的锁
锁：和表关联的标志，

- 针对会话
- 防止其他会话在特定时间段内访问同一个表。
- 客户端会话只能为自己获取或释放表锁。它无法获取或释放其他会话的表锁

#### 读锁-共享锁 (表锁)

语法：

- 显式上锁：`LOCK TABLES table_name READ`
- 隐式上锁：`select `
- 解锁：`UNLOCK TABLES; `

约束：

1. 当在 A 会话中设置了 READ 锁，则 A 会话中插入数据会报错
2. 当在 A 会话中设置了 READ 锁，会话 B 依然可以从表中读取数据
3. 当在 A 会话中设置了 READ 锁，会话 B 如果要插入数据，会进入等待状态，直至 A 会话中的锁被释放
4. 如果会话终止，则隐式释放所有锁

#### 写锁-排他锁 (表锁)

语法：

- 显式上锁：`LOCK TABLE table_name WRITE;`
- 隐式上锁：`insert、update、delete`
  种类：

- 约束：

1. 当在 A 会话中设置了 WRITE 锁,A 会话仍可以检索或者插入数据
2. 当在 A 会话中设置了 WRITE 锁,会话 B 的所有命令都会进入等待状态，直至解锁

#### 行锁

显式上锁：

- `select * from tableName lock in share mode;`//读锁/共享锁 5.7
- ``select * from tableName lock for share;`//读锁 8.0
- `select * from tableName for update;`//写锁/排他锁

解锁：

- 提交事务（commit）
- 回滚事务（rollback）
- kill 阻塞进程

---

```go
// SELECT * FROM users FOR UPDATE
db.Clauses(clause.Locking{Strength: "UPDATE"}).Find(&users)
// SELECT * FROM users FOR SHARE OF users
db.Clauses(clause.Locking{
  Strength: "SHARE",
  Table: clause.Table{Name: clause.CurrentTable},
}).Find(&users)

// SELECT * FROM users FOR UPDATE NOWAIT
db.Clauses(clause.Locking{
  Strength: "UPDATE",
  Options: "NOWAIT",
}).Find(&users)
```

### 子查询
```go
// 相当于SELECT * FROM "orders" WHERE amount > (SELECT AVG(amount) FROM "orders");
db.Where("amount > (?)", db.Table("orders").Select("AVG(amount)")).Find(&orders)
// 相当于SELECT AVG(age) as avgage FROM `users` GROUP BY `name` HAVING AVG(age) > (SELECT AVG(age) FROM `users` WHERE name LIKE "name%")

subQuery := db.Select("AVG(age)").Where("name LIKE ?", "name%").Table("users")
db.Select("AVG(age) as avgage").Group("name").Having("AVG(age) > (?)", subQuery).Find(&results)
// FROM子查询
// 相当于SELECT * FROM (SELECT `name`,`age` FROM `users`) as u WHERE `age` = 18
db.Table("(?) as u", db.Model(&User{}).Select("name", "age")).Where("age = ?", 18).Find(&User{})
```
### 多个列的IN查询
```go
// SELECT * FROM users WHERE (name, age, role) IN (("jinzhu", 18, "admin"), ("jinzhu 2", 19, "user"));
db.Where("(name, age, role) IN ?", [][]interface{}{{"jinzhu", 18, "admin"}, {"jinzhu2", 19, "user"}}).Find(&users)
```
<!-- 待补充 -->
## 修改更新
### 保存所有字段
```go
// UPDATE users SET name='jinzhu 2', age=100, birthday='2016-01-01', updated_at = '2013-11-17 21:34:10' WHERE id=111;
db.First(&user)
user.Name = "jinzhu 2"
user.Age = 100
db.Save(&user)
```
### 修改单个列
需要设置一些条件避免`ErrMissingWhereClause`错误
使用 Model 方法，并且值中有主键值时，主键将会被用于构建条件
```go
// 条件更新:UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE active=true;
db.Model(&User{}).Where("active = ?", true).Update("name", "hello")
// User 的 ID 是 `111`: UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111;
db.Model(&user).Update("name", "hello")
// 根据条件和 model 的值进行更新:UPDATE users SET name='hello', updated_at='2013-11-17 21:34:10' WHERE id=111 AND active=true;
db.Model(&user).Where("active = ?", true).Update("name", "hello")
```
### 修改多个列
根据 `struct` 更新属性，只会更新非零值的字段
```go
// 根据 `struct` 更新属性
// UPDATE users SET name='hello', age=18, updated_at = '2013-11-17 21:34:10' WHERE id = 111;
db.Model(&user).Updates(User{Name: "hello", Age: 18, Active: false})
// 根据 `map` 更新属性
// UPDATE users SET name='hello', age=18, active=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
db.Model(&user).Updates(map[string]interface{}{"name": "hello", "age": 18, "active": false})
```
### 修改指定字段
方法: Select、Omit
```go
// User's ID is `111`:
// struct:UPDATE users SET name='hello' WHERE id=111;
db.Model(&user).Select("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "active": false})
// 忽略某个字段
// UPDATE users SET age=18, active=false, updated_at='2013-11-17 21:34:10' WHERE id=111;
db.Model(&user).Omit("name").Updates(map[string]interface{}{"name": "hello", "age": 18, "active": false})
//选择role以外的所有字段
db.Model(&user).Select("*").Omit("Role").Updates(User{Name: "jinzhu", Role: "admin", Age: 0})
```
###  更新hook
暂时忽略
### 批量更新
未通过 Model 指定记录的主键，则 GORM 会执行批量更新
更新如果没有任何条件则会报错,可以通过添加条件或原生Sql或者启用`AllowGlobalUpdate`模式
```go
// 根据 struct 更新
// UPDATE users SET name='hello', age=18 WHERE role = 'admin';
db.Model(User{}).Where("role = ?", "admin").Updates(User{Name: "hello", Age: 18})
// 根据 map 更新
db.Table("users").Where("id IN ?", []int{10, 11}).Updates(map[string]interface{}{"name": "hello", "age": 18})
// UPDATE users SET name='hello', age=18 WHERE id IN (10, 11);
// gorm.ErrMissingWhereClause
db.Model(&User{}).Updates("name", "jinzhu").Error 
```
通过原生sql,启用`AllowGlobalUpdate`模式解决gorm.ErrMissingWhereClause报错
```go
db.Exec("UPDATE users SET name = ?", "jinzhu")
// UPDATE users SET name = "jinzhu"
db.Session(&gorm.Session{AllowGlobalUpdate: true}).Model(&User{}).Update("name", "jinzhu")
// UPDATE users SET `name` = "jinzhu"
```
### 获取受更新影响的行数
`RowsAffected`属性
```go
// UPDATE users SET name='hello', age=18 WHERE role = 'admin';
result := db.Model(User{}).Where("role = ?", "admin").Updates(User{Name: "hello", Age: 18})
result.RowsAffected // 更新的记录数
result.Error        // 更新的错误
```
### 高级选项
暂时忽略

## 删除

### 删除单条记录
需要指定主键,否则会触发批量删除
```go
// Email 的 ID 是 `10`
// DELETE from emails where id = 10;
db.Delete(&email)
// 带额外条件的删除
// DELETE from emails where id = 10 AND name = "jinzhu"
db.Where("name = ?", "jinzhu").Delete(&email)
```
### 根据主键删除
```go
// DELETE FROM users WHERE id = 10;
db.Delete(&User{}, 10)
db.Delete(&User{}, "10")
// DELETE FROM users WHERE id IN (1,2,3);
db.Delete(&users, []int{1,2,3})
```
### Delete hook
暂时忽略
### 批量删除
如果指定的值不包括主属性，那么 GORM 会执行批量删除，将删除所有匹配的记录
```go
// DELETE from emails where email LIKE "%jinzhu%";
db.Where("email LIKE ?", "%jinzhu%").Delete(&Email{})
// DELETE from emails where email LIKE "%jinzhu%";
db.Delete(&Email{}, "email LIKE ?", "%jinzhu%")
```
### 返回被删除的数据
```go
// 返回所有列
var users []User
// 返回所有列
var users []User
// DELETE FROM `users` WHERE role = "admin" RETURNING *
DB.Clauses(clause.Returning{}).Where("role = ?", "admin").Delete(&users)
// users => []User{{ID: 1, Name: "jinzhu", Role: "admin", Salary: 100}, {ID: 2, Name: "jinzhu.2", Role: "admin", Salary: 1000}}
// 返回指定的列
// DELETE FROM `users` WHERE role = "admin" RETURNING `name`, `salary`
// users => []User{{ID: 0, Name: "jinzhu", Role: "", Salary: 100}, {ID: 0, Name: "jinzhu.2", Role: "", Salary: 1000}}
DB.Clauses(clause.Returning{Columns: []clause.Column{{Name: "name"}, {Name: "salary"}}}).Where("role = ?", "admin").Delete(&users)

```

### 软删除
概念:
1. 不会把记录从数据库中真正删除,只是把DeletedAt设置为当前时间
2. 删除后不能再通过普通的查询方法找到该记录
```go
// user 的 ID 是 `111`
// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE id = 111;
db.Delete(&user)
// 批量删除
// UPDATE users SET deleted_at="2013-10-29 10:23" WHERE age = 20;
db.Where("age = ?", 20).Delete(&User{})
// 查询时会忽略被软删除的记录
db.Where("age = 20").Find(&user)
// SELECT * FROM users WHERE age = 20 AND deleted_at IS NULL
```
### 永久删除
找到被软删除的记录:`db.Unscoped().Where("age = 20").Find(&users)`
```go
// DELETE FROM orders WHERE id=10;
db.Unscoped().Delete(&order)
```
---
## 关联
### belongs to
概念:
1. 包含 user 和 company，并且每个 user 能且只能被分配给一个 company
2. User和Company有一个共同的外键CompanyID
```go
type User struct {
  gorm.Model
  Name      string
  CompanyID int
  Company   Company `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"`
}
type Company struct {
  ID   int
  Name string
}
```


### has one 
概念:
1. 包含 user 和 credit card ，且每个 user 只能有一张 credit card
```go
// User 有一张 CreditCard，UserID 是外键
type User struct {
  gorm.Model
  CreditCard CreditCard
}
type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}
// 检索用户列表并预加载信用卡
func GetAll(db *gorm.DB) ([]User, error) {
    var users []User
    err := db.Model(&User{}).Preload("CreditCard").Find(&users).Error
    return users, err
}
```
### Has Many
概念:
1. 包含 user 和 credit card 模型，且每个 user 可以有多张 credit card
```go
// User 有多张 CreditCard，UserID 是外键
type User struct {
  gorm.Model
  CreditCards []CreditCard
}
type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}
// 检索用户列表并预加载信用卡
func GetAll(db *gorm.DB) ([]User, error) {
    var users []User
    err := db.Model(&User{}).Preload("CreditCards").Find(&users).Error
    return users, err
}
```
### Many to Many
概念:
1. 包含了 user 和 language，且一个 user 可以说多种 language，多个 user 也可以说一种 language
2. 当使用 GORM 的 AutoMigrate 为 User 创建表时，GORM 会自动创建连接表
```go
// User 拥有并属于多种 language，`user_languages` 是连接表
type User struct {
  gorm.Model
  Languages []Language `gorm:"many2many:user_languages;"`
}
type Language struct {
  gorm.Model
  Name string
}
// User 拥有并属于多种 language，`user_languages` 是连接表
type User struct {
  gorm.Model
  Languages []*Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
  Users []*User `gorm:"many2many:user_languages;"`
}
// 检索 User 列表并预加载 Language
func GetAllUsers(db *gorm.DB) ([]User, error) {
    var users []User
    err := db.Model(&User{}).Preload("Languages").Find(&users).Error
    return users, err
}
// 检索 Language 列表并预加载 User
func GetAllLanguages(db *gorm.DB) ([]Language, error) {
    var languages []Language
    err := db.Model(&Language{}).Preload("Users").Find(&languages).Error
    return languages, err
}
```
### 实体关联
在创建、更新记录时，GORM 会通过 Upsert 自动保存关联及其引用记录。
跳过自动创建更新:使用select 和 omit

### 预加载
#### 使用 `Preload`通过多个SQL中来直接加载关系
```go
type User struct {
  gorm.Model
  Username string
  Orders   []Order
}
type Order struct {
  gorm.Model
  UserID uint
  Price  float64
}
// 查找 user 时预加载相关 Order
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4);
db.Preload("Orders").Find(&users)
// SELECT * FROM users;
// SELECT * FROM orders WHERE user_id IN (1,2,3,4); // has many
// SELECT * FROM profiles WHERE user_id IN (1,2,3,4); // has one
// SELECT * FROM roles WHERE id IN (4,5,6); // belongs to
db.Preload("Orders").Preload("Profile").Preload("Role").Find(&users)

```
#### joins预加载
```go
db.Joins("Company").Joins("Manager").Joins("Account").First(&user, 1)
db.Joins("Company").Joins("Manager").Joins("Account").First(&user, "users.name = ?", "jinzhu")
db.Joins("Company").Joins("Manager").Joins("Account").Find(&users, "users.id IN ?", []int{1,2,3,4,5})
db.Joins("Company", DB.Where(&Company{Alive: true})).Find(&users)
```
---
## 处理错误
普通错误:
```go
if err := db.Where("name = ?", "jinzhu").First(&user).Error; err != nil {
  // 处理错误...
}
```
未找到对应记录错误ErrRecordNotFound
```go
// 检查错误是否为 RecordNotFound
err := db.First(&user, 100).Error
errors.Is(err, gorm.ErrRecordNotFound)
```
## 链式方法
链式/终结方法之后返回一个初始化的`*gorm.DB`实例
- 链式方法:Where, Select, Omit, Joins, Scopes, Preload, Raw
- 终结方法:Create, First, Find, Take, Save, Update, Delete, Scan, Row, Rows
- 新建会话方法: Session、WithContext、Debug 
## session
## 钩子
## 事务
暂时忽略
## 迁移
用于自动迁移 schema，保持您的 schema 是最新的
schema:数据库对象集合，它包含了各种对像，比如：表，视图，存储过程，索引等等
```go
db.AutoMigrate(&User{})
db.AutoMigrate(&User{}, &Product{}, &Order{})
// 创建表时添加后缀
db.Set("gorm:table_options", "ENGINE=InnoDB").AutoMigrate(&User{})

```
## 日志Logger
作用:打印慢 SQL 和错误
级别:Silent、Error、Warn、Info
```go
newLogger := logger.New(
  log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer（日志输出的目标，前缀和日志包含的内容）
  logger.Config{
    SlowThreshold: time.Second,   // 慢 SQL 阈值
    LogLevel:      logger.Silent, // 日志级别
    IgnoreRecordNotFoundError: true,   // 忽略ErrRecordNotFound（记录未找到）错误
    Colorful:      false,         // 禁用彩色打印
  },
)
// 全局模式
db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{
  Logger: newLogger,
})

// 新建会话模式
tx := db.Session(&Session{Logger: newLogger})
tx.First(&user)
tx.Model(&user).Update("Age", 18)
```

## 通用数据库接口
```go
// 获取通用数据库对象 sql.DB，然后使用其提供的功能
sqlDB, err := db.DB()
// Ping
sqlDB.Ping()
// Close
sqlDB.Close()
// 返回数据库统计信息
sqlDB.Stats()
```
### 连接池
```go
// 获取通用数据库对象 sql.DB ，然后使用其提供的功能
sqlDB, err := db.DB()
// SetMaxIdleConns 用于设置连接池中空闲连接的最大数量。
sqlDB.SetMaxIdleConns(10)
// SetMaxOpenConns 设置打开数据库连接的最大数量。
sqlDB.SetMaxOpenConns(100)
// SetConnMaxLifetime 设置了连接可复用的最大时间。
sqlDB.SetConnMaxLifetime(time.Hour)
```