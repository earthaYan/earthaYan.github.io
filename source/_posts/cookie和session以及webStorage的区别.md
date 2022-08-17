---
title: cookie和session以及webStorage的区别
date: 2022-08-17 09:43:38
tags: [session,webStorage,cookie]
categories: 浏览器
---
# cookie VS webStorage
1. 都会在浏览器端保存，有大小限制，同源限制
2. cookie 会在请求时发送到服务器，作为会话标识，服务器可修改 cookie；web storage 不会发送到服务器
3. cookie 有 path 概念，子路径可以访问父路径 cookie，父路径不能访问子路径 cookie
4. 有效期：cookie 在设置的有效期内有效，默认为浏览器关闭；sessionStorage 在窗口关闭前有效；localStorage 长期有效，直到用户删除
5. 作用域不同 sessionStorage：不在不同的浏览器窗口中共享，即使是同一个页面；localStorage：在所有同源窗口都是共享的；cookie：也是在所有同源窗口中共享的
6. 存储大小不同：cookie 数据不能超过 4K；webStorage 虽然也有存储大小的限制，但是比 cookie 大得多，可以达到 5M 或更大
---
# cookie VS session
1. 存储位置不同：
- cookie 数据存放在客户的浏览器上
- session 数据放在服务器上。
2. 存储容量不同：
- 单个 cookie 保存的数据不能超过 4K，一个站点最多保存 20 个 cookie。
- 对于 session 来说并没有上限，但出于对服务器端的性能考虑，session 内不要存放过多的东西，并且设置 session 删除机制。

3. 存储方式不同：

- cookie 中只能保管 ASCII 字符串，并需要通过编码方式存储为 Unicode 字符或者二进制数据。

- session 中能够存储任何类型的数据，包括且不限于 string，integer，list，map 等。

4. 隐私策略不同

- cookie 对客户端是可见的，别有用心的人可以分析存放在本地的 cookie 并进行 cookie 欺骗，所以它是不安全的。

- session 存储在服务器上，不存在敏感信息泄漏的风险。

5. 有效期不同

- cookie 保管在客户端，不占用服务器资源。对于并发用户十分多的网站，cookie 是很好的选择。

- session 是保管在服务器端的，每个用户都会产生一个 session。假如并发访问的用户十分多，会产生十分多的 session，耗费大量的内存