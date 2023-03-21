---
title: gorm学习笔记
date: 2023-03-21 12:58:53
tags: [golang, gorm]
categories: GoLang
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
- 检查ErrRecordNotFound 错误
`errors.Is(result.Error, gorm.ErrRecordNotFound)`
- 避开ErrRecordNotFound 错误
`db.Limit(1).Find(&user)`
- Fist和Last方法生效条件
  1. 指向目标struct的指针作为参数传入方法
  2. 使用`db.Model()`指定model
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
2. 主键是字符串:有sql注入风险
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
#### string条件
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
如果设置了对象的主键,则与查询条件构成AND关系

#### struct&Map条件
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
内联指的是将查询条件嵌入到First等方法中,达到与where相似的效果
```go
db.First(&user, "id = ?", "string_primary_key")
db.Find(&user, "name = ?", "jinzhu")
db.Find(&users, "name <> ? AND age > ?", "jinzhu", 20)
// struct
db.Find(&users, User{Age: 20})
// map
db.Find(&users, map[string]interface{}{"age": 20})
```
#### Not条件 和 Or条件
```go
// Not
// 查询namewe
db.Not("name = ?", "jinzhu").First(&user)
db.Not(map[string]interface{}{"name": []string{"jinzhu", "jinzhu 2"}}).Find(&users)
db.Not(User{Name: "jinzhu", Age: 18}).First(&user)
db.Not([]int64{1,2,3}).First(&user)
// Or
db.Where("role = ?", "admin").Or("role = ?", "super_admin").Find(&users)
db.Where("name = 'jinzhu'").Or(User{Name: "jinzhu 2", Age: 18}).Find(&users)
db.Where("name = 'jinzhu'").Or(map[string]interface{}{"name": "jinzhu 2", "age": 18}).Find(&users)

```
## 修改

## 删除
