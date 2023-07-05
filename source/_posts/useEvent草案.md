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

在上面的例子中，`text` 会随着输入变化，所以 `onClick` 在每次输入时仍然是不同的函数。（我们不能将`text`从 `useCallback` 的依赖项中移除，因为这样 `onClick` 处理函数会一直只能“看到”初始的text。）

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

在这个例子中， `Chat` 组件有一个 Effect，这个Effect会连接选定的房间。当你加入房间或者收到一个消息时，它会使用选中的 `theme` 展示一个toast,且因为`muted`设置，它可能会播放一种声音：

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

## Internal implementation

Internally, `useEvent` Hook will approximately work like this:

```js
// (!) Approximate behavior

function useEvent(handler) {
  const handlerRef = useRef(null);

  // In a real implementation, this would run before layout effects
  useLayoutEffect(() => {
    handlerRef.current = handler;
  });

  return useCallback((...args) => {
    // In a real implementation, this would throw if called during render
    const fn = handlerRef.current;
    return fn(...args);
  }, []);
}
```

In other words, it gives you a stable function that calls the latest version of the function you passed.

The built-in `useEvent` would have a few differences from the userland implementation above.

Event handlers wrapped in `useEvent` will **throw if called during render**. (Calling it from an effect or at any other time is fine.) So it is enforced that during rendering these functions are treated as opaque and never called. This makes it safe to preserve their identity despite the changing props/state inside. Because they can't be called during rendering, they can't affect the rendering output — and so they don't need to change when their inputs change (i.e. they're not "reactive").

The "current" version of the handler is switched before all the layout effects run. This avoids the pitfall present in the userland versions where one component's effect can observe the previous version of another component's state. The exact timing of the switch is an open question though (listed with other open questions at the bottom).

As an optimization, when server rendering, `useEvent` will return the same throwing shim for all calls. This is safe because events don't exist on the server. This optimization allows frameworks that bundle code for SSR to strip out event handlers (and their dependencies) from the SSR bundles, potentially improving SSR performance. (Note that this means that comparisons like `fn1 === fn2` would not allow to reliably distinguish two different event handlers.)

## Linter plugin

The dependency linter will treat the `useEvent` return values in scope as “stable”, so they are optional in the dependency list. (Similar to how `setState` functions are treated today.) The `useEvent` functions passed from parent components would have to be declared as dependencies. When you use a plain function from inside an effect, the linter “suggestions” would generate a `useEvent` rather than `useCallback` wrapper if the function’s name starts with `on` or `handle`.

In the future, it might make sense for the linter to warn if you have `handle*` or `on*` functions in the effect dependencies. The solution would be to wrap them into `useEvent` in the same component. This lets you be sure that the event handler won’t cause the effect to re-fire (because its identity is always stable) and makes it unnecessary in the dependency list.

## Static typechecking

The simplest way to type this is that `useEvent` takes a function and returns a function with the same shape. However, there may be opportunities to add new restrictions at the type system level around `useEvent` that would pave the way for statically checking against mistakes like using DOM manipulation during render. We plan to explore this in a future RFC.

## When `useEvent` should not be used

### Functions called during render still use `useCallback`

Some functions need to be memoized but are used during rendering. `useCallback` works for these cases:

```js
function ThemedGrid() {
  const theme = useContext(ThemeContext);
  const renderItem = useCallback(
    (item) => {
      // Called during rendering, so it's not an event.
      return <Row {...item} theme={theme} />;
    },
    [theme]
  );
  return <Grid renderItem={renderItem} />;
}
```

Since `useEvent` functions throw if called during render, this isn't much of a pitfall.

### Not all functions in effect dependencies are events

In the example below, `createSocket` accepts a `createKeys` function that is passed via context:

```js
function Chat({ selectedRoom }) {
  const { createKeys } = useContext(EncryptionSettings);
  // ...
  useEffect(() => {
    const socket = createSocket('/chat/' + selectedRoom, createKeys());
    // ...
    socket.connect();
    return () => socket.disconnect();
  }, [selectedRoom, createKeys]); // ✅ Re-runs when room or createKeys changes
}
```

Here, `createKeys` is not an event, so it should be specified in the effect dependencies. This ensures that if the user changes the encryption settings while in the chat, and a different function is passed as `createKeys`, it will cause the API to reconnect.

### Not all functions extracted from effects are events

Here is an example where a piece of code is incorrectly marked as an event:

