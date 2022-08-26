---
title: DBLE读写分离操作文档
urlname: wuofdb
date: '2022-02-09 13:24:26 +0800'
tags: []
categories: []
---

# 一、背景

新版的 DBLE 目前已支持读写分离功能，DMP（4.21.0.9 版本以上）平台支持通过界面创建使用 MySQL 5.7.x / 8.0.x 的读写分离功能，但暂不支持 MySQL 5.6.x 版本。根据资料显示，可以通过修改 DBLE 的配置文件，实现 MySQL 5.6.x 版本的读写分离。

# 二、DBLE 安装

## 2.1 安装 java 环境

DBLE 是 java 语言开发的，因此需要在 DBLE 节点上安装 java，java 版本为 1.8 或者以上。
1、查找 java 相关的列表
yum -y list java\*
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384330362-e09e7975-d6a1-42de-8875-612342cab48b.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=171&id=u394cc823&margin=%5Bobject%20Object%5D&name=image.png&originHeight=300&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=158014&status=done&style=none&taskId=uc84ef15e-e805-4dcd-979f-278ee8f2dff&title=&width=494.2857142857143)
2、安装 jdk
yum -y install java-1.8.0-openjdk.x86_64
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384339515-2045bb44-2efc-4d82-b412-170980bcaf7d.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=172&id=u88783863&margin=%5Bobject%20Object%5D&name=image.png&originHeight=301&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=311457&status=done&style=none&taskId=u5c258282-a912-4aac-8a1d-07e983b8273&title=&width=494.2857142857143)
3、完成安装后验证
java -version
4、修改环境变量
vi /etc/profile
在文件最后加入：

```bash
#set java environment
JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME CLASSPATH PATH
```

![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384359069-78e6b18e-d26f-40e4-9db1-d397d448b307.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=95&id=ud0a88765&margin=%5Bobject%20Object%5D&name=image.png&originHeight=167&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=95789&status=done&style=none&taskId=u8ac89ec9-96b4-4c76-9a27-0bee4cda76e&title=&width=494.2857142857143)
注：通过 yum 安装的默认路径为：/usr/lib/jvm
5、配置生效
. /etc/profile
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384368980-d7a39d89-59cc-4031-8242-dda2f8df22af.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=27&id=u01114dbd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=47&originWidth=738&originalType=binary∶=1&rotation=0&showTitle=false&size=34126&status=done&style=none&taskId=u12959dda-ecf5-4cc8-84e1-e6652fab461&title=&width=421.7142857142857)

## 2.2 安装 DBLE

1、DBLE 下载
地址：[https://github.com/actiontech/dble/releases](https://github.com/actiontech/dble/releases)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384380030-5b735238-8f24-464c-ae1d-bfa48aae6729.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=171&id=uc04350dc&margin=%5Bobject%20Object%5D&name=image.png&originHeight=300&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=36410&status=done&style=none&taskId=u7832652e-fe19-4ea6-9b73-2de5128f0b5&title=&width=494.2857142857143)
2、安装部署

```bash
#创建DBLE的工作目录
mkdir -p /data/dble/
#解压DBLE的安装包
tar xf dble-3.21.10.0-20211119065525-java1.8.0_151-linux.tar.gz
#修改DBLE配置文件名称
cd /data/dble/dble/conf
mv cluster_template.cnf cluster.cnf
mv bootstrap_template.cnf bootstrap.cnf
mv db_template.xml db.xml
mv user_template.xml user.xml
mv sharding_template.xml sharding.xml
```

![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384399272-8531bf3b-9cb7-4847-bb35-17d3455243b8.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=121&id=u308bef28&margin=%5Bobject%20Object%5D&name=image.png&originHeight=211&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=109818&status=done&style=none&taskId=u4cdc0593-8b2f-43a4-96ef-ce75aeea3b3&title=&width=494.2857142857143)
3、修改 DBLE 配置文件
（1）user.xml
vi user.xml
<rwSplitUser name="test" password="123456" dbGroup="dbGroup1" blacklist="blacklist1" maxCon="20"/>
注：rwSplitUser 为读写用户配置，同时需要把 shardingUser 的标签内容给注释掉。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384428590-162e6ed0-3fe5-4c3c-830a-2192e48fd599.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=270&id=ub5e708aa&margin=%5Bobject%20Object%5D&name=image.png&originHeight=473&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=304953&status=done&style=none&taskId=u42221cc1-3639-4fe8-b251-88b05919871&title=&width=494.2857142857143)
（2）db.xml
修改对应的 ip/端口/账号密码
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384434565-d1838cc7-74db-4140-822f-17fe3347ccaa.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=139&id=u34bc71c3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=243&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=108033&status=done&style=none&taskId=ud9353676-f9aa-497a-87aa-712ae98b6a8&title=&width=494.2857142857143)

## 2.3 启动并连接

1、启动
cd /data/dble/dble
bin/dble start
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384452472-e5157f29-1fd3-4912-b5a2-e5091b1f0804.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=254&id=u46419886&margin=%5Bobject%20Object%5D&name=image.png&originHeight=445&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=327608&status=done&style=none&taskId=u1943ddf4-3619-42ac-87dc-78c12321e81&title=&width=494.2857142857143)
2、连接
DBLE 客户端连接（使用读写分离用户）
mysql -p -P8066 -h 127.0.0.1 -u test
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384460100-53057cd0-cbcb-4f7e-9a90-eefc31798e1a.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=177&id=ua406914a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=310&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=110145&status=done&style=none&taskId=uff404877-ad6b-41f9-8ce3-2651e337110&title=&width=494.2857142857143)

## 2.4 测试验证

1、修改 my.cnf 文件，开启 MySQL 的 general.log，用于验证 SQL 语句的下发
general_log_file = /opt/mysql/data/3306/general.log
general_log = ON
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384470112-a3abfcff-bf32-44a1-8dbc-93a1e7381265.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=181&id=ua4812b22&margin=%5Bobject%20Object%5D&name=image.png&originHeight=316&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=156123&status=done&style=none&taskId=ubcf68042-59b7-42a9-97c1-dc0d2226827&title=&width=494.2857142857143)
2、在库中创建表并插入数据，查询
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384483762-aa16d92e-b3cd-4fc9-b4dd-b1f0bb2ca8f6.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=254&id=udcb157ed&margin=%5Bobject%20Object%5D&name=image.png&originHeight=444&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=171099&status=done&style=none&taskId=u4c10fdce-ea5b-4e61-ae2a-1ff7e3c988b&title=&width=494.2857142857143)
3、查看主从实例的 general.log
主实例![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384491121-0a999d75-5cec-4e92-925f-87cde68d7b78.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=65&id=u87f31a57&margin=%5Bobject%20Object%5D&name=image.png&originHeight=113&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=77552&status=done&style=none&taskId=u957ed13b-ed5a-4713-a69f-0d705215c2b&title=&width=494.2857142857143)
从实例![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1644384496657-68622c2d-cd51-4ca7-8b76-94c8c4d11865.png#clientId=u714ff03f-4505-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=37&id=u4e87a9cf&margin=%5Bobject%20Object%5D&name=image.png&originHeight=64&originWidth=865&originalType=binary∶=1&rotation=0&showTitle=false&size=38345&status=done&style=none&taskId=u27a90ee9-d0e4-4ed5-a860-5c8d58eb5c3&title=&width=494.2857142857143)
