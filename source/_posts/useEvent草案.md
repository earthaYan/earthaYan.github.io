---
title: useEvent草案
date: 2023-07-03 23:49:34
tags: [React, RFC]
categories: React
---

- Start Date: 2022–05-04
- RFC PR: (leave this empty)
- React Issue: https://github.com/facebook/react/issues/14099

# 总结

这个 Hook 定义了一个事件处理函数，这个函数有着稳定的函数标识。

# 基础示例

你可以将任何事件处理函数包裹进 `useEvent`。

```js
function Chat() {
  const [text, setText] = useState('');

  const onClick = useEvent(() => {
    sendMessage(text);
  });

  return <SendButton onClick={onClick} />;
}
```

`useEvent` 内部的代码可以“看到”调用时的 props/state 值。即使引用的 props/state 变了，返回的函数还是有一个稳定的标识。这里没有依赖数组。

# 动机

## 在事件处理函数中读取 state/props 会破坏优化

这个事件处理函数 `onClick` 需要读取当前输入的 needs `text`:

```js
function Chat() {
  const [text, setText] = useState('');

  // 🟡 一直是不同的函数
  const onClick = () => {
    sendMessage(text);
  };

  return <SendButton onClick={onClick} />;
}
```

假设你想要通过将它包裹进 `React.memo` 来优化 `SendButton` 组件。为了让它生效，props 需要在两次重渲染之间做浅层比较。而 `onClick` 函数每次重渲染的时候都会有一个不同的函数标识符，所以它会破坏缓存。

解决像这样的问题最常见的方式是将函数包裹进 `useCallback` 来维持函数标识符。但是它在这个场景下丝毫没有帮助，因为 `onClick` 需要读取最新的 `text`。

```js
function Chat() {
  const [text, setText] = useState('');

  // 🟡无论何时只要`text`变化就是不同的函数
  const onClick = useCallback(() => {
    sendMessage(text);
  }, [text]);

  return <SendButton onClick={onClick} />;
}
```

在上面的例子中，`text` 会随着输入变化，所以 `onClick` 在每次输入时仍然是不同的函数。（我们不能将`text`从 `useCallback` 的依赖项中移除，因为这样 `onClick` 处理函数会一直只能“看到”初始的 text。）

相比之下， `useEvent` 没有使用依赖项数组，并且即使 `text` 变了也总是返回相同的稳定的函数。然而， `useEvent` 里面的 `text` 会反映它最新的值：

```js
function Chat() {
  const [text, setText] = useState('');

  // ✅ 一直是同一个函数(即使 `text` 变了)
  const onClick = useEvent(() => {
    sendMessage(text);
  });

  return <SendButton onClick={onClick} />;
}
```

最终缓存 `SendButton` 组件将会生效，因为它的 `onClick` prop 会一直接收到同一个函数。

## 当事件处理函数变化时，`useEffect` 不应该再次触发

在这个例子中， `Chat` 组件有一个 Effect，这个 Effect 会连接选定的房间。当你加入房间或者收到一个消息时，它会使用选中的 `theme` 展示一个 toast,且因为`muted`设置，它可能会播放声音：

```js
function Chat({ selectedRoom }) {
  const [muted, setMuted] = useState(false);
  const theme = useContext(ThemeContext);

  useEffect(() => {
    const socket = createSocket('/chat/' + selectedRoom);
    socket.on('connected', async () => {
      await checkConnection(selectedRoom);
      showToast(theme, 'Connected to ' + selectedRoom);
    });
    socket.on('message', (message) => {
      showToast(theme, 'New message: ' + message);
      if (!muted) {
        playSound();
      }
    });
    socket.connect();
    return () => socket.dispose();
  }, [selectedRoom, theme, muted]); // 🟡 当他们变化时，都会导致Effect重新运行
}
```

A problem with this implementation is that changing `theme` or `muted` will cause the socket to reconnect. This is because `theme` and `muted` are used inside the effect, and so they have to be specified in the effect dependency list. When they change, the effect has to re-run, destroying and recreating the socket.