```js
function Chat({ selectedRoom, theme }) {
  // ...
  // 🔴 This should not be an event!
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

This code is broken: since the effect no longer depends on `selectedRoom`, changing the room won’t recreate the socket. The mistake was in classifying `createSocket` as an event.

As a rule of thumb, it helps to think of events as things that objectively happened at a particular moment (“user visited a page”, “connected to a room”, “received a message”) regardless of how we structure the code. If the function name starts with `on` or `handle`, it’s probably an event. Conversely, events shouldn’t need to have cleanup code (because they represent discrete moments in time).

# 缺点

- This adds a new concept to React. People are already struggling with the best practices around defining functions ("should I use `useCallback` everywhere?") and this adds another layer to it.
  - This is the biggest issue. However, we think this concept is unavoidable in the practical usage of React so it benefits from a first-class API, a shared vocabulary, and a set of best practices. Between [#14099](https://github.com/facebook/react/issues/14099) and [#16956](https://github.com/facebook/react/issues/16956), the problem with `useCallback` invalidation is one of the top upvoted issues, is in our FAQ, and is one of the earliest patterns we needed to [write about](https://overreacted.io/making-setinterval-declarative-with-react-hooks/) after introducing Hooks. Even in the world where [memoization is done by a compiler](https://www.youtube.com/watch?v=lGEMwh32soc), we have to distinguish between optimizations and semantic guarantees about re-firing. We suspect that `useEvent` is a fundamental missing piece in the Hooks programming model and that it will provide the correct way to fix overfiring effects without error-prone hacks like skipping dependencies.
- Compared to a plain event handler, wrapping with `useEvent` looks more noisy.
  - However, it makes more sense to compare it with `useCallback` which people use today to solve the same problems. Many (likely the majority) of `useCallback` wrappers are used for functions that are never called during render, so they can be replaced with `useEvent`. Compared to them, `useEvent` is an ergonomic improvement (no dependency list and no invalidation). And it is optional, so if you prefer you can keep the code as is.
- `useEvent` makes the "event handler" term broader than just the DOM event handlers.
  - It could be called something like `useStableCallback` or `useCommittedCallback`. However, the whole point is to encourage using it for event handlers. Having a short name helps, and "is this an event handler?" is a good rule of thumb for the majority of cases when you want to use it. Even in effects, the cases where you'd want to extract a part of logic into an event corresponds to when you want to express "something happened!" (e.g. the user visited a page, and you want to log that). Conceptually, these "events" are similar to Events in Functional Reactive Programming. But most importantly, it is already common in React to refer to any `on*` callback prop as an "event handler", regardless of whether it corresponds to any actual DOM event (e.g. `onIntersect`, `onFetchComplete`, `onAddTodo`). `useEvent` is exactly the same concept.
- Compared to `useCallback`, the implementation of `useEvent` adds extra work to the commit phase.
  - However, in practice this pattern is already widespread. Having a built-in way to do this and a set of best practices seems better overall than ad-hoc solutions that exist in many libraries and products but suffer from timing flaws.
- There are a few edge cases. However, we think they’re not dealbreakers.
  - Unmounting layout effects will observe the previous version of the event callback but unmounting non-layout effects will run after the switch, so they will observe the next version. This is similar to how reading a ref during unmounting layout and non-layout effects produces different results.
  - The values in the event handler correspond to the values at the time it was called. This means that you don’t get truly “live” bindings. For example, if you have `async`/`await` inside an event and you read some prop after the `await`, the value will be the same as before the `await`. To get a “fresh” value again, you would need to step into another event. For this reason, events should usually not be asynchronous. It’s best to treat them as fire-and-forget: “here’s what just happened”
  - The “conditional event” case like `onSomething={cond ? handler1 : handler2}`. In this case, if you use `onSomething` as an effect dependency, it would re-fire when `cond` changes. You can “protect” against it by moving the `useEvent` wrapping to the same component as the effect that calls `onSomething`. We may consider adding more runtime or linter warnings if this case ends up common.

# 备选方案

- Status quo: `useCallback` invalidates too often and there's no built-in solution. Also, no built-in solution to overfiring effects. We think this is ergonomically untenable and that a solution is needed.
- Call `useEvent` something different. For example, `useStableCallback`. We think this makes it more difficult to tell when to use it. Longer or more complex name also makes it less ergonomic.
- Give the `useEvent` behavior to `useCallback`. We don’t want to do this because they have sufficiently different semantics.
- Force React event handlers to always be declared with `useEvent`. This seems premature at this point.
- Add an API to read the "latest" versions of arbitrary values instead. We find that this gets noisy in practice since a block of code often needs to read multiple values. Marking entire blocks of code (functions) instead of individual values is more convenient as the amount of code grows, and solves the same problem in a more generic way.
- Add some special API to `useEffect` instead. We think this is not broad enough because the problem with memoizing event handlers is the same, and so a shared solution is better.
- Same proposal, but allow calling event handlers during rendering. We think this creates too many footguns.
- Same proposal, but different timing of when the "current" version is switched up. This is an open question.
- Same proposal, but different linter behavior or runtime warnings. E.g. warn at runtime if an event is passed a dependency to an effect, and then lint to exclude events from dependencies altogether.

# 采用的策略

Release it in a minor. Change the dependency linter suggestions to wrap functions starting with `on*` or `handle*` into `useEvent` instead of the linter's current `useCallback` suggestion. Write new documentation teaching common patterns.

`useCallback` remains useful for cases where a function is used while rendering. However, it'll probably be deemphasized with time as it won't be needed as often.

A high-fidelty polyfill for `useEvent` is not possible because there is no lifecycle or Hook in React that we can use to switch `.current` at the right timing. Although [`use-event-callback`](https://github.com/Volune/use-event-callback) is “close enough” for many cases, it doesn't throw during rendering, and the timing isn’t quite right. We don’t recommend to broadly adopt this pattern until there is a version of React that includes a built-in `useEvent` implementation.

# 我们怎么讲授它

It's easy to teach how to wrap a function in it. Teaching how to solve problems with it is a bit harder.

We might be able to introduce `useEvent` earlier in the documentation than `useEffect` or `memo` because you don't need to understand referential identity or dependency arrays to use it. Then, when you get to `useEffect` and `memo`, the solution to their pitfalls (breaking memoization, re-firing effects) is based on an API you already know how to use.

# 还未解决的问题

- The exact timing of when the "current" function switches.
- Whether it makes sense for unmounting layout effects to "see" event handlers with the old value.
- Whether it makes sense for unmounting non-layout effects to "see" event handlers with the old value.
- Whether calling event handlers from an effect cleanup function is an anti-pattern and whether it should warn.
- How exactly to change the linter suggestions.
- Whether figuring out the full typing story in the follow-up RFC is a blocker for this one.
