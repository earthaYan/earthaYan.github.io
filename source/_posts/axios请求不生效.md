---
title: umc-ui表格筛选不生效
date: 2023-07-31 10:34:09
tags: [http请求]
categories: 工作
---

## 背景：

偶然发现项目中一个表格筛选没有生效,传参字段值为` filter_redis_sentinel_instance_ids: tableFilterInfo.redis_sentinel_instance_id ?? undefined`
{%asset_img fail.jpg 表格筛选不生效%}
上报缺陷以后，自己用 postman 试了一下，发现接口`v4/redis/sentinel_instance/list?page_index=1&page_size=20&filter_redis_sentinel_instance_ids[]=redis-sentinel-u97bvd`,当`filter_redis_sentinel_instance_ids`字段传入单个值的时候，是可以有效筛选出对应的节点 ID 数据的。

## 解决方案：

寻求后端帮助，后端发现如果将`filter_redis_sentinel_instance_ids`参数值用逗号分隔开，而不是直接传数组，此时筛选是有效的。但是实践后发现由于后端将其定义为字符串数组类型，所以前端将它使用`join()`方法转换为字符串后，TS 语法检查过不去。此时解决方案是后端重新定义接口字段类型，将其从`string[]`转换为`string`,将参数修改为`filter_redis_sentinel_instance_ids:tableFilterInfo.redis_sentinel_instance_id?.[0]`。此时可以修复问题。

## 类似问题

发现项目中有很多类似的问题，比如 uProxy 页面实例列表有一个实例 id 筛选:

```javascript
  React.useEffect(() => {
    if (!!selectData) {
      const groupId = selectData?.uproxy_group_id ?? '';
      UproxyService.listUproxyInstancesV6({
        // 该参数类型定义为Array<string>，但传递数组是无效的，只能传递字符串。
        filter_uproxy_group_ids: groupId as any,
      }).then((res) => {
        if (res.data && res.data.length === 1) {
          setIsLast(true);
        } else {
          setIsLast(false);
        }
      });
    }
  }, [selectData]);
```

这里根据后端 swagger 文档生成的 api 接口定义里,`filter_uproxy_group_ids`字段是一个字符串数组，但是此时前端传递数组是无效的，只能传递字符串，但是 TS 检查过不去，所以这里使用了`as any`，这也是大部分同类问题没有出现问题的原因，比如：

```javascript
const params: IListUproxyInstancesV6Params = {
  filter_uproxy_group_ids: info.uproxy_group_id?.[0],
};
```

由于`info`是`FilteredInfo`类型,所以此时传给`filter_uproxy_group_ids`的实际上是`any`类型,躲过了 TS 检查。但如果后续需求有多值筛选的时候，就无法躲过 TS 检查：

```javascript
export type FilteredInfo = {
  [key: string]: any[] | null,
};
```

## 后续

有后端同事反馈，这种重新定义接口的解决方案修复成本较高，因为每次修改接口定义都需要新增一个 v1->v2 这种类似的接口，但是内部逻辑是不变的。所以需要从前端角度再找一找其他的解决方案，降低以后修改项目里其他类似缺陷的修复成本。询问其他前端同事得到以下信息：

> 问题本质原因是 axios 对 query 类型的参数的 format 格式与后端使用的 parse params 方式不匹配。axios 默认会将 query 中的 array 格式化城?a[]=1&a[]=2 的格式，但是后端使用的 parse 只支持 ?a=1,2 的格式。

查阅了[axios 的官方文档](https://axios-http.com/zh/docs/req_config) ,发现了配置项：

```javascript
import qs from 'query-string'
paramsSerializer: function (params) {
  return qs.stringify(params, {arrayFormat: 'brackets'})
}
```

`arrayFormat`的默认值是`brackets`,所以出现了 url 中 a[]=1 这种现象，导致筛选失败，将其修改为`comma`即可。

```javascript
qs.stringify({ a: ['b', 'c'] }, { arrayFormat: 'indices' });
// 'a[0]=b&a[1]=c'
qs.stringify({ a: ['b', 'c'] }, { arrayFormat: 'brackets' });
// 'a[]=b&a[]=c'
qs.stringify({ a: ['b', 'c'] }, { arrayFormat: 'repeat' });
// 'a=b&a=c'
qs.stringify({ a: ['b', 'c'] }, { arrayFormat: 'comma' });
// 'a=b,c'
```

所以最终修改方式是修改 request 属性值

```javascript
return handleTableRequestError(
  RedisService.ListRedisSentinelInstancesV5(cleanEmptyParams(params))
);
// ----变更为--------
return handleTableRequestError(
  RedisService.ListRedisSentinelInstancesV5(cleanEmptyParams(params), {
    paramsSerializer(paramsAll) {
      return qs.stringify(paramsAll, {
        arrayFormat: 'comma',
      });
    },
  })
);
```
