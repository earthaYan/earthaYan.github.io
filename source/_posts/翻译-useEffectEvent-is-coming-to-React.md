---
title: 翻译-useEffectEvent-is-coming-to-React
date: 2023-07-03 13:38:37
tags: [翻译, React]
categories: 翻译
---

原文地址：https://vived.io/useeffectevent-is-coming-to-react-frontend-weekly-vol-118/

## useEvent 已死, useEffectEvent 万岁！

六个多月前，React 团队向全世界分享了一个有关新 hook `useEvent` 的意见征求。它本该返回一个稳定的函数引用。同时函数内的 state 也应该总是对应组件的当前 state。这种行为可以非常有效地优化不必要的渲染。

```javascript
function Chat() {
  const [text, setText] = useState('');
  // 🟡 只要`text` 变化，就返回一个不同的函数
  const onClick = useCallback(() => {
    sendMessage(text);
  }, [text]);

  return <SendButton onClick={onClick} />;
}
```

```javascript
function Chat() {
  const [text, setText] = useState('');
  // ✅总是返回相同的函数 (即使 `text` 变化)
  const onClick = useEvent(() => {
    sendMessage(text);
  });
  return <SendButton onClick={onClick} />;
}
```

不幸的是，RFC 完成了它的工作并展开了许多讨论。最终，这些讨论引发了了 Hook 创建者心里的疑虑，他们决定暂停其实现。此时两个反对的论据浮出了水面。首先，用户可能会这个新 Hook 当做优化版的`useCallback`，将两者混淆。事实上，这两个 hook 本应该有稍微不同的功能。其次，除了 `useEvent` 之外，开发者还致力于开发一个能够实现函数调用自动缓存的编译器。同时处理这两个功能太麻烦了。
> 当一个函数接收相同的参数时,并不需要重新计算结果,而是直接使用缓存的结果。这就是 memoization 的工作原理。

所有迹象都表明 `useEvent` 将会以另一种形式回到我们视野。一个神秘的PR出现在了React的仓库中。它将 `useEvent` 重命名为  `useEffectEvent` ,且稍微改变了一下它的行为。从现在起，这个函数不会返回一个稳定的引用，但是你仍然可以在`useEffect` 中引用它，而不需要将其指定为依赖项。

```javascript
function Chat() {
  const [text, setText] = useState('');
  const [state, setState] = useState<State>('INITIAL');

  const onHappened = useEffectEvent(() => {
    logValueToAnalytics(text);
  });

  useEffect(() => {
    onHappened();
  }, [state]);

  return (/*...*/);
}
```

现在这个PR还没有完整的RFC文档描述，所以很难预测`useEffectEvent` 的未来或者对他的功能做出更清楚的结论。毫无疑问，当RFC最终出现的时候，会提供更多的上下文，并且你肯定会在我们的周报中读到它。

参考链接：

1. [useEvent 命名为 useEffectEvent](https://github.com/facebook/react/pull/25881)
2. [useEvent 完整提案](https://github.com/reactjs/rfcs/blob/useevent/text/0000-useevent.md)
3. [useEvent 提案描述](https://github.com/reactjs/rfcs/pull/220)
