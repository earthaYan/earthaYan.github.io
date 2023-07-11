---
title: 翻译-CSS vs. CSS-in-JS：How and why to use each
date: 2023-03-07 14:09:26
tags: [CSS]
categories: 翻译
---

原文地址：https://blog.logrocket.com/css-vs-css-in-js/
https://blog.logrocket.com/how-style-react-router-links-styled-components/
当使用 javascript 框架写代码的时候，开发者经常会面临一个困境：是否需要使用 CSS-in-JS。如果你使用 React 进行开发，可能你之前就使用过 CSS-in-JS。

CSS vs CSS-in-JS 是当下的热门话题。这主要是因为 CSS-in-JS 正在因为性能问题而备受关注。但是在[这个方向上(pipline 翻译不确定)](https://web.dev/state-of-css-2022/)也有一些新的 CSS 特性,他们应该会在不久的未来解决一部分问题。

这篇文章的目的是结合现代 CSS 的当前状态以及将来可能如何变化帮助你在接下来的项目中就 CSS 和 CSS-in-JS 中做出选择。

这篇文章展示的代码片段和 demo 都是使用 React 和 CSS 编写的。所以在进行下一步之前需要确保你对这两种 web 技术都非常熟悉。

注意任意的 JavaScript 前端框架或者库都可以是实现 CSS-in-JS 的理念。本文使用目前为止最流行的前端库——React 来讨论 CSS-in-JS 的应用以及它显著的利弊。

## Render-blocking 和 CSS

在进一步讨论什么是最好的,什么不是最好的之前,我们先讨论因为 CSS 导致的一些渲染问题。

传统 web 技术中,浏览器首先会加载 HTML,然后加载来自所有外部资源的 CSS。那之后,浏览器使用所有的内外部 CSS 信息创建 CSSOM。此时浏览器已准备好通过 CSS 级联规则向已经渲染的 HTML 提供样式。

这个进程会导致 CSS [阻止页面渲染](https://blog.logrocket.com/9-tricks-eliminate-render-blocking-resources/)，并延迟所请求页面的首绘。首绘指的是浏览器在屏幕上打印所请求页面的第一个像素时的事件。

首绘中超过半秒的延迟就会造成用户不满意的风险，并且可以对 app 的评分造成负面影响。越快把 CSS 传递到客户端，就可以越好地优化页面的首绘时间。

### 战胜 CSS render-block

基于 HTTP/2 的应用程序,可以并行加载多个 HTML, CSS 和 JS 文件。HTTP/1.1 不具备这种功能。大部分现代浏览器和网站都已经支持 HTTP/2,这最大程度地减少了由等待其他文件加载引起的渲染阻塞。

{% asset_img img1-Graphic-showing-difference-file-loading-HTTP1-HTTP2.avif %}

但是渲染阻塞除了文件加载速度还有其他原因。

我们假设 app 的一个页面有许多 CSS。这个页面可能包含了很多存在但是没有被使用的选择器，因为我们在每个页面都导入了一个主 CSS 文件。

上面这个场景基本描述了我们是如何习惯直接使用我们创建的 [CSS UI 框架或者 UI 工具箱](https://blog.logrocket.com/comparing-tailwind-css-bootstrap-time-ditch-ui-kits/)来快速促进我们的设计系统。并非所有从框架或者工具箱引用的样式都会在每个页面内被使用。结果就是我们最终为这个页面生成的 CSS 样式里出现了更多的垃圾。

CSS 越多,浏览器构建 CSSOM 的时间越长，这会导致完全没有必要的渲染阻塞。

为了遏制这种局面,把 CSS 分割成小代码块非常有用。换句话说,把全局样式和必要的 CSS 保存在一个全局文件中，然后将其他内容组件化。这种策略更有意义且解决了不必要的非必要 CSS 阻塞：

{%asset_img img2-Project-structure-componentized-CSS.avif%}

上面这张图展示了在 React 中为各个组件创建和管理局部 CSS 文件的传统方式。因为每个 CSS 文件是直接附加在各自的组件上,所以它只在相关组件被导入的时候被导入，在组件被移除的的时候消失。

目前，这个方法还有不足之处。假设 app 包含 100 个组件，同一个项目中的其他开发者可能在这些 CSS 文件中已经不小心使用了一样的类名。

在这里,每个组件的每个 CSS 文件的范围都是全局的，所以这些不小心重复的样式会不断相互覆盖并被全局应用。像这样的场景会引起严重的布局和设计不一致。

据说 CSS-in-JS 可以解决这个作用域问题。接下来的文章在高层次上回顾了 CSS-in-JS，并讨论了它是否一劳永逸地有效地解决了作用域问题。

## CSS-in-JS 提供了什么

CSS-in-JS 简单来说就是外部功能层，它可以让你通过 JavaScript 为组件编写 CSS 属性。

这一切起源于 2015 年一个叫做 [JSS](https://cssinjs.org/?v=v10.10.0) 的库，当然这个库现在仍然处于活跃的维护状态。你必须使用 JavaScript 语法给选择器提供 CSS 属性，一旦页面加载后就会自动把这些属性应用到他们各自的选择器。

当 JavaScript 使用类似 React 的库接管渲染和管理前端的时候，一个叫做 [styled-components](https://blog.logrocket.com/how-style-react-router-links-styled-components/) 的 CSS-in-JS 解决方案出现了。另外一个快速流行的解决方案是使用 Emotion 库做同样的事。

我们打算用 styled-components 库演示 CSS-in-JS 的示例用例，因为他是在 React 生态中使用 CSS-in-JS 方案中最流行的。

### 通过 styled-components 使用 CSS-in-JS 的例子

在 React app 中使用下面的 Yarn 命令安装 styled-components 库。如果你使用的是不同的包管理器,可以查看 styled-components 安装文档找到合适的安装命令：

```bash
yarn add styled-components
```

安装完 styled-components 库之后,导入 styled 函数，按如下代码使用：

```jsx
import styled from "styled-components";

const StyledButton = styled.a`
  padding: 0.75em 1em;
  background-color: ${({ primary }) => (primary ? "#07c" : "#333")};
  color: white;

  &:hover {
    background-color: #111;
  }
`;

export default StyledButton;
```

如果你没有 React 环境，[这里](https://codepen.io/_rahul/pen/oNywWXR)有一个运行上述代码的链接：

上面的代码演示了如何在 React 中给一个 button-link 组件添加样式。添加完样式的组件现在可以不用担心样式问题在任意地方被导入并被直接用来构建一个功能组件：

```bash
import StyledButton from './components/styles/Button.styled';

function App() {
  return (
    <div className="App">
      ...
      <StyledButton href="...">Default Call-to-action</StyledButton>
      <StyledButton primary href="...">Primary Call-to-action</StyledButton>
    </div>
  );
}
export default App;
```

注意：应用到 styled 组件上的样式是局部范围的,这消除了需要留心 CSS 类命名和全局范围的繁琐需求。除此之外，我们可以基于提供给组件的 props 或者 app 功能所需的任何其他逻辑动态添加或移除 CSS。

## CSS-in-JS 的好处

比起 CSS 类,JavaScript 开发者可能更喜欢使用 CSS-in-JS 来写样式。CSS-in-JS 解决的最大问题是全局作用域。如果你是 JavaScript 开发者的话，它其他的一些优势也非常有意义。

现在让我们开始探索这些优势中的一部分。

### 没有作用域和特异性问题

由于样式只能在局部范围内使用，所以他们不容易和其他组件的样式冲突。你甚至不需要担心使用严格的命名来避免样式冲突。

专门为一个组件写的样式不需要预先考虑子选择器，所以特异性问题很少。

### 动态样式

条件 CSS 是 CSS-in-JS 的另外一个高光点。如同上面演示的按钮示例一样，比起为每个变动写一个单独的样式，检查 props 值并且添加合适的样式是更酷的一种方法。

### 更少的 CSS 特异性

CSS-in-JS 帮助你把 CSS 声明的特异性保持在最低水平，因为你唯一使用它的样式的途径就是元素本身。这同样适用于创建组件变体，你可以检查 prop 对象值并且在需要的时候添加动态样式。

### 容易的主题

使用自定义 CSS 属性为 app 设置主题非常有意义。在最后，你必须转到 JavaScript 侧，基于用户输入写一些逻辑代码来切换和记住主题。

CSS-in-JS 让你可以完全使用 JavaScript 编写主题逻辑。借助 styled-components 的 ThemeProvider wrapper，你可以快速为组件的主题进行颜色编码。下面借[这个案例](https://codepen.io/_rahul/pen/qBKXevo)来查看使用 styled-components 定制主题：

### 无痛维护

考虑到 CSS-in-JS 提供的特性和优势，JavaScript 可能会发现 CSS-in-JS 比管理上百个 CSS 文件更方便。

但是有一个遗留事实是：只有对 JavaScript 和 CSS 都有很深的理解,才能高效管理和维护由 CSS-in-JS 驱动的大型项。

## CSS-in-JS 的坏处

CSS-in-JS 确实非常完美的解决了作用域问题。但是就像我们一开始讨论的那样，我们会面临更大的挑战——比如渲染阻塞——这会直接影响用户体验。除此之外，CSS-in-JS 的概念还需要处理一些其他的问题。

### 延迟渲染

CSS-in-JS 会执行 JavaScript 来从 JavaScript 组件中解析 CSS,然后把这些转换出来的样式注入 DOM。组件越多，浏览器首绘的时间就越长。

### 缓存问题

CSS 缓存经常被用来改善连续页面加载时间。当使用 CSS-in-JS 的时候由于没有 CSS 文件,缓存变成了一个大问题。而且。动态生成 CSS 类名让这个问题变得更复杂。

### CSS 预处理器支持度

借助组件化的 CSS 方法,很容易添加像[SASS](https://blog.logrocket.com/how-to-write-reusable-css-with-sass/), Less, PostCSS 和其他的预处理的支持。而在 CSS-in-JS 中，这是不可能的。

### 凌乱的 DOM

CSS-in-JS 的基础是将所有的样式定义从 JavaScript 解析为基础 CSS，然后使用样式块将样式注入 DOM 中。

对于每个使用 CSS-in-JS 进行样式编写的组件来说,可能首先就会有 100 个样式块需要解析然后注入。简单来说就是会有更多的间接成本。

### 库依赖

如同我们所知道的那样，我们可以使用外部库添加 CSS-in-JS 功能。许多 JavaScript 将在实际的 CSS 解析之前被包含并运行，因为从 JavaScript 到 CSS 样式的解析取决于像 styled-components 这样的库。

### 学习曲线

CSS-in-JS 缺失很多 CSS 和 SCSS 与生俱来的特性。对于已经习惯了 CSS 和 SCSS 的开发者来说适应 CSS-in-JS 将会非常有挑战性

### 没有大规模的支持

目前大部分 UI 库和组件库都不支持 CSS-in-JS 方式，因为它仍然有许多问题需要解决

上面讨论的问题可能会累积在一起，导致产品性能低、难以维护，并存在若干 UI 和 用户体验不一致的问题。

## 什么情况下推荐使用 CSS-in-JS

当你处理一个较小的应用并且性能优先级要求不高的话， CSS-in-JS 是一个理想的解决方案。在处理具有庞大设计系统的性能要求高的应用时，它可能并不理想。

随着 app 逐渐变大，考虑到这个概念的所有缺点，使用 CSS-in-JS 会很容易变得复杂，把一个设计系统转化为 CSS-in-JS 有许多工作要做，从我的角度来看，没有 JavaScript 开发者会想要处理这种情况。

## CSS Module 概览

[CSS Module](https://blog.logrocket.com/a-deep-dive-into-css-modules/)是一个 CSS 文件，里面所有的属性在已经渲染的 CSS 中默认都被限制在局部范围内。JavaScript 进一步处理 CSS Module 文件并且封装他们的样式声明来解决作用域问题。

为了使用 CSS Module，你需要把 CSS 文件扩展名修改为`.module.css`,然后将他们导入 JavaScript 文件中。下面的代码片段提供了一个如何使用 CSS Module 的例子：

```jsx
import styles from "./Button.module.css";

export default function Button(props) {
  return (
    <a href={props.href ? props.href : "#"} className={styles.btn}>
      {props.name}
    </a>
  );
}
```

看这个在 React 中实现 CSS Module 的[示例](https://stackblitz.com/edit/react-hbivvp?file=src%2Fcomponents%2FAnotherButton%2FAnotherButton.jsx)。这个例子展示了如何使用 CSS Module 修复作用域问题。

在这个例子里,请注意如何智能地处理和优化 Button.module.css 和 AnotherButton.module.css 的相同类名来防止命名冲突。

## CSS Module 的好处

CSS Module 提供的最大的好处就是摆脱对 CSS in-JS 的依赖解决范围和特异性问题。如果我们可以通过保持尽可能传统 CSS 来解决作用域和特异性问题，那么 CSS-in-JS 的工作量会比必要的工作量大。

### 没有作用域和特异性问题

就像上面演示的示例一样，CSS Module 成功解决了我们遇到的传统旧式的 CSS 作用域问题。。由于规则是松散地编写在 CSS 模块文档中的，因此很少观察到任何特异性问题。

### 有组织的代码

保留各自单独的 CSS 文件似乎是一个限制。但是这个方法确实促进了更好的组织组件。举例来说，这就是我如何通过把他们分到各自的文件夹下来组织组件：

```bash
- Project
  - src
    - components
      - Button
          - Button.jsx
          - Button.modules.css
      - Carousel
          - Carousel.jsx
          - Carousel.modules.css
```

### 缓存的可能

最终构建生成的极简化的 CSS 文件可以被浏览器缓存，从而改善连续页面加载时间。

### CSS 预处理

添加对 CSS 预处理器（如 PostCSS，SASS，Less 等）的支持很容易。但是必须依赖额外的包来做这个事情。

### 零学习曲线

If you know how CSS works, you can use CSS Module without learning anything new besides the few points that we discussed above in the intro segment.
如果你知道 CSS 是怎么工作的就能使用 CSS Module，除了上面介绍部分讨论的几点外你几乎不用学习任何新的东西。

### 强大的支持

你不需要添加任何额外的包就能使用 CSS Module。所有的主流框架和库都提供了内置的支持。

## CSS Module 的坏处

尽管 CSS Modue 提供了许多好处，但是他还不是一个完美的解决方案。以下是一些需要牢记的注意事项。

### 非标准的 `:global` 属性

当在全局作用域内定位选择器的时候，你必须使用`:global`规则。这不是 CSS 规范的一部分，但是被 JavaScript 用它来标记全局样式。

### 没有动态样式

借助 CSS Module，所有的声明都会进入单独的 CSS 文件。因此不可能像 CSS-in-JS 一样实现动态样式，因为我们不能在 CSS 文件中实现任何 JavaScript。

### 外部的 CSS 文件

你不能省略组件中带有 CSS 模块的 CSS 文件的用法。使用 CSS 模块的唯一可能方法是维护和导入外部 CSS 文档。

### TypeScript 限制

为了在 TypeScript 下使用 CSS Module,你必须在`index.d.ts`中添加 module 定义或者使用[webpack loader](https://blog.logrocket.com/how-to-configure-css-modules-webpack/)：

```typescript
/** index.d.ts **/
declare module "*.module.css"; // TS module for CSS Module files
declare module "*.module.scss"; // TS module for CSS Module files in SCSS format
```

## 推荐使用 CSS Module 的场景

如果你应用 UI 规模大并且对性能要求严苛，CSS Module 是一个非常好的选择。由于 CSS Module 提供的每个东西最终都是基于传统的,非实验性的用法，所以这个方法让监控和修复性能变得更容易。
CSS Module 文件非常容易适应你选择的任意 CSS 框架的代码，因为你需要处理的只有 CSS。就像前面说的，基础的 CSS 对于这个任务来说已经足够了。

## 现代 CSS 特性

在介绍里，我提到了一些现代化的 CSS 特性在未来不需要依赖 CSS Module，CSS-in-JS 或者其他的一些 JavaScript 解决方案的情况下是如何协助解决作用域问题的。

新的并且正在计划中的特性——例如作用域指令和@scope 伪元素——旨在使用传统的 CSS 解决老问题。反之，这也会减少开发者转向类似 CSS-in-JS 作为这些缺陷的变通方法的需求

让我们看一下目前的 scoped CSS 草案是如何解决 CSS-in-JS 甚至 CSS Module 的问题。对于其他的 CSS 属性的完整列表，查看[the State of CSS 2022](https://web.dev/state-of-css-2022/)

### CSS 作用域的潜在可能性

在从 CSS 规范中奇怪的引入和移除<style scope>之后，当前的 Scope CSS 草案看上去已经足够优秀到去通过编写 CSS 规则来定义元素的作用域前提。
Its current status involves using a directive and a pseudo-class to control the provision of scoping for a given element. Here is a rough picture of how it will lock an element’s scope within a boundary and maintain it regardless of the cascade’s rules of scoping:
目前的状态涉及了使用指令和伪类来控制一个给定的元素的作用域。这里是一个如何将元素的作用域锁定在边界内并维护它的粗略图片，而不管级联的作用域规则如何：

```html
<div class="card">
  <img src="..." />
  <div class="content">
    <p>...</p>
  </div>
  <!-- .content -->
</div>
<!-- .card -->

<style>
  @scope (.card) {
    :scope {
      display: grid;
      ...;
    }
    img {
      object-fit: cover;
      ...;
    }
    .content {
      ...;
    }
  }
</style>
```

这个新特性也许会消除对于 CSS Module 或者 CSS-in-JS 解决作用域问题的需求。我们拭目以待，等它在我们的浏览器中可以使用的那一天。

## 总结

以上，我们首先提到了对于web应用来说，CSS 渲染阻塞是一个主要的性能问题。然后讨论了修复这些问题的部分解决方案，这促使我们探索 CSS-in-JS、CSS Module以及新作用域 CSS 功能的官方进度草案的当前状态。

开发者喜欢JavaScript，爱CSS-in-JS是因为它用JavaScript覆盖了几乎所有的样式角度。另一方面，这些喜欢CSS的——并且想让当前的技术能支持开发者和终端用户同样也许会更喜欢CSS Module。
