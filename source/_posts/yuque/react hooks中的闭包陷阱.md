---
title: react hooks中的闭包陷阱
urlname: gknl3f
date: '2022-07-14 10:20:48 +0800'
tags: []
categories: []
---

原文：[Understanding the Closure Trap of React Hooks
](https://betterprogramming.pub/understanding-the-closure-trap-of-react-hooks-6c560c408cde)
在开发的过程中，我们经常使用 hooks。但是也经常会遇到一些问题，比如：

```javascript
import { useEffect, useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setInterval(() => {
      setCount(count + 1);
    }, 1500);
  }, []);

  useEffect(() => {
    setInterval(() => {
      console.log(count);
    }, 1500);
  }, []);

  return <div>Hello world</div>;
}
```

在这段代码中，使用 useState 创建了一个 count 的 state 值，并且在第一个 useEffect 中定时增加 count 的值，同时在另外一个 useEffect 打印 count 的值。预期的结果是 0，1，...，但是实际执行以后发现跟预期是不太符合的
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1657765946009-617cb759-84c8-4a4e-b58e-0d252e8d6fc2.png#clientId=ucde22273-7b3b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=595&id=ucaca7b44&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1189&originWidth=2552&originalType=binary∶=1&rotation=0&showTitle=false&size=264060&status=done&style=none&taskId=u426fe684-5088-4eb6-a5d4-92dcbc9d9ed&title=&width=1276)
这就是 React hooks 带来的闭包陷阱

---

React 运行时的组件：

- 每个组件对应一个 fiber node
- 每个 fiber node 都有一个 memorizedState 属性，memorizedState 是一个链表
- 组件的每个 hook 都对应 memorizedState 链表中的一个节点，他们从对应的节点访问自己的值

![1_T1TiRZM4ilPXV4B2m2GWwA.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1657767533868-13feb8eb-f1a4-490b-b73c-55a4ea29734e.png#clientId=u06c2f962-ebf5-4&crop=0&crop=0&crop=1&crop=1&from=drop&height=405&id=u6b6e2ad1&margin=%5Bobject%20Object%5D&name=1_T1TiRZM4ilPXV4B2m2GWwA.png&originHeight=1590&originWidth=1225&originalType=binary∶=1&rotation=0&showTitle=false&size=241986&status=done&style=none&taskId=u98f8a216-d516-4fac-afe1-c84da9bd0b4&title=&width=312)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1657767921376-c1ca8d74-6008-400b-9af3-b728bbdf535c.png#clientId=u06c2f962-ebf5-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=381&id=ub84d6099&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1005&originWidth=913&originalType=binary∶=1&rotation=0&showTitle=false&size=409788&status=done&style=none&taskId=u7c66f2ad-c48d-439b-84c0-5f3e7064bc6&title=&width=346.5)
比如，在上面的代码中使用了 3 个 hook，和 memorizedState 链表中的节点是一 一对应的，hook 通过各自的 memorizedState 完成自己的逻辑

---

hooks 的实现：
一个 hook 有两个阶段：加载和更新
当 hook 第一次被创建的时候，会执行 mount 函数；hook 更新，update 函数也随之被执行

```typescript
function mountEffect(
  create: () => (() => void) | void,
  deps: Array<mixed> | void | null
): void {
  //....
  return mountEffectImpl(
    PassiveEffect | PassiveStaticEffect,
    HookPassive,
    create,
    deps
  );
}
function mountEffectImpl(fiberFlags, hookFlags, create, deps): void {
  const hook = mountWorkInProgressHook();
  //如果没有传第二个参数deps，则deps被设置为null。
  const nextDeps = deps === undefined ? null : deps;
  currentlyRenderingFiber.flags |= fiberFlags;
  //需要被执行的回调函数会被标记上 HookHasEffect
  hook.memoizedState = pushEffect(
    HookHasEffect | hookFlags,
    create,
    undefined,
    nextDeps
  );
}

function updateEffect(
  create: () => (() => void) | void,
  deps: Array<mixed> | void | null
): void {
  return updateEffectImpl(PassiveEffect, HookPassive, create, deps);
}

function updateEffectImpl(fiberFlags, hookFlags, create, deps): void {
  const hook = updateWorkInProgressHook();
  //如果没有传第二个参数deps，则deps被设置为null。
  const nextDeps = deps === undefined ? null : deps;
  let destroy = undefined;

  if (currentHook !== null) {
    const prevEffect = currentHook.memoizedState;
    destroy = prevEffect.destroy;
    if (nextDeps !== null) {
      const prevDeps = prevEffect.deps;
      //比较新传入的deps和 memorizedState 已经存在的deps，如果两个值相等，之前的函数会直接被使用，否则会创建一个新的函数。
      if (areHookInputsEqual(nextDeps, prevDeps)) {
        hook.memoizedState = pushEffect(hookFlags, create, destroy, nextDeps);
        return;
      }
    }
  }
  //需要被执行的回调函数会被标记上 HookHasEffect
  hook.memoizedState = pushEffect(
    HookHasEffect | hookFlags,
    create,
    destroy,
    nextDeps
  );
}
```

比较两个 deps 是否一致的方法：

```typescript
function areHookInputsEqual(
  nextDeps: Array<mixed>,
  prevDeps: Array<mixed> | null
) {
  //如果之前的deps是null,就直接返回false-不相等
  if (prevDeps === null) {
    return false;
  }
  //依次遍历和比较数组
  for (let i = 0; i < prevDeps.length && i < nextDeps.length; i++) {
    if (is(nextDeps[i], prevDeps[i])) {
      continue;
    }
    return false;
  }
  return true;
}
```

从这些可以得出：

1. 如果 useEffect 的 deps 参数是 undefined 或者 null,回调函数将会被重新创建并且在每次重新渲染的时候执行
1. 如果是一个空数组，回调函数只会执行一次
1. 除了这两种情况之外，其他都是通过比较 deps 的每个元素是否改变来决定是否执行回调函数
1. useMemo 或者 useCallback 也是用同样的方式处理 deps

---

说回 hooks 的 closure trap
上面的例子中 deps 参数是一个空数组，所以回调函数只会执行一次，需要被执行的回调函数会被标记上 Hook(HasEffect)并且之后会被执行：
![1_cLJig3k-pHM7fV2TTJdDrQ.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1657777774545-1de764b1-fb39-43c3-acd6-a7a05217d858.png#clientId=u06c2f962-ebf5-4&crop=0&crop=0&crop=1&crop=1&from=drop&height=262&id=u28e8b9cc&margin=%5Bobject%20Object%5D&name=1_cLJig3k-pHM7fV2TTJdDrQ.png&originHeight=824&originWidth=1225&originalType=binary∶=1&rotation=0&showTitle=true&size=698254&status=done&style=none&taskId=u467f7911-de94-4408-9e2f-656ed9a3579&title=react%2016&width=390 "react 16")

```typescript
function commitHookEffectListUnmount(
  flags: HookFlags,
  finishedWork: Fiber,
  nearestMountedAncestor: Fiber | null,
) {
  const updateQueue: FunctionComponentUpdateQueue | null = (finishedWork.updateQueue: any);
  const lastEffect = updateQueue !== null ? updateQueue.lastEffect : null;
  if (lastEffect !== null) {
    const firstEffect = lastEffect.next;
    let effect = firstEffect;
    do {
      if ((effect.tag & flags) === flags) {
        // Unmount
        const destroy = effect.destroy;
        effect.destroy = undefined;
        if (destroy !== undefined) {
          safelyCallDestroy(finishedWork, nearestMountedAncestor, destroy);
        }
      }
      effect = effect.next;
    } while (effect !== firstEffect);
  }
}

function commitHookEffectListMount(flags: HookFlags, finishedWork: Fiber) {
  const updateQueue: FunctionComponentUpdateQueue | null = (finishedWork.updateQueue: any);
  const lastEffect = updateQueue !== null ? updateQueue.lastEffect : null;
  if (lastEffect !== null) {
    const firstEffect = lastEffect.next;
    let effect = firstEffect;
    do {
      if ((effect.tag & flags) === flags) {
        // Mount
        const create = effect.create;
        effect.destroy = create();
        //...
      }
      effect = effect.next;
    } while (effect !== firstEffect);
  }
}
```

由于 deps 在这里是一个空数组，所有没有 HookHasEffect 标记，回调函数也就不会再被执行。
所以定时器 setInterval 只会被设置一次。因此，他的回调函数所引用的状态始终是初始状态，无法获得最新的状态。
解决方法：
每次重新渲染的时候都要让回调函数执行一次，即应该把 count 放在依赖数组中

```typescript
const [count, setCount] = useState(0);
useEffect(() => {
  setInterval(() => {
    setCount(count + 1);
  }, 1500);
}, [count]);
useEffect(() => {
  setInterval(() => {
    console.log(count);
  }, 1500);
}, [count]);
```

![kKP8JvICPl.jpg](https://cdn.nlark.com/yuque/0/2022/jpeg/115484/1657782415240-6ef5a049-8315-47bd-97c2-826fbf80f5c5.jpeg#clientId=u00d3ff6b-076b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=419&id=ub57a6dd6&margin=%5Bobject%20Object%5D&name=kKP8JvICPl.jpg&originHeight=692&originWidth=995&originalType=binary∶=1&rotation=0&showTitle=false&size=101462&status=done&style=none&taskId=ube855ea3-751e-4b1b-83cc-21818bfa224&title=&width=603.0302681760922)
这个时候看上去回调函数获取到了最新的 count，但是打印出来的结果似乎很混乱。这是因为每个 effect 都会创建一个定时器，所以需要清除上一个 effect 的定时器

```typescript
const [count, setCount] = useState(0);
useEffect(() => {
  const timer = setInterval(() => {
    setCount(count + 1);
  }, 1500);
  return () => clearInterval(timer);
}, [count]);
useEffect(() => {
  const timer = setInterval(() => {
    console.log(count);
  }, 1500);
  return () => clearInterval(timer);
}, [count]);
```

![origin_img_v2_9c44d06d-7017-4b8c-85f6-50db130503bg.jpg](https://cdn.nlark.com/yuque/0/2022/jpeg/115484/1657782596834-1a8714e7-599a-49c8-a1a7-a1feec5d836c.jpeg#clientId=u00d3ff6b-076b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=447&id=uee20bf60&margin=%5Bobject%20Object%5D&name=origin_img_v2_9c44d06d-7017-4b8c-85f6-50db130503bg.jpg&originHeight=738&originWidth=701&originalType=binary∶=1&rotation=0&showTitle=false&size=69372&status=done&style=none&taskId=u0ff7fc63-050d-46cf-a977-8ac8dd41748&title=&width=424.84846029290514)
总结：

- memorizedState 链表被存储在 fiberNode 中。链表的节点和组件中的 hooks 一一对应，每个 hook 通过对应的节点访问数据
- 类似 useEffect,useMemom 和 useCallback 这样的 hook 都有一个 deps 参数。重新渲染的时候，新老 deps 每次都会被比较，如果不相同，回调函数就会被重新执行
- 如果不传第二个参数，hook 会在每次渲染中执行，参数为[]的只会执行一次
- closure trap 发生的原因是 hook 里使用了一个特定的值但是并没有添加到依赖数组中，所以即使值变化了，回调函数也不会再次被执行
- 只需要添加依赖项即可解决这个问题，但是同时需要注意清除定时器

[
](https://betterprogramming.pub/understanding-the-closure-trap-of-react-hooks-6c560c408cde)
