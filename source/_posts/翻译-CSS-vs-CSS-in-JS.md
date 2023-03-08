---
title: 翻译-CSS vs. CSS-in-JS：How and why to use each
date: 2023-03-07 14:09:26
tags: [CSS, 翻译]
categories: 翻译
---

原文地址：https://blog.logrocket.com/css-vs-css-in-js/

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

当 JavaScript 使用类似 React 的库接管渲染和管理前端的时候，一个叫做 styled-components 的 CSS-in-JS 解决方案出现了。另外一个快速流行的解决方案是使用 Emotion 库做同样的事。

我们打算用styled-components库演示CSS-in-JS的示例用例，因为他是在React生态中使用CSS-in-JS方案中最流行的。

### 通过styled-components使用 CSS-in-JS的例子
In your React app, install the styled-components library using the below Yarn command. If you are using a different package manager, see the styled-components installation docs to find the appropriate installation command:
在React app中
```bash
yarn add styled-components
```

After installing the styled-components library, import the styled function and use it as shown in the code below:

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

If you don’t have access to a React environment, here’s a [CodePen demo](https://codepen.io/_rahul/pen/oNywWXR) for you to see the above code in action:

The code above demonstrates how to style a button-link component in React. This styled component can now be imported anywhere and used directly to build a functional component without having to worry about the styles:

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

Note that the styles applied to the styled components are locally scoped, which eliminates the cumbersome need to be mindful of CSS class naming and the global scope. In addition, we can add or remove CSS dynamically based on the props supplied to our component or any other logic demanded by an app feature.

## Pros of CSS-in-JS

A JavaScript developer may prefer to style things with CSS-in-JS rather than going through CSS classes. The biggest problem the CSS-in-JS approach solves is the global scope. It also has some other advantages that make a lot of sense if you are a JavaScript developer.

Let’s explore some of these benefits now.

### No scoping and specificity problems

ince styles are available in a local scope, they are not prone to clashing with the styles of other components. You don’t even have to worry about naming things strictly to avoid style clashes.

Styles are written exclusively for one component without prepending child selectors, so specificity issues are rare.

### Dynamic styling

Conditional CSS is another highlight of CSS-in-JS. As the button example above demonstrates, checking for prop values and adding suitable styles is way cooler than writing separate CSS styles for each variation.

### Less CSS specificity

CSS-in-JS helps you keep the specificity of CSS declarations to the lowest, as the only thing you style with it is the element itself. The same applies to creating component variations, where you can check for prop object values and add dynamic styling when required.

### easy theming

Theming apps with custom CSS properties makes sense. In the end, you will have to move to the JavaScript side and write the logic to switch and remember the theme based on user input.

CSS-in-JS allows you to write theming logic entirely in JavaScript. With the styled-components ThemeProvider wrapper, you can quickly color-code themes for components. Take a look at this [CodePen](https://codepen.io/_rahul/pen/qBKXevo) example to see component theming with styled-components in action:

### Painless maintenance

Considering the features and advantages CSS-in-JS offers, a JavaScript developer may find CSS-in-JS more convenient than managing hundreds of CSS files.

The fact remains, however, that one must have a good understanding of both JavaScript and CSS to effectively manage and maintain huge projects powered by CSS-in-JS.

## Cons of CSS-in-JS

CSS-in-JS does solve the scoping problem very well. But as we discussed initially, we have much bigger challenges — like render-blocking — that directly affect the user experience. Along with that, there are some other issues that the concept of CSS-in-JS still has to address.

### Delayed rendering

CSS-in-JS will execute JavaScript to parse CSS from JavaScript components, and then inject these parsed styles into the DOM. The more components more will be the more time taken by the browser for the first paint.

### Caching problem

CSS caching is often used to improve successive page load times. Since no CSS files are involved when using CSS-in-JS, caching is a big problem. Also, dynamically generated CSS class names make this issue even more complicated.

### No CSS preprocessor support

With the regular componentized CSS approach, it’s easy to add support for preprocessors like SASS, Less, PostCSS, and others. The same is not possible with CSS-in-JS.

### Messy DOM

CSS-in-JS is based on the idea of parsing all style definitions from JavaScript into vanilla CSS and then injecting the styles into the DOM using style blocks.

For each component styled with CSS-in-JS, there could be 100 style blocks that must be parsed first, then injected. Simply put, there will be more overhead costs.

### Library dependency

As we already know, we can add CSS-in-JS functionality with an external library. A lot of JavaScript will be included and run before actual CSS parsing, as parsing styles from JavaScript to CSS styles depends on a library like styled-components.

### Learning curve

A lot of native CSS and SCSS features are missing with CSS-in-JS. It may be very challenging for developers who are used to CSS and SCSS to adapt to CSS-in-JS.

### No extensive support

Most of the UI and component libraries don’t support the CSS-in-JS approach right now, as it still has a lot of issues to address.

The problems discussed above may collectively contribute to a low-performant, hard-to-maintain product with several UI and UX inconsistencies.

## Recommendations for where to use CSS-in-JS

The CSS-in-JS solution is ideal when you are dealing with a smaller application for which performance is a lower priority. It may not be ideal when dealing with a performance-critical application with a huge design system.

As an app grows bigger, using CSS-in-JS can get complicated easily, considering all the drawbacks of this concept. A lot of work goes into converting a design system into CSS-in-JS, and in my opinion, no JavaScript developer would want to deal with that.

## Overview of CSS Module

A CSS Module is a CSS file in which all the properties are scoped locally by default in the rendered CSS. JavaScript processes the CSS Module files further and encapsulates their style declarations to solve the scoping issue.

To use CSS Module, you need to name your CSS files with a .module.css extension and then import them into JavaScript files. The below code snippet provides a basic example of how to use CSS Module:

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

Take a look at this StackBlitz example for implementing CSS Modules in React. This example shows how to use CSS Modules to fix the scoping problem.

In the StackBlitz example, notice how the same class names in Button.module.css and AnotherButton.module.css are processed and optimized intelligently to prevent naming conflicts.

## Pros of CSS Module

The most significant benefit that CSS Module offers is removing the reliance on CSS-in-JS to fix the scoping and specificity problems. If we can fix the scoping and specificity problems by keeping CSS as traditional as possible, CSS-in-JS will be more work than necessary.

### No scoping and specificity issues

As demonstrated in the example above, CSS Module successfully solves the scoping problem we have with traditional, old-style CSS. As the rules are loosely written in CSS Module files, it’s rare to observe any specificity problems.

### Organized code

Keeping separate CSS files may appear to be a limitation. However, this method actually promotes better organization. For example, here’s how I organize components by separating them into their own folders:

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

### Caching possibilities

The minified CSS files generated with the final build can be cached by the browser to improve the successive page load times.

### CSS preprocessing

It’s easy to add support for CSS preprocessors like PostCSS, SASS, Less, and others. However, you have to rely on additional packages to do so.

### Zero learning curve

If you know how CSS works, you can use CSS Module without learning anything new besides the few points that we discussed above in the intro segment.

### Great support

You won’t need to add additional packages to use CSS Modules. All major frameworks and libraries provide inbuilt support.

## Cons of CSS Module

While CSS Module offers many benefits, it’s not a perfect solution. Below are some considerations to keep in mind.

### The nonstandard :global property

When targeting selectors in the global scope, you must use the :global rule. This not a part of CSS specifications but is used by JavaScript to label global styles.

### No dynamic styles

With CSS Module, all the declarations go into separate CSS files. It’s therefore impossible to implement dynamic styles like CSS-in-JS, as we can’t implement any JavaScript in CSS files.

### External CSS files

You can’t omit the usage of CSS files with CSS modules in your components. The only possible way to use CSS modules is to maintain and import external CSS files.

### TypeScript limitation

To use CSS Modules with TypeScript, you have to add module definitions in the index.d.ts file or use a webpack loader:

```typescript
/** index.d.ts **/
declare module "*.module.css"; // TS module for CSS Module files
declare module "*.module.scss"; // TS module for CSS Module files in SCSS format
```

## Recommendations for where to use CSS Module

Using CSS Module is a good choice if you have a performance-critical application with a large UI. Since everything offered by CSS Module is ultimately based on traditional, non-experimental usage, this method makes it easier to monitor and fix performance.

The CSS Module files are simple to adapt code from any CSS framework of your choice since all you’re dealing with is CSS. Some basic knowledge of CSS is sufficient for this task, as discussed previously.

## Modern CSS features to watch

In the introduction, I mentioned how some modern CSS features may help solve the scoping problem in the future without relying on CSS Module, CSS-in-JS, or any other JavaScript solution.

New and planned features — such as scoping directives and the @scope pseudo-element — aim to address the old issues with traditional CSS. This, in turn, may reduce the need for developers to turn to methods like CSS-in-JS as workarounds for those issues.

Let’s take a look at how the current draft for scoped CSS could solve the problems with CSS-in-JS and even CSS Module. For a full list of other modern CSS features, check out the State of CSS 2022.

### The potential future of CSS scoping

After the strange introduction and removal of <style scope> from the CSS specifications, the current draft for scoped CSS looks good enough to define scoping premises for elements by writing CSS rules.

Its current status involves using a directive and a pseudo-class to control the provision of scoping for a given element. Here is a rough picture of how it will lock an element’s scope within a boundary and maintain it regardless of the cascade’s rules of scoping:

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

This new feature may remove the need for CSS Module or CSS-in-JS to resolve the scoping problem. We have to wait and see until it becomes available in our browsers.

## Conclusion

Above, we discussed how CSS render-blocking can be a major performance issue for your web apps. We then discussed some solutions to fix this issue, which led us to explore CSS-in-JS, CSS Modules, and the current status of the official in-progress draft for new scoped CSS features.

Developers who like JavaScript love CSS-in-JS because it covers almost all styling aspects with JavaScript. On the other hand, those who like CSS — and want the current technologies to support developers and end users equally — may prefer CSS Module.

I hope you enjoyed this article. Let me know your thoughts, questions, and suggestions in the comments.
