---
title: backTopAndBottom
date: 2022-09-23 10:44:09
tags: ['工作','常用功能']
categories: 缺陷修复
---

## 缺陷链接
http://10.186.18.11/jira/browse/DMP-13892

## 需求
巡检报告页面、库表检查页面增加置顶、置底功能

## 思路
1. 两个页面都需要增加这个功能,那就做成一个组件,避免写重复代码
2. umc-ui项目中已经有这部分功能的实现,所以只需要整合一下相关的代码封装成组件
3. 置顶功能在antd中已经实现,所以需要我们自己实现的只有置底功能
4. 通过scrollInView方法实现

## 相关代码
```React
import {
  VerticalAlignBottomOutlined,
  VerticalAlignTopOutlined,
} from '@ant-design/icons';
import { BackTop, Button } from 'antd';
import { useEffect, useState } from 'react';

const BackTopAndBottom: React.FC<{ contentRef: HTMLDivElement | null }> = ({
  contentRef,
}) => {
  const [toBottomButtonVisible, setToBottomButtonVisible] = useState(true);
  const moveToBottom = () => {
    if (contentRef) {
      contentRef.scrollIntoView({
        block: 'end',
        behavior: 'smooth',
      });
    }
  };
  useEffect(() => {
    const dom = document.querySelector(
      '#root main.ant-layout-content.action-content'
    );
    const handleScrollChange = () => {
      const interval =
        (dom?.scrollHeight ?? 0) -
        (dom?.scrollTop ?? 0) -
        (dom?.clientHeight ?? 0);
      setToBottomButtonVisible(interval > 80);
    };
    dom?.addEventListener('scroll', handleScrollChange);
    return () => {
      dom?.removeEventListener('scroll', handleScrollChange);
    };
  }, []);
  return (
    <>
      {toBottomButtonVisible && (
        <Button
          shape="circle"
          icon={<VerticalAlignBottomOutlined />}
          onClick={moveToBottom}
          type="primary"
        />
      )}
      <BackTop
        visibilityHeight={250}
        className="back-top"
        target={() => document.querySelector('.action-content') as HTMLElement}
      >
        <Button
          shape="circle"
          type="primary"
          icon={<VerticalAlignTopOutlined />}
        ></Button>
      </BackTop>
    </>
  );
};
export default BackTopAndBottom;

```


## 遇到的问题
这个组件添加以后,在库表检查页面没有问题,但是在巡检报告页面,出现了下面的bug:
```TypeScript
  contentRef.scrollIntoView({
    block: 'end',
    behavior: 'smooth',
  });
  ```
当behavior设置为smooth的时候点击置底按钮,预期是拉到页面底部,但是实际情况是停在了页面的第一张canvas图部分,并没有一直拉到页面底部;但是设置为auto以后,即取消动画,点击可以拉到页面底部。

## 问题解决
比较两个页面调用组件的父组件的代码，发现巡检报告页面监听了页面的滚动事件，而库表检查页面没有,于是注释了对应的代码，发现问题被解决了。

```TypeScript
  let setScroll = true;
  useLayoutEffect(() => {
    const content = document.querySelector<HTMLElement>('.action-content');

    if (setScroll && content) {
      setScroll = false;
      // 此处是问题产生的原因，增加防抖可解决问题
      content.addEventListener('scroll',scrollChange);
      // 修改后
       content.addEventListener('scroll',lodash.debounce(scrollChange,100));
    }

    return () => {
      if (content) {
        content.removeEventListener('scroll', scrollChange);
      }
    };
  });

  const scrollChange = () => {
    const ball = document.querySelector<HTMLSpanElement>(
      '.ant-anchor-ink-ball'
    );

    if (ball) {
      const top = Number.parseInt(ball.style.top || '');
      const wrapper = document.querySelector<HTMLDivElement>(
        '.ant-anchor-wrapper'
      );
      const height = wrapper ? wrapper.clientHeight : 0;
      if (wrapper) {
        if (top > height) {
          wrapper.scrollTop = top - height + 100;
        } else if (top < wrapper.scrollTop) {
          wrapper.scrollTop = top - 100;
        }
      }
    }
  };
```

## 猜想
子组件和父组件都监听了action-content容器的滚动事件，并且有不同的回调函数，同时执行会导致冲突，最终滚动的高度没有达到预期。使用debounce防抖，延迟执行，可以消除这一问题

## 知识点
- debounce 防抖
>  - _.debounce(func, [wait=0], [options=])
>  - 在一段连续操作结束后，处理回调
>  - 创建一个 debounced（防抖动）函数，该函数会从上一次被调用后，延迟 wait 毫秒后调用 func 方法
>  - 如果 wait 为 0 并且 leading 为 false, func调用将被推迟到下一个点，类似setTimeout为0的超时
- throttle 节流
>  - _.throttle(func, [wait=0], [options=])
>  - 创建一个节流函数，在 wait 秒内最多执行 func 一次的函数
>  - 在一段连续操作中，每一段时间只执行一次
- 原生JS实现
```TypeScript
//防抖 debounce
function debounce(fn, delay) {
    var timer; // 维护一个 timer
    return function () {
        var _this = this; // 取debounce执行作用域的this
        var args = arguments;
        if (timer) {
            clearTimeout(timer);
        }
        timer = setTimeout(function () {
            fn.apply(_this, args); // 用apply指向调用debounce的对象，相当于_this.fn(args);
        }, delay);
    };
}
//节流 throttle
function throttle(fn, delay) {
    var timer;
    return function () {
        var _this = this;
        var args = arguments;
        if (timer) {
            return;
        }
        timer = setTimeout(function () {
            fn.apply(_this, args);
            timer = null; // 在delay后执行完fn之后清空timer，此时timer为假，throttle触发可以进入计时器
        }, delay)
    }
}
```


## 参考文章链接
1. https://juejin.cn/post/6844903669389885453
2. https://segmentfault.com/a/1190000018445196