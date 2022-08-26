---
title: ssr-2
urlname: pxpg8p
date: '2022-04-06 14:06:16 +0800'
tags: [工作]
categories: [工作]
---

SSR（`Server Side Rendering`）:服务端渲染，将渲染的工作放在服务端进行
CSR（`Client Side Rendering`）:客户端渲染，常见的应用形态有 SPA(单页面应用)
![1649306205(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649306215469-a6bc399a-926c-4654-925c-e172becefc9b.png#clientId=ua62afdcd-1b9c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=232&id=u3448b19a&margin=%5Bobject%20Object%5D&name=1649306205%281%29.png&originHeight=791&originWidth=697&originalType=binary∶=1&rotation=0&showTitle=false&size=168757&status=done&style=none&taskId=ud0ce4a7c-f56a-4483-8ab2-a318f046be3&title=&width=204.28704833984375)![1649306324(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649306330293-68ddb23f-6090-423c-9c9f-4a0d60feb5b6.png#clientId=ua62afdcd-1b9c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=177&id=uc2fa3351&margin=%5Bobject%20Object%5D&name=1649306324%281%29.png&originHeight=922&originWidth=1875&originalType=binary∶=1&rotation=0&showTitle=true&size=452442&status=done&style=none&taskId=u4ef02f20-1b0c-47d4-9c61-6e4ce289ef1&title=SSR&width=359.97222900390625 "SSR")
![1649225457(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649225465942-fa41d865-d42a-4791-acfc-d95ed7039b4a.png#clientId=u40d9040d-a82e-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=161&id=u6bbbd39a&margin=%5Bobject%20Object%5D&name=1649225457%281%29.png&originHeight=282&originWidth=701&originalType=binary∶=1&rotation=0&showTitle=false&size=12273&status=done&style=none&taskId=uab9f48fd-a44b-41b8-8278-f2a269b1c4b&title=&width=400.317138671875)![1649225408(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649225416106-3ef9f0d3-2725-4a3a-b350-249f313758a1.png#clientId=u40d9040d-a82e-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=170&id=ub6fff946&margin=%5Bobject%20Object%5D&name=1649225408%281%29.png&originHeight=958&originWidth=1841&originalType=binary∶=1&rotation=0&showTitle=true&size=153012&status=done&style=none&taskId=u75ced11f-6d9a-4c92-a56e-8c7a24caffd&title=CSR&width=326 "CSR")

很明显，CSR 的首页内容是由下面的 script 中拉取的 JS 代码控制的。CSR 和 SSR 最大的区别是：CSR 的页面渲染是由 JS 负责进行，而 SSR 是由服务器端直接返回 HTML 让浏览器直接渲染

![](https://cdn.nlark.com/yuque/0/2022/jpeg/115484/1649227809779-ce603989-3bbf-440e-a2ac-3280d244301f.jpeg)
![image.png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649308249685-f0d5632e-4b94-4977-a740-1871f6f64fc3.png#clientId=u0dff0637-de54-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=K4HkR&margin=%5Bobject%20Object%5D&name=image.png&originHeight=431&originWidth=824&originalType=url∶=1&rotation=0&showTitle=true&size=182132&status=done&style=none&taskId=uc4fd520c-457a-4208-89ef-2a0b04f91d0&title=%E6%A9%99%E8%89%B2%E9%83%A8%E5%88%86%E4%B8%BA%E9%A1%B5%E9%9D%A2%E8%83%8C%E6%99%AF%E8%89%B2%EF%BC%8C%E5%AF%B9%E5%BA%94%E4%BA%86%E5%B8%B8%E8%A7%84%E6%84%8F%E4%B9%89%E4%B8%8A%E7%9A%84%E7%99%BD%E5%B1%8F%E6%97%B6%E9%97%B4 "橙色部分为页面背景色，对应了常规意义上的白屏时间")

### CSR（SPA）的优点：

1. 只有一开始进入或者刷新的时候才会请求服务器，只需加载一次 js css 资源
1. 页面的路由维护在客户端，页面间的跳转就是切换相关的组件所以切换速度很快，用户体验流畅
1. 数据渲染都在客户端完成，服务器只需要提供一个返回数据的接口,降低了服务器的压力。

### CSR 的缺点：

1. SPA 应用第一次打开页面获取到的是一个空白的 html 文档，数据的渲染需要等待页面 js、css 资源加载完成,且执行时再发起异步数据请求，然后等数据返回后，再进行渲染，渲染完成后用户才能看到最终的页面，导致首屏（首屏 ≠ 首页）加载时间会比较慢
1. 对于 SEO 不友好，搜索引擎爬虫只能识别 html 的内容，而 CSR 返回的是一个早已准备好的空白文档

### SSR 的优势：

1. 直接是由服务器端直接返回 HTML,这个内容基本是已经可以呈现的界面，首屏时间大大缩短
1. 对于站点访问请求响应的是填充过的页面，信息和数据可供爬虫识别，有利于 SEO

### SSR 的缺点：

1. 所有页面的加载都需要向服务器请求完整的页面内容和资源，当产品逐渐复杂以后，可能有几十个甚至上百个页面，此时会增加服务器的压力
1. 页面之间频繁刷新跳转，用户体验较差

疑问：单纯的 SSR 或者 SPA 好像都不完美，所以如果结合 SPA 和 SSR，会不会更好一点呢？
主要问题:

- SEO 问题
- 首次白屏等待时间长

方法：第一次打开页面的时候使用服务端渲染，用户后续的交互使用 SPA，这样可以在用户体验流畅的同时，也解决了上面的两个问题（比如 next.js）。

### 实现一个简单的 react ssr

#### react 能够实现 SPA+SSR 的原理：

虚拟 DOM:可以在服务端渲染组件的根本原因,平时写组件用的 jsx 本质上是一个语法糖，他最终会被转换为一个普通对象[https://github.com/facebook/react/blob/main/packages/react/src/ReactElement.js](https://github.com/facebook/react/blob/main/packages/react/src/ReactElement.js)

```javascript
//编译前
<ul id="list">
  <li class="child">item1</li>
  <li class="child">item2</li>
  <li class="child">item3</li>
</ul>;

//编译后
("use strict");

/*#__PURE__*/
React.createElement(
  "ul",
  {
    id: "list",
  },
  /*#__PURE__*/ React.createElement(
    "li",
    {
      class: "child",
    },
    "item1"
  ),
  /*#__PURE__*/ React.createElement(
    "li",
    {
      class: "child",
    },
    "item2"
  ),
  /*#__PURE__*/ React.createElement(
    "li",
    {
      class: "child",
    },
    "item3"
  )
);
```

```javascript
//类型定义
function createElement<P extends {}>(
    type: FunctionComponent<P> | ComponentClass<P> | string,
    props?: Attributes & P | null,
    ...children: ReactNode[]): ReactElement<P>;
//源码实现
export function createElement(type, config, children) {
  let propName;
  // Reserved names are extracted
  const props = {};

  let key = null;
  let ref = null;
  let self = null;
  let source = null;

  if (config != null) {
    if (hasValidRef(config)) {
      ref = config.ref;

      if (__DEV__) {
        warnIfStringRefCannotBeAutoConverted(config);
      }
    }
    if (hasValidKey(config)) {
      if (__DEV__) {
        checkKeyStringCoercion(config.key);
      }
      key = '' + config.key;
    }

    self = config.__self === undefined ? null : config.__self;
    source = config.__source === undefined ? null : config.__source;
    // Remaining properties are added to a new props object
    for (propName in config) {
      if (
        hasOwnProperty.call(config, propName) &&
        !RESERVED_PROPS.hasOwnProperty(propName)
      ) {
        props[propName] = config[propName];
      }
    }
  }

  // Children can be more than one argument, and those are transferred onto
  // the newly allocated props object.
  const childrenLength = arguments.length - 2;
  if (childrenLength === 1) {
    props.children = children;
  } else if (childrenLength > 1) {
    const childArray = Array(childrenLength);
    for (let i = 0; i < childrenLength; i++) {
      childArray[i] = arguments[i + 2];
    }
    //....
    props.children = childArray;
  }
//...代码省略
  return ReactElement(
    type,
    key,
    ref,
    self,
    source,
    ReactCurrentOwner.current,
    props,
  );
}

//类型定义
interface ReactElement<P = any, T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>> {
        type: T;
        props: P;
        key: Key | null;
    }
//源码实现
const ReactElement = function(type, key, ref, self, source, owner, props) {
  const element = {
    // This tag allows us to uniquely identify this as a React Element
    $$typeof: REACT_ELEMENT_TYPE,
    // Built-in properties that belong on the element
    type: type,
    key: key,
    ref: ref,
    props: props,
    // Record the component responsible for creating this element.
    _owner: owner,
  };
  //.....
  return element;
};


```

我们可以把这个对象转换为我们需要的形式，比如 html 格式，这个 html 就是服务端返回给用户的响应页面。关于转换 react 内部也提供了相关的 api

- `renderToString(element)`
  - 作用：把一个 react 组件转换为原始的 html,只用于服务端，返回值为一个 html 字符串
  - 注意：如果在一个已经有这个服务器渲染标记的节点上调用客户端渲染 api——reactdom.hydrate()，客户端会采用服务端渲染的结果，只附加事件处理程序，提升初次加载体验
- `renderToStaticMarkup(element)`
  - 作用和 renderToString 类似
  - 注意：不会在 React 内部创建的额外 DOM 属性，可以用作静态页面生成器，去除额外的属性可以节省一些字节
- `renderToNodeStream(element）`
  - 作用：将一个 React 元素渲染成其初始 HTML。返回一个可输出 HTML 字符串的可读流
  - 注意：无论是 renderToString 还是 renderToNodeStream，最终的渲染结果都是一样的，但是后者的性能更好，可以缩短 TTFB 时间，让首屏更快显示
  - 原因：组件转换为字符串是一次性处理完之后才开始返回，组件转换为流，可以边读边输出
- `renderToStaticNodeStream(element)`
  - 区别同上

#### 实践：

[https://gitee.com/earthaYan/react_ssr](https://gitee.com/earthaYan/react_ssr)

### next.js:

#### 预渲染形式：

1. 静态生成 （推荐）：HTML 在 构建时生成，并在每次页面请求（request）时重用。
1. 服务器端渲染：在 每次页面请求（request）时 重新生成 HTML

#### 使用：

- 不带数据的静态页面：使用静态生成
- 静态生成：页面内容取决于外部数据
  - getStaticProps()只在服务端 build 时执行
- ![1649385626(1).png](https://cdn.nlark.com/yuque/0/2022/png/115484/1649385634236-c02dce49-0cf6-46e0-b544-e780898989f9.png#clientId=u2ded078c-23ec-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=521&id=u60500755&margin=%5Bobject%20Object%5D&name=1649385626%281%29.png&originHeight=782&originWidth=1116&originalType=binary∶=1&rotation=0&showTitle=false&size=186777&status=done&style=none&taskId=u29083750-8a7d-4d4b-abd7-16c67ef40fc&title=&width=744)
  - 在预渲染时将 getStaticProps()获取的数据作为 props 参数传递给页面
  - 在 dev 模式下, getStaticProps 会在每一次请求的时候被调用

```javascript
// posts will be populated at build time by getStaticProps()
function Blog({ posts }) {
  return (
    <ul>
      {posts.map((post) => (
        <li>{post.title}</li>
      ))}
    </ul>
  );
}

// This function gets called at build time on server-side.
// It won't be called on client-side, so you can even do
// direct database queries. See the "Technical details" section.
export async function getStaticProps() {
  // Call an external API endpoint to get posts.
  // You can use any data fetching library
  const res = await fetch("https://.../posts");
  const posts = await res.json();

  // By returning { props: { posts } }, the Blog component
  // will receive `posts` as a prop at build time
  return {
    props: {
      posts,
    },
  };
}

export default Blog;
```

- 静态生成：页面路径取决于外部数据

```javascript
function Post({ post }) {
  // Render post...
}

// 此函数在构建时被调用
export async function getStaticPaths() {
  // 调用外部 API 获取博文列表
  const res = await fetch("https://.../posts");
  const posts = await res.json();

  // 据博文列表生成所有需要预渲染的路径
  const paths = posts.map((post) => ({
    params: { id: post.id },
  }));

  // We'll pre-render only these paths at build time.
  // { fallback: false } means other routes should 404.
  return { paths, fallback: false };
}

// 在构建时也会被调用
export async function getStaticProps({ params }) {
  // params 包含此片博文的 `id` 信息。
  // 如果路由是 /posts/1，那么 params.id 就是 1
  const res = await fetch(`https://.../posts/${params.id}`);
  const post = await res.json();

  // 通过 props 参数向页面传递博文的数据
  return { props: { post } };
}

export default Post;
```

- 服务端渲染：getServerSideProps（context）
  - 只运行在服务端
  - 如果直接访问该页面，使用 props 的值预渲染该页面，直接返回 html 文档
  - 如果通过 next/link 等客户端方式访问该页面，next 会发送一个 api 请求给服务端，返回 getServerSideProps 的值的 json 数据渲染该页面
  - 使用时机：只有当需要预呈现一个必须在请求时获取数据的页面时，才应该使用 getServerSideProps

```javascript
function Page({ data }) {
  // Render data...
}

// This gets called on every request
export async function getServerSideProps() {
  // Fetch data from external API
  const res = await fetch(`https://.../data`);
  const data = await res.json();

  // Pass data to the page via props
  return { props: { data } };
}

export default Page;
```
