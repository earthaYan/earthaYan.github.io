---
title: React_Router中的Prompt
date: 2023-05-23 14:17:29
tags: [React]
categories: 前端
---

web 中的`Prompt`组件是从核心的`Prompt`中二次导出的。

## 概览

- 作用：在从一个页面导航离开之前给用户提示。
- 场景：应用处在一个应该阻止用户离开当前页面的状态
- 实际场景：表单填了一半，用户想要离开
- 使用：

```jsx
<Prompt when={formIsHalfFilledOut} message="Are you sure you want to leave?" />
```

## 参数详解

### when

#### boolean

可以直接传写死的布尔值，而不是有条件地在守卫后面渲染`Prompt`

1. true:阻止导航
2. false：允许导航

### message

#### string

当用户试图离开当前页时，会给用户这个字符串信息
{%asset_img prompt.jpeg %}
#### function
```jsx
export function Users() {
  return (
    <React.Fragment>
      <Prompt
        message={(nextLocation, action) => {
          if (action === 'POP') {
            console.log('Backing up...');
          }

          return nextLocation.pathname.startsWith('/app')
            ? false
            : `Are you sure you want to go to ${location.pathname}?`;
        }}
      />
      <h2>Users</h2>
    </React.Fragment>
  );
}
```
会在进入用户试图导航进入的下一个 `location`和 `action`之前被调用。
返回值：

1. string：向用户展示一个提示,用户点击确定后跳转，点击取消停留在原地
2. true：允许这个过度，直接跳转到nextLocation
3. false:不允许过度，且点击link无反应
