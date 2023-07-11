---
title: 【译】The Evolution of the Modern Web Application Development
date: 2022-09-19 11:22:55
tags: [前端]
categories: 翻译
---
>  本文原文链接：[https://blog.bitsrc.io/the-evolution-of-the-modern-web-application-development-18aa95b7c1a](https://blog.bitsrc.io/the-evolution-of-the-modern-web-application-development-18aa95b7c1a)

## 现代web应用开发的进化

### 那时候开发人员的工作和现在大不相同

![人类进化](https://cdn-images-1.medium.com/max/8208/1*47wUIbkat0g69vKjxm-rOg.jpeg)

你可能会非常好奇: 什么样的开发者会写出像这样的文章?

那么我可以回答这个问题: *一个老程序员*.

![推特给了我写这篇文章的灵感(这让我觉得自己老的要命)](https://cdn-images-1.medium.com/max/2416/1*cH7VoyCKrOykiUr5wDr0KA.png)

不开玩笑了,我不年轻了,且到目前为止已经在 IT 行业工作了20年. 好处就是当我年纪大到可以写这篇文章的时候，我还很年轻，我仍然记得我们过去的工作有哪些不同。所以，我接受了我在同一时间可以既年轻又年迈。

也就是说, “以前” 我们常常使用不同的工具、模式、heck甚至标准工作，那时候兼容 IE 还不是一个笑话, 事实上, 兼容所有主流浏览器也不容易。

让我们沿着记忆的小路慢慢前行,慢慢回忆过去的情形,这样我们可以更好的理解现在使用的工具。

## Netlify? Vercel? AWS? 这是什么?

当我20年前入行的时候，把平台甚至软件作为一个 Service 这件事还不存在。

那时候开发软件有多不同呢? 事实上,  “API Everything” 思想那时候还没有真正实现。 启动并运行一个 Service 需要大量精力和金钱，所以除非有必要的理由，否则没有人会去做。

除此之外, 我们过去使用的工具也不一样, Node.js 还没出现, 所以想使用像 Next.js 这样的框架也是不可能的。我一开始使用 PHP 4, 它和现在的 Node.js(或其他工具) 不一样，不能创建你自己的 web 服务器。相反, 我们必须安装 [Apache Web Server](https://httpd.apache.org/),或者如果你是一个冒险者,并且想拥有一个基于 Windows 的 web 服务器, Internet Information Service(IIS) 也可以, 它曾经是(或许现在也是？) Microsoft 提供的一个选择(这在过去并不理想)。

关于这种工作方式很有趣的一点是：你的应用是一系列的脚本，它们会在每次服务器接收到一个请求的时候被执行。 这意味着你的服务器上没有运行中的 app。 每一个新的请求最终都会变成一个新的进程，运行在服务器内部。这意味着服务器必须足够强大，能够处理很多请求，因为每个请求都是一个并行进程，会占用一块内存和 CPU 时间。

当然, 数据库连接 (和其他的服务) 也必须在脚本的生命周期内被建立和关闭(比如在请求期间)。

如果你想要扩容, “自动扩容”是不可能的。我还记得特定节假日必须评估运行电商网站需要的服务器数量是多么痛苦。 当然, 总是有不足之处，以至于开发者们周末期间不得不进行紧急修复处理(比如重新启动挂掉的数据库,或者清理大到充满整个硬盘的日志文件)。

### 前端技术栈比现在更简单

因为下面的一些原因，那时候的前端场景非常不同：

 1. 我认为最重要的一点是那时候的 HTML, CSS 和 JavaScript 还没有现在这么标准化。 尤其是后者, 每个浏览器都遵循自己的指导方针实现了各自的版本, 并没有考虑到其他的浏览器. 它更像一场比赛而不是合作。所以 Chrome 有的功能在   Firefox 或者 IE 中可能并不可用，反之亦然。 这意味着构建任何人都能使用的 Web 应用，就必须增加许多代码处理这些差异。

 2. 那时候也没有 UI 框架, 只有各种库. 对我来说, 这个区别非常重要, 因为现在像 React 和 Vue 这样的框架提供了一个体系架构，定义了一系列你可以遵循的工具和模式。如果你基于他们去构建，就像 Next, Nuxt 和 其他一些应用做的那样，那么他们就为你提供了一条可遵循的路径。过去我们有 jQuery,[underscore](https://underscorejs.org/)(之后几乎被[lodash](https://lodash.com/)取代)，以及 [Mootools](https://mootools.net/)。这些都是很好的库，但是没有真正强制推行一种工作方式，这导致人们认为前端开发不需要使用任何先进的开发方法和技术。我记得我曾经认为 JavaScript 就是增加表单验证,不然就是为静态网站添加一些愚蠢的动画。

你必须记住, “过去那时候”, 我们甚至不能异步加载数据。直到术语 AJAX 流行起来，才发现了这种能力 (并且开始学习异步行为的概念)。这些在现在看来很普通的事情对于当时来说是工作模式的转变。

### 现在它容易多了

现在开发一个应用简单多了,非常方便,不会让我担心。

你可以把你的 Github 账号和一个 Netlify (或者类似的平台) 账号连接起来，在世界的*某个地方*自动部署应用。Heck 你可以利用类似 Supabase, 或者 AWS DynamoDB 的服务，在这里你都不用担心维护数据库或者认证服务。

甚至一些服务会集中控制你的日志文件, 像 [Loggly](https://www.loggly.com/) 和 [Splunk](https://www.splunk.com/), 所以如果你的日志轮换配置不是最优的话，也不需要担心硬盘空间被全部占用。

那时候独立工作是很困难的，但是现在你可以真正地接近独立工作(如果你愿意为此付出报酬的话)。

### 前端技术栈变得更有难度了，但是这是一件好事

前端生态系统现在很大，React、Vue、Svelte 甚至是 Angular,他们启发了许多框架的诞生，这些框架让前端更上一层楼。

我这么说吧,过去当我开始工作的时候,web 开发的座右铭常常是 “瘦客户端,胖服务端”或者是“让你的客户端变傻”又或者是这些思想的变体。本质上来说,你的客户端代码只是简单的表示层，不应该在上面做任何“困难”的事情，因为浏览器还没有做好准备。相反，我们将“复杂的”逻辑维护在后端，只使用 JavaScript 显示漂亮的颜色和一些警告框。

从那时起，我们已经走过了一条漫长的路。当然,这些不是没有代价的。过去我们的“bundler”是一系列的脚本标签，添加在 HTML 顶部，并且这就是所有了。

现在驱动一个现代 app 的 JS 数量已经增长了如此之多，用于优化它的工具生态系统也随之增长。

现在你需要：

 1. 如果你使用的不是纯 JavaScript 的话，就需要一个转译器。

 2. 打包工具把所有的代码放在一起，移除不必要的部分,以一种对用户来说低“开销”的方式传输和发布。

 3. lint程序，确保10万行JS代码中的每一行都遵循团队中相同的标准。

 4. 一个拥有热更新和文件监听功能的 webserver,优化开发体验。否则修改单独一行代码也会花费大量时间去更新。

 5. 一个包管理器, 因为作为开发者，我们已经完成了重复造轮子的工作。

 6. 一个版本控制系统 (通常是 Git + Github 但是也有其他一些选择) 确保团队成员可以很容易就同一个项目合作。

 7. 一个测试运行器,因为现在你的前端业务逻辑已经如此复杂（顺便说一下也很伟大），以至于需要一个方法确保所有的事情都和预期一样运行。

我打赌你可能会想到更多。这对刚起步的人来说可能会有一点不知所措。

我知道这是我在多年不编程后重新上马的原因。
I know it was for me when getting back on the horse after years of not coding.

值得庆幸的是，行业仍然在进化。虽然它们仍然是新的，并试图进入，但人们正在开发专门用于再次简化技术栈的工具，同时保留当今复杂解决方案的功能和能力。

### web 开发工具生态系统的未来

旅程还未结束，这是好事情。

如果你仔细思考这件事情，我们在代码中也是这么做的：

 1. 我们针对一个问题写了简单的解决方法。

 2. 我们意识到这个解决方法并没有覆盖所有潜在的边际案例，所以需要在此基础上添加更多代码，直到它能够正常工作。

 3. 我们意识到它是一个可恶的 Frankenstein 类型的代码，不可维护并且难以理解，所以我们开始重构和简化。

我们的工具链正在经历同样的过程。我们现在开始看到步骤 #3。我们看到像来自[bit.dev](https://bit.dev/)的[Bit](https://bit.dev/) 这样的工具正在尝试集中化管理开发周期中的所有任务。

事实上, 使用 Bit, 你可以管理代码的版本并且测试代码, 并且作为个人包发布。你甚至可以用它管理一个 Monorepo 而不需要担心其他工具。

当然，这也不是说工具会为你做完所有的事情，事实上，他只是管理了整个你通常会需要担心的工具生态系统。如果你问我，我会觉得这是个聪明的做法。

另外, 类似打包工具这样的工具开始见证一个不再需要他们的趋势。听我说, 我在主持的 [20MinJS podcast](https://podcast.20minjs.com/) 节目中采访了 [Michele Riva](https://twitter.com/MicheleRivaCode)(他是来自 Nearform 的高级软件架构师),在那一集中,Michele 提及了 [Vite](https://vitejs.dev/) 这样的新一代打包工具是如何利用浏览器的新能力：[ECMA Script import 语句](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import),异步加载文件,因此提升了 JavaScript 的加载速度(而不是必须加载一个或多个大的被打包的文件)。

所以如果你问我的话，未来看上去是非常光明的。仍然有许多工作要做，但是担忧必须为应用手动设置平台的日子已经一去不返了。工具生态系统正在进化至一个点：我们可以快速制作原型和部署想法,然后将它们发展成成熟的应用程序，而无需改变太多，只需要改变我们使用的服务或我们支付的层。如果我们想要扩容，因为它们最终获得了成功，只要我们准备好为它付费，我们也可以获得。

我认为 web 开发行业的当前状态的魅力在于我们拥有选择的权利。

我们仍然可以使用“old school 方式”手动去做每一件事情，管理我们自己的服务器,规划应用所需的流量和工作量，并增加对应的基础设施。

或者如果愿意信任已经试用并且经过测试的外部平台和服务，我们可以支付他们报酬为我们工作。我们从本质上用服务替代了原本必须成熟的 IT 团队，这对一些公司来说是一个很好的引导策略。是的，最终你会需要 IT 团队和你一起工作，这是不可否认的，但是没有 IT 团队，您可以比以前走得更远。

除此之外,工具本身也会成长和适应社区的反馈。**Developer Experience** 是一个会在日常工具设计中频繁抛出的术语，并且我们可以从使用这些工具的简单程度中看出这一点。我认为这是非常聪明的一步，它将进一步推动开发速度和能力。

你认为呢? 从你的角度来看，未来是光明的吗?

## 可组合: 像乐高一样更快地构建应用

![](https://cdn-images-1.medium.com/max/2400/1*x2l8LRH1nbC1FQZUdt50RQ.jpeg)

[Bit](https://bit.cloud) 是一个以模块化和协作方式构建 app 的开源工具。通过可组合的方式更快,更一致并且更容易扩容。

→ [了解更多](https://bit.dev)

构建应用,页面,用户体验和 UI 作为独立的组件。使用它们更快地组成新的应用和体验。将任意框架和工具引进你的工作流程中。共享、复用和协作以一起构建应用。

帮助你的团队了解:

**→ [Micro-Frontends](https://blog.bitsrc.io/how-we-build-micro-front-ends-d3eeeac0acfc)**

**→ [Design Systems](https://blog.bitsrc.io/how-we-build-our-design-system-15713a1f1833)**

**→ [Code-Sharing and reuse](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4)**

**→ [Monorepos](https://www.youtube.com/watch?v=5wxyDLXRho4&t=2041s)**

## 了解更多
[**How We Build Micro Frontends**](https://blog.bitsrc.io/how-we-build-micro-front-ends-d3eeeac0acfc)
[**How we Build a Component Design System**](https://blog.bitsrc.io/how-we-build-our-design-system-15713a1f1833)
[**How to reuse React components across your projects**](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l3bhezsg)
[**5 Ways to Build a React Monorepo**](https://blog.bitsrc.io/5-ways-to-build-a-react-monorepo-a294b6c5b0ac)
