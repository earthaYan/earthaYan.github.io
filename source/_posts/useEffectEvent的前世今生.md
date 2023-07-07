---
title: useEffectEvent的前世今生
date: 2023-07-06 20:00:48
tags:
---

去年 React 团队分享了一个新 Hook `useEvent` 的[RFC220](https://github.com/reactjs/rfcs/pull/220),完整 RFC 内容见[useEvent](https://github.com/reactjs/rfcs/blob/useevent/text/0000-useevent.md)。这个 Hook 的来源是[#14099](https://github.com/facebook/react/issues/14099)。 useEvent 的[原型](https://github.com/facebook/react/pull/25229)已经实现，但是今年 1 月份关闭了`useEvent`提案，为什么会关闭呢，主要有以下几个原因：

1. 将渲染优化和“修复”Effect 耦合在一个提案下，很难实现
2. 容易诱导开发者将当前使用 `useCallback` 包裹的函数都替换成 `useEvent`
   
   
但是关闭提案并不意味着全盘否定，事实上，只是对其进行了拆分。针对渲染优化，React 团队准备开发一个[自动记忆编译器](https://www.youtube.com/watch?v=lGEMwh32soc)，而针对修复 Effect，则发布了一个 `useEffectEvent`的新的 Hook。

官方之前在RFC给出的 useEvent 的大概实现如下所示，当然这不是真正的实现，真正的实现肯定比这个复杂得多：

```javascript
// (!) Approximate behavior
function useEvent(handler) {
  const handlerRef = useRef(null);
  // 渲染之前运行
  useLayoutEffect(() => {
    handlerRef.current = handler;
  });
  return useCallback((...args) => {
    // 渲染期间执行的话，会抛出错误
    const fn = handlerRef.current;
    return fn(...args);
  }, []);
}
```

下面就借助代码来讲述一下这个新的 Hook 应该怎么使用。
当前存在的问题：
你创建了一个聊天连接，把当前的 message 存储在 state 变量中，每次输入的时候更新 message,当用户准备好后就可以发送。

```javascript
function Chat() {
  const [message, setMessage] = React.useState("");
  const sendMessage = (val) => {
    console.log(val);
  };
  const onSend = () => {
    sendMessage(message);
  };
  return (
    <>
      <Input onSend={onSend} setMessage={setMessage} />
    </>
  );
}
```

在上面的例子中，由于 `onSend` 的函数引用每次都会变化，即每次的 `onSend` 都是重新创建的不同的函数，这会直接破坏 Input 组件的 memo 效果，原因是当一个组件被 memoize 后,会对 props 进行浅层比较来决定是否需要重新渲染。如果 props 是“浅相等”(同一个引用),就跳过重新渲染。而 `onSend` 每次都跟上一次不一样。

那如何优化呢？很明显可以使用`useCallback`包裹`onSend`函数，保证只有 state 变量变化时，`onSend`函数才会被重新创建。

```javascript
const onSend = React.useCallback(() => {
  sendMessage(message);
}, [message]);
```

通过这个修改，Input 组件只有在 `onSend` 函数重新创建的时候 `Input` 组件才会重新渲染。但是这样并不完全契合我们的预期，因为每当 message 变化， `onSend` 函数还是会被重新创建。但是如果去掉依赖项，就获取不到最新的 message 值。

{% asset_img recreate.png %}

还可以通过 ref 修复这个问题:使用 sendRef 存储事件处理函数，这样你输入的时候 onSend 函数会一直保持为同一个函数标识符

```javascript
const sendRef = React.useRef(null);
React.useLayoutEffect(() => {
  sendRef.current = () => sendMessage(message);
});
const onSend = React.useCallback((...args) => {
  return sendRef.current(...args);
}, []);
```

尽管这个方法能解决我们的问题，但是很明显牺牲了代码可读性。基于以上的问题，React 团队推出了一个新的 Hook `useEffectEvent`，使用起来非常方便。

但是因为这个 Hook 目前还没有在稳定版 React 中发布，所以需要先安装实验版本的 React

```bash
npm install react@experimental
npm install react-dom@experimental
npm install eslint-plugin-react-hooks@experimental
```

现在只需要直接用 `useEffectEvent` 将回调函数包裹起来就可以

```javascript
import { experimental_useEffectEvent as useEffectEvent } from "react";
const onSend = React.experimental_useEffectEvent(() => {
  sendMessage(message);
});
```

新的 Hook useEffectEvent 允许用户定义一个函数，可以一直读取到最新的 props/state，但是和这个函数会有一个稳定的标识符，所以他不会破坏缓存，也不会重新触发 Effect,可以减少不必要的渲染。它和 `useCallback` 的区别是:

1. 重渲染次数的显著不同：
   {% asset_img retrigger.png %}
2. useEffectEvent 不需要依赖项列表

useEvent 的返回值，它的行为就和普通函数一样，所以也可以给他传递参数，比如 `roomID`

```javascript
const onSend = useEffectEvent((roomID) => {
  sendMessage(roomID, message);
});
onSend(roomID);
```

回到 Chat 组件，每当 roomID 变化时就展示一个成功的 alert 并清空 message,使用 useEffect 可以达到目的。

```javascript
function Chat() {
  const [message, setMessage] = React.useState("");
  const [roomID, setRoomID] = React.useState("reavel");
  const sendMessage = (val) => {
    console.log(val);
  };
  const onSend = React.experimental_useEffectEvent(() => {
    sendMessage(message);
  });
  React.useEffect(() => {
    if (!!roomID) {
      showNotification("Changed room->" + roomID, "dark");
      setMessage("");
    }
  }, [roomID]);
  return (
    <>
      <div>
        <select
          onChange={(e) => {
            setRoomID(e.target.value);
          }}
        >
          <option value="travel">travel room</option>
          <option value="music">music room</option>
          <option value="sport">sport room</option>
        </select>
      </div>
      <Input onSend={onSend} setMessage={setMessage} message={message} />
    </>
  );
}
```

但是如果 toast 是从当前的主题上下文中读取的话，代码检查工具会提示你需要将 theme 添加到依赖项中

```javascript
function Chat() {
  const theme = useContext(ThemeContext);
  const [message, setMessage] = useState("");
  const onSend = useEffectEvent(() => {
    setMessage(message);
  });

  React.useEffect(() => {
    if (!!roomID) {
      showNotification("Changed room->" + roomID, theme);
      setMessage("");
    }
  }, [roomID, theme]);
  return <Input onSend={onSend} />;
}
```

实际上主题色变化的时候，连接的房间并没发生变化，所以实际上我们并不需要重新展示消息。我们可以使用 `useCallback` 将代码从 `useEffect` 中提取出来。

```javascript
const theme = useContext(ThemeContext);
const onChangedRoom = useCallback(() => {
  showNotification("Changed room->" + roomID, theme);
  setMessage("");
}, [theme]);
useEffect(() => {
  onChangedRoom();
}, [roomID]);
return <Input onSend={onSend} />;
```

但是因为 `useEffectEvent` 在防止不必要的重渲染上更有意义,所以我们使用 `useEffectEvent` 包裹对应的代码，使它变成非响应式代码。

```javascript
const theme = useContext(ThemeContext);
const onChangedRoom = useEffectEvent(() => {
  showNotification("Changed room->" + roomID, theme);
  setMessage("");
});
useEffect(() => {
  onChangedRoom();
}, [roomID]);
return <Input onSend={onSend} />;
```

这样既减少了不必要的重渲染，代码可读性也得到了改善。

那哪些情况不适合用 useEvent 呢？即需要在渲染期间调用的函数,因为useEvent在渲染期间运行会抛出错误
```javascript
function ThemedGrid() {
  const theme = useContext(ThemeContext);
  const renderItem = useCallback(
    (item) => {
      // 渲染期间调用，所以他不是一个事件
      return <Row {...item} theme={theme} />;
    },
    [theme]
  );
  return <Grid renderItem={renderItem} />;
}
```
代码：https://stackblitz.com/edit/stackblitz-starters-ida8fu