If you move these socket callbacks out of the effect and wrap them into `useCallback`, their dependency lists would still have to include `theme` and `muted`. So if `theme` or `muted` change, the callbacks will change their identity, and the effect (which depends on these callbacks) will have to re-run. So `useCallback` doesn’t solve this problem.

You might be tempted to ignore the linter and “skip” `theme` and `muted` in the list of dependencies. However, that would introduce a bug. If you omit them from the list of dependency list, then the effect will keep “seeing” their initial values. As a result, even if user changes from the light to a dark theme, the subsequent toasts would keep appearing with a light theme. Switching the muted setting would also have no effect. (In general, “capturing” values is [usually desirable](https://overreacted.io/how-are-function-components-different-from-classes/) in components. It turns into a pitfall only when you suppress the linter error.)

`useEvent` provides an idiomatic solution to this problem:

```js
function Chat({ selectedRoom }) {
  const [muted, setMuted] = useState(false);
  const theme = useContext(ThemeContext);

  // ✅ Stable identity
  const onConnected = useEvent((connectedRoom) => {
    showToast(theme, 'Connected to ' + connectedRoom);
  });

  // ✅ Stable identity
  const onMessage = useEvent((message) => {
    showToast(theme, 'New message: ' + message);
    if (!muted) {
      playSound();
    }
  });

  useEffect(() => {
    const socket = createSocket('/chat/' + selectedRoom);
    socket.on('connected', async () => {
      await checkConnection(selectedRoom);
      onConnected(selectedRoom);
    });
    socket.on('message', onMessage);
    socket.connect();
    return () => socket.disconnect();
  }, [selectedRoom]); // ✅ Re-runs only when the room changes
}
```

We’ve separated the effect (“set up a socket”) from the events that it causes (“connected to a room”, “received a message”). By doing that, we’ve also fixed the issue (the socket no longer reconnects on theme change).

The dependency linter will be changed to accept this code. It is valid to omit `onConnected, onMessage` from the dependency list because they are declared with `useEvent` — and the linter will know that `useEvent` returns functions with a stable identity. (This is similar to how you can omit `setState` if the linter can trace it to a declaration in the same component.) Even if you include `onConnected, onMessage` in dependencies, they won’t cause the effect to re-run because they’re stable.

The effect depends on `selectedRoom`, so when the room changes, the socket needs to reconnect. However, note that the effect does not need to depend on `theme` or `muted` because they’re not used inside the effect. The `useEvent` calls can read any “fresh” value at the time of the event handler call without changing the function identity of the event itself.

### Passing arguments to events

When you call `onConnected` or `onMessage`, the `theme` and `muted` variables inside are “fresh” and capture their values at the time of the event call. However, you might also want to pass some information from the “past”.

In the above example, if `selectedRoom` changes (say, from “Room A” to “Room B”) while `checkConnection("Room A")` is being awaited, reading the `selectedRoom` inside the `onConnected` event will give you the latest value (“Room B”). But the room you’ve just connected to (and which should appear in the toast) is “Room A”. The value we want is not the _latest_ value but the one that _caused_ this event. This is why we pass it as a part of the event call (“Connected to Room A”), and `onConnected` receives `connectedRoom` as an argument:

```js
const onConnected = useEvent((connectedRoom) => {
  console.log(selectedRoom); // already "Room B"
  showToast(theme, 'Connected to ' + connectedRoom); // "Room A" passed from effect
});
```

The `theme` is not a part of “what happened” (you didn’t “Connect to Room A with the light theme”), so it makes sense to read its fresh value inside the event. Depending on the use case, you can pass arguments to events, read fresh values inside events, or use a mix of both.

### Wrapping events at the usage site

Functions can be wrapped with `useEvent` further down from their definition — for example, in a custom Hook:

```js
function Chat({ selectedRoom }) {
  const [muted, setMuted] = useState(false);
  const theme = useContext(ThemeContext);

  const onConnected = (connectedRoom) => {
    showToast(theme, 'Connected to ' + connectedRoom);
  };

  const onMessage = (message) => {
    showToast(theme, 'New message: ' + message);
    if (!muted) {
      playSound();
    }
  };

  useRoom(selectedRoom, { onConnected, onMessage });
  // ...
}

function useRoom(room, events) {
  const onConnected = useEvent(events.onConnected); // ✅ Stable identity
  const onMessage = useEvent(events.onMessage); // ✅ Stable identity

  useEffect(() => {
    const socket = createSocket(room);
    socket.on('connected', async () => {
      await checkConnection(room);
      onConnected(room);
    });
    socket.on('message', onMessage);
    socket.connect();
    return () => socket.disconnect();
  }, [room]); // ✅ Re-runs only when the room changes
}
```

Here, it doesn’t matter whether the passed callbacks are memoized or wrapped in `useEvent`. The `useRoom` custom Hook ensures that the passed event handlers are wrapped, so they have a stable identity and never re-trigger the effect.

If the parent passes a `useEvent` function as a prop or an argument to a custom Hook, and it's wrapped into `useEvent` again in the child component or a custom Hook, it will still work (with minor overhead from double wrapping). It is plausible that with static typing enforcement, `useEvent` could be modeled as an opaque type, and custom Hooks or components could declare that certain props or arguments must be “event functions”. This opens up several questions that are out of scope of this RFC (see “static typechecking” below).

### Extracting an event from an effect

In the earlier example, it was easy to classify `onConnected` and `onMessage` as events because they were passed to a `socket.on(...)` event subscription. However, the concept is more general and applies in more cases. Whenever you have an effect where re-firing on data change doesn’t make sense, the idiomatic solution will often be to extract an event from it.

Consider this example that logs a page visit analytics event:

```js
function Page({ route, currentUser }) {
  useEffect(() => {
    logAnalytics('visit_page', route.url, currentUser.name);
  }, [route.url, currentUser.name]);
  // ...
}
```

Initially, it might work fine. Later you add a Settings screen that lets the user change their name. Now you notice that the analytics logs are fired whenever the user types into the input because `currentUser.name` is changing. But this doesn’t make sense: the user changing their name doesn’t constitute a new visit to the page!

This observation gives us a hint: conceptually, “User visited the page” is itself an event — something that “happens” at a particular time (for example, in response to user interaction). “Re-triggering” that event doesn’t make sense even if the data changes. Let's extract the event:

```js
function Page({ route, currentUser }) {
  // ✅ Stable identity
  const onVisit = useEvent((visitedUrl) => {
    logAnalytics('visit_page', visitedUrl, currentUser.name);
  });

  useEffect(() => {
    onVisit(route.url);
  }, [route.url]); // ✅ Re-runs only on route change
  // ...
}
```

Now our code is split in two parts. The “reactive” part of the code — which re-fires whenever its inputs change — is in the effect. Specifically, changing `route.url` causes the effect to re-fire. Whenever the URL changes, the “The page /somepage was visited” event fires, and we call `onVisit(route.url)`. Then, the “non-reactive” part of the code — which can read fresh values like `currentUser.name` but does not need to re-trigger when it changes — is inside the event.

When an effect doesn't do anything except calling an event, it's often a sign that there may be a better place to put that code than an effect. For example, the analytics log call might better be placed in a route change handler (conceptually, it's an event!) rather than as an effect caused by the page re-render. Thinking in terms of events and effects helps notice when effects are not necessary.

# 细节设计

## 内部实现

内部实现上， `useEvent` Hook 大概会像这样工作：

```js
// (!) 大概的行为

function useEvent(handler) {
  const handlerRef = useRef(null);

  // 在实际实现里，这会在layout effect 之前运行
  useLayoutEffect(() => {
    handlerRef.current = handler;
  });

  return useCallback((...args) => {
    // 在实际实现中，如果在渲染期间调用将会抛出错误
    const fn = handlerRef.current;
    return fn(...args);
  }, []);
}
```

换句话说，他提供了一个稳定的函数，用这个函数来调用你传入的最新版函数。

内置的 `useEvent` 会和上面的实现稍有不同。

包裹在 `useEvent` 中的时间处理函数 **如果在渲染期间被调用就会抛出错误**（但是从 Effect 中调用或者在其他时间调用则没有问题）。所以在渲染期间这些函数会被强制性当做不透明并且从不会被调用。尽管内部的 props/state 变化了，但是他们的函数标识符因为上述原因仍能很安全地保持住。因为他们在渲染期间不会被调用，不会影响渲染的最终输出 - 所以当输入变化时他们也不需要变化（即他们不是“响应式”的）。

事件处理函数的“当前”版本在所有的 layout effect 运行之前就被切换了。这避免了用户级版本中在一个组件的 Effect 可以监听另一个组件上一个版本的 state 的用户级版本中的缺陷展示。但是切换的精确时间是一个开放的问题（在底部的开放问题列表中）。

作为优化，当服务端渲染时， `useEvent` 会为所有调用返回相同的抛出错误。这种方式很安全因为事件不存在于服务端。这个优化可能会提高 SSR 的性能，因为它可以让打包 SSR 代码的框架从 SSR 的 bundle 中剥离出事件处理函数（以及他们的依赖项）。（注意这意味着像 `fn1 === fn2` 这样的比较将不能可靠的区分两个不同的事件处理函数）

## 代码检查插件

依赖项检查将把作用域中的 `useEvent` 返回值当做“稳定值”处理，所以他们在依赖项列表中是可选的（和当下对 `setState` 函数的处理方式类似）。从父组件中传入的 `useEvent` 函数将不得不被声明为依赖项。当你在 Effect 内部使用普通函数时，如果函数的名称以`on` 或者 `handle`开头，代码检查工具的“建议”会生成使用 `useEvent` 而不是`useCallback` 包裹。

在未来，如果你在 effect 依赖项中有 `handle*` 或者 `on*` 函数的话，让代码检查工具发出警告可能是有意义的。这个解决方案将会将他们包裹进同一个组件中的 `useEvent` 。这让你可以确定：事件处理函数不会导致 effect 重新触发（因为它的标识符一直是稳定不变的）并且把它放在依赖项也是没有意义的。

## 静态类型检查

最简单的方法就是 `useEvent`接受一个函数并返回一个同样形式的函数。但是将来可能有机会在类型系统层面添加新的约束，这将为静态检查错误铺平道路，比如在渲染期间使用 DOM 操作。我们计划在未来的 RFC 中探索这个问题。

## 什么时候不应该使用 `useEvent`

### 渲染期间的函数调用仍然使用 `useCallback`

一些函数需要被缓存，且渲染期间被调用。 `useCallback`对这些场景有效：

```js
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

由于 `useEvent` 函数在渲染期间调用会抛出错误，这不是什么大问题。

### 不是所有在 Effect 依赖项中的函数都是事件

在下面的例子中， `createSocket` 接收通过上下文传递的 `createKeys` 函数：

```js
function Chat({ selectedRoom }) {
  const { createKeys } = useContext(EncryptionSettings);
  // ...
  useEffect(() => {
    const socket = createSocket('/chat/' + selectedRoom, createKeys());
    // ...
    socket.connect();
    return () => socket.disconnect();
  }, [selectedRoom, createKeys]); // ✅ 当room 或者createKeys 变化时重新运行
}
```

此例子中的 `createKeys` 不是 event，所以它应该被指定为 effect 依赖项。这保证了如果用户聊天时修改了加密设置，且不同的函数作为`createKeys`被传入时， 它都将导致 API 重新连接。

### 不是所有从 effect 中提取的函数都是 event

这里有一个例子，一段代码被错误地标记为 event：

```js
function Chat({ selectedRoom, theme }) {
  // ...
  // 🔴 这不应该是Event
  const createSocket = useEvent(() => {
    const socket = createSocket('/chat/' + selectedRoom);
    socket.on('connected', async () => {
      await checkConnection(selectedRoom);
      onConnected(selectedRoom);
    });
    socket.on('message', onMessage);
    socket.connect();
    return () => socket.disconnect();
  });
  useEffect(() => {
    return createSocket();
  }, []);
}
```

这段代码是有问题的：因为 effect 不再依赖于 `selectedRoom`，所以修改 roomId 将不会重新创建 socket。这个问题在于将 `createSocket` 分类到了 event。根据经验，将 event 当做是在特定时间点客观发生的事情会很有帮助（“用户访问了一个页面”，“连接到房间”，“收到消息”）而不需要关注如何组织代码。如果函数名称以 `on`或者 `handle`开头，那它很可能就是一个 event。相反，event 不应该需要有清理代码（因为他们代表着离散的时间点）

# 缺点

- 这给 React 增加了一个新概念。人们已经因为定义函数时的最佳实践（“我应该在任何地方都使用 `useCallback` 吗”）而苦苦挣扎，而它又增加了一层。

  - 这是最大的问题。但是我们认为这个概念在 React 实际使用中是不可避免的，所以它受益于顶层的 API，共享词汇以及一系列的最佳实践。在 [#14099](https://github.com/facebook/react/issues/14099)和[#16956](https://github.com/facebook/react/issues/16956)中， `useCallback` 失效问题是投票最高的问题之一，同时也在我们的 FAQ 中，并且也是引入 Hook 后我们需要[写作](https://www.youtube.com/watch?v=lGEMwh32soc)的早期模式之一。即使在[编译器已经做了缓存](https://www.youtube.com/watch?v=lGEMwh32soc)的世界，我们也必须区别优化和关于重新触发的语义保证。我们怀疑 `useEvent` 是 Hook 编程模式中缺失的基础不分且它可以提供正确的方式修复过度触发 Effect 的问题，而不是像跳过依赖项这样的易出错的 hack 方式。

- 和普通的事件处理函数相比，使用 `useEvent` 包裹看上去更具干扰性。
  - However, it makes more sense to compare it with `useCallback` which people use today to solve the same problems. Many (likely the majority) of `useCallback` wrappers are used for functions that are never called during render, so they can be replaced with `useEvent`. Compared to them, `useEvent` is an ergonomic improvement (no dependency list and no invalidation). And it is optional, so if you prefer you can keep the code as is.
- `useEvent` 让术语 "event handler" 的含义不止于 DOM 事件处理函数
  - It could be called something like `useStableCallback` or `useCommittedCallback`. However, the whole point is to encourage using it for event handlers. Having a short name helps, and "is this an event handler?" is a good rule of thumb for the majority of cases when you want to use it. Even in effects, the cases where you'd want to extract a part of logic into an event corresponds to when you want to express "something happened!" (e.g. the user visited a page, and you want to log that). Conceptually, these "events" are similar to Events in Functional Reactive Programming. But most importantly, it is already common in React to refer to any `on*` callback prop as an "event handler", regardless of whether it corresponds to any actual DOM event (e.g. `onIntersect`, `onFetchComplete`, `onAddTodo`). `useEvent` is exactly the same concept.
- 和 `useCallback`相比, `useEvent` 的实现在提交阶段增加了额外的工作
  - However, in practice this pattern is already widespread. Having a built-in way to do this and a set of best practices seems better overall than ad-hoc solutions that exist in many libraries and products but suffer from timing flaws.
- 有一些边缘用例，但我们不认为他们是破坏因素
  - Unmounting layout effects will observe the previous version of the event callback but unmounting non-layout effects will run after the switch, so they will observe the next version. This is similar to how reading a ref during unmounting layout and non-layout effects produces different results.
  - The values in the event handler correspond to the values at the time it was called. This means that you don’t get truly “live” bindings. For example, if you have `async`/`await` inside an event and you read some prop after the `await`, the value will be the same as before the `await`. To get a “fresh” value again, you would need to step into another event. For this reason, events should usually not be asynchronous. It’s best to treat them as fire-and-forget: “here’s what just happened”
  - The “conditional event” case like `onSomething={cond ? handler1 : handler2}`. In this case, if you use `onSomething` as an effect dependency, it would re-fire when `cond` changes. You can “protect” against it by moving the `useEvent` wrapping to the same component as the effect that calls `onSomething`. We may consider adding more runtime or linter warnings if this case ends up common.

# 备选方案

> "invalidate"（失效）指的是回调函数被重新创建的过程

- 现状:`useCallback` 失效过于频繁，且目前没有内置的解决方案。同时过度触发 effect 也没有内置的解决方案。我们认为这是不应该的，需要一个解决方案。
- 和`useEvent` 有所不同的命名，例如 `useStableCallback`。我们认为会使其更难以确定何时使用它。更长或者更复杂的名字也更加不符合人类认知。
- 将 `useEvent` 行为提供给 `useCallback`。我们不想要这么做，因为他们的语义已经非常不同。
- React 强制事件处理函数始终使用 `useEvent`声明。这一点看上去为时过早。
- 增加一个读取任意值的“最新”版的 API。我们发现这在实践中会受到干扰，因为代码块经常需要读取多个值。当代码量增加时，比起标记单个的值，标记整个代码块（函数）更加方便，并且以更加通用的方式解决同一个问题。
- 给 `useEffect` 添加一些特殊的 API。我们认为这不够普遍，因为缓存事件处理函数的问题也是一样的，所以可以共用的解决方案会更好。
- 提案相同，但是允许在渲染期间调用事件处理函数。我们认为这会导致过多的自伤行为。
- 提案相同，但是“当前”版本切换的时间不一样。这是一个开放的问题。
- 提案相同，但是提供不同的代码检查行为或者运行时告警。比如，如果向 effect 的依赖项传递了一个 event，就在运行时发出告警，然后使用 lint 排除 event 作为依赖项。

# 采用的策略

这个 Hook 将会在小版本中发布。修改依赖项检查的建议，会建议把以 `on*` 或者 `handle*` 开头的函数包裹进`useEvent`，而不是建议 `useCallback`。写新文档讲普通模式。

`useCallback` 在渲染期间使用函数的场景下仍然有用。但是它的重要性可能会随着时间而减小，因为它不需要经常被用到了。

针对 `useEvent` 高度优化的 polyfill 不可能实现，因为在 React 中没有我们可以用来在正确的时间切换 `.current` 的生命周期或 Hook。尽管[`use-event-callback`](https://github.com/Volune/use-event-callback)在许多情况下已经“足够接近”，但它在渲染期间不会抛出错误，并且时间也不绝对正确。React 有一个版本包含了内置的 `useEvent` 实现后我们才会推荐采用这种方式。

# 我们怎么讲授它

教会如何将函数包裹进去是非常容易的。教会如何利用它解决问题会更困难一点。

我们也许可以在文档中比 `useEffect` 或者 `memo` 更早地引入 `useEvent` ，因为你不需要了解引用标识 或者依赖项就可以使用它。接下来，当你解决他们的问题(如破坏缓存，重新触发 effect)的解决方案就是基于你已经知道如何使用的 API。

# 还未解决的问题

- “当前的”函数切换的时间并不准确
- 使用旧值卸载 layout effect 来“看”事件处理函数是否有意义
- 使用旧值卸载 non-layout effect 来“看”事件处理函数是否有意义
- 从 effect 的清理函数中调用事件处理函数是否是反面模式，是否应该发出警告
- 究竟如何修改代码检查工具的建议
- 对于这个 Hook,在后续 RFC 中找出完整的 story 是否是一个障碍
