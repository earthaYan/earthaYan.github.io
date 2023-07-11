---
title: unit-test-with-react
date: 2023-04-18 00:38:16
tags: [React]
categories: 翻译
---

原文地址：
https://blog.openreplay.com/unit-testing-with-the-react-testing-library/

# 使用 React Testing Library 进行单元测试

单元测试是一种用来测试单独的代码片段的测试方法，比如 function 或者 class,通过这种测试方法来确保代码正常工作。当在 React 中执行单元测试时，我们将组件与应用其他部分隔离，对这个组件进行单独测试。单元测试目的是在开发进程早期就可以捕获 bug，避免问题出现在最终的生产环境中。它给我们带来了许多好处，这让单元测试在 web 开发进程中变成了必需品。下面是执行这个过程的一些原因：

- **早期 bug 检测**: 单元测试可以帮助我们在开发过程早期识别出 bug，避免变得更复杂和不容易修复。
- **增强对修改的信心**:单元测试提供了一个简单的途径证明代码修改不会破坏已存在的功能。
- **能够起到文档的作用**: 单元测试作为代码文档的一种形式而存在，为我们对于代码如何工作提供了清晰的认识。
- **使开发更快**: 单元测试提供了在某段时间内只测试一小部分代码的方法。这让开发者在某一时间内只需要专注于那一段代码，也让debug更简单。
- **持续集成**: 单元测试可以包含在可持续集成系统中，这个系统可以自动进行测试并且当代码发生变化时提供反馈，以确保代码修改在部署之前总是被测试过的。

开发人员知道如何在他们的应用中执行测试，这是再怎么强调也不过分的，因为测试可以识别任何和实际需求相反的差距，错误或者缺失的需求，从而确认应用为公众使用做好准备。借助下面这些例子，这篇文章旨在教会你如何在React应用中使用React Testing Library执行单元测试   

## React Testing Library

[React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) 是一个React库，为测试React组件提供直观和高效的API。它基于[DOM Testing Library](https://testing-library.com/docs/ecosystem-jest-dom/)构建，并且提供了更加以用户为中心的测试React组件的方式。这个库提供了一系列工具函数，这些让写测试断言React组件的行为更加容易。RTL函数被设计成和React渲染的真实DOM元素一起使用而不是虚拟DOM，所以测试会模仿用户如何和应用交互。你可以在[这里](https://testing-library.com/docs/react-testing-library/intro/)了解更多关于React testing library的知识。

## 使用 React testing library在React中单元测试的构建块
React中使用React testing library的单元测试如下所示：

```javascript
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
```

- 从上面的例子可以看出，首先看到的就是一些必要的模块必须被导入，比如render,screen和被测试的组件(App)。render方法返回一个对象，这个对象提供对渲染组件的访问，以及多个可以查询组件和与组件交互的工具函数
- 其次，测试块包含两部分；第一部分是描述测试的文本内容，第二部分是一个回调函数。
- 在测试块中，使用render方法渲染将要被测试的组件。
- 渲染完组件后，我们需要在待测试的组件中找到特定的元素。在一个渲染的组件中查找元素主要有三种方法：getBy, findBy和 queryBy。
  - - getBy 方法被用来获取符合条件的单个元素。如果使用同一个属性找不到或者找到多个元素，会抛出错误。当测试一个元素是否在DOM上时这个方法非常有用，我们希望只有一个元素满足这个条件。比如：
   This method is useful when testing if an element is present in the DOM and we expect only one element to match the condition. For example:

```javascript
const { getByText } = render(<MyComponent />);
const element = getByText('Hello World');
```
在上述例子中，getByText会查询DOM找一个包含 ‘Hello World’文本内容 的元素，返回第一个符合条件的元素。如果没有一个元素包含‘Hello World’或者有多个元素包含它，就会抛出一个错误。

- findBy方法被用来获取满足条件的单个元素。如果没有找到则返回null,如果找到多个就抛出错误。当你不确定这个元素是否在DOM中或者你希望只有一个元素符合条件的时候这个方法非常有用，比如：

```javascript
const { findByText } = render(<MyComponent />);
const element = await findByText('Hello World');
```
在上面这个例子中，findByText会查询DOM找一个包含 ‘Hello World’文本内容 的元素，返回第一个符合的元素或者如果元素未找到的话返回null。如果有多个则会抛出错误。

- queryBy被用来获取满足条件的所有元素。如果没有找到元素则返回null,否则以数组的形式返回。当你希望找到多个满足条件的元素时候，这个方法非常有用。例如：

```javascript
const { queryByText } = render(<MyComponent />);
const elements = queryByText('Hello World');
```
在这个例子中，queryByText会查询DOM寻找包含文本 ‘Hello World’的所有元素，返回一组符合条件的元素，或者如果没有找到的话会返回null。这些方法都接受一个条件作为参数，这个条件可以是一个字符串（按元素文本搜索），组件，角色或者你需要查询的其他属性。你也可以串联多个条件来进行更精确的搜索。这里是一个例子：

```javascript
const { getByRole, getByLabelText } = render(<MyComponent />);
const element = getByRole('button', { name: 'Save' }).getByLabelText('Save');
```
在这个例子中，getByRole将会查询DOM寻找角色为button，name是Save的元素。然后getByLabelText会遍历getByRole返回的所有元素；它将返回label文本为‘Save’的相同元素，如果没有找到元素或找到多个元素，就抛出错误。

- 找到元素后，测试期间我们可以使用来自 @testing-library/react 库的fireEvent 函数在React组件的元素上模拟用户事件（如：click,input等）。这里是一个使用fireEvent模拟点击按钮事件的例子：

```javascript
import { render, fireEvent } from '@testing-library/react';
import MyComponent from './MyComponent';

test('clicking the button calls the onClick prop', () => {
  const onClick = jest.fn();
  const { getByText } = render(<MyComponent onClick={onClick} />);
  const button = getByText('Click me');
  fireEvent.click(button);
  expect(onClick).toHaveBeenCalled();
});
```
在这个例子中，我们从@testing-library/react导入了render和fireEvent 功能，然后我们导入想要测试的组件。在测试函数中，我们创建了mock函数来作为组件的onClick属性使用。然后使用render函数来渲染组件，使用getByText 方法来找到包含文本”click me"的按钮元素。通过使用fireEvent.click函数，我们模拟了点击按钮，最终，预期检查mock的函数应该被调用。你可以使用fireEvent.change模拟input的change 事件，使用fireEvent.submit模拟表单的提交事件以及其他事件。

- 随着找到元素和事件fire,我们随后检查他们行为是否与预期一致或者他们应该在哪里被找到。这个检查被称为断言，断言被用来测试在渲染的组件里某个条件是否满足。这些断言典型的用法是检查元素状态，文本或者属性以及组件行为。RTL提供了一系列内置的断言比如toHaveBeenCalled，toHaveBeenCalledTimes, 和 toHaveBeenCalledWith，断言函数行为比如事件处理器。举个例子：

```javascript
test('simulate and test click event on a button', () => {
  const handleClick = jest.fn();
  const { getByTestId } = render(<MyComponent onClick={handleClick} />);
  fireEvent.click(getByTestId('my-button'));
  expect(handleClick).toHaveBeenCalled();
  expect(handleClick).toHaveBeenCalledTimes(1);
  expect(handleClick).toHaveBeenCalledWith(expect.anything());
});
```
这个例子中，我们使用jest.fn() 创建一个我们可以断言的mock函数。然后我们将它作为prop传递给组件，接着使用fireEvent.click 模拟点击按钮。再断言。使用 toHaveBeenCalled()方法，检查当点击按钮时，函数handleClick是否被调用。 使用toHaveBeenCalledTimes(1)，我们测试当按钮点击的时候，handleClick是否只被调用过一次。最后，使用toHaveBeenCalledWith()测试他是否只被调用一次且带有参数的调用。

注意RTL目的是提供最小且灵活的一系列断言，并且你可以使用任何断言库，类似chai，jest等断言组件状态。

##  使用 React- Testing Library编写有效的单元测试的步骤
这里是使用React Testing Library编写综合有效的单元测试需要遵循的步骤：
  
- 导入需要的模块：你必须导入React和React Testing Library。你也需要导入你想测试的组件。
- 写测试：使用Jest的描述和他的方法来为组件写测试。你会使用React Testing Library的render方法来渲染测试中的组件。
- 从组件获取元素：使用来自返回的渲染对象getBy 和queryBy方法从已经渲染的组件中获取元素。你可以使用这些方法通过文本，展示值，label文本或者联合体获取元素。
- 和组件交互：使用fireEvent 方法和组件交互。你可以使用fireEven模拟类似点击按钮，提交表单或者修改输入值这样的用户事件。
- 做出断言：使用Jest的expect方法对组件的状态做出断言。举例来说，你可能会断言表单已经成功提交或者展示错误信息。
- 清理：在进入下一个测试之前，确保清理干净任意的spy,mock或者给组件添加的事件监听器。
- 为每个组件重复这个过程：为每一个你想测试的组件写一个单独的测试。为每个测试重复上述步骤。现在我们自己来写一些测试。

## 写单元测试
为了测试，我们还会创建简单的联系表单，校验每一个field。
![](https://blog.openreplay.com/images/unit-testing-with-the-react-testing-library/images/UHSZlyc.png)
为了测试，我们将创建一个简单的表单，校验每一个field。如果空白表单被提交就会展示错误信息。
![](https://blog.openreplay.com/images/unit-testing-with-the-react-testing-library/images/yHK5HIa.png)

做完这些之后，我们将为这个表单写一些单元测试：
- 测试label和输入域是否正确渲染：
```javascript
it('renders the form with correct labels and inputs', () => {
  const { getByLabelText, getByRole } = render(<App />);
  expect(getByLabelText('Name:')).toBeInTheDocument();
  expect(getByLabelText('Email:')).toBeInTheDocument();
  expect(getByLabelText('Message:')).toBeInTheDocument();
  expect(getByRole('textbox', { name: 'Name:' })).toBeInTheDocument();
  expect(getByRole('textbox', { name: 'Email:' })).toBeInTheDocument();
  expect(getByRole('textbox', { name: 'Message:' })).toBeInTheDocument();
});
```
这个测试用来检测表单的label和输入值是否正确。来自react-testing-library的render函数被用来渲染App组件。之后，getByLabelText和getByRole函数用来找表单里的元素，并断言他们在文档中。

- 测试是否会展示空域的错误信息：

```javascript
it('displays errors for empty fields', () => {
  const { getByText, getByRole } = render(<App />);
  const submitButton = getByRole('button', { type: 'submit' });
  fireEvent.click(submitButton);
  expect(getByText('Name is required')).toBeInTheDocument();
  expect(getByText('Email is required')).toBeInTheDocument();
  expect(getByText('Message is required')).toBeInTheDocument();
});
```
这个测试检查当用户尝试提交空白表单的时候是否会展示正确的错误信息。我们的表单是使用render函数渲染的，使用getByRole方法找到按钮元素。fireEvent函数模拟点击提交按钮。getByText函数找到错误信息并且断言他们在文档里。


- 测试在email地址不合法的情况下是否会展示错误信息:

```javascript
it('display error for invalid email', () => {
  const { getByLabelText, getByText, getByRole } = render(<App />);
  const emailInput = getByRole('textbox', { name: 'Email:' });
  fireEvent.change(emailInput, { target: { value: 'wdwkfb.com@' } });
  const submitButton = getByRole('button', { type: 'submit' });
  fireEvent.click(submitButton);
  expect(getByLabelText('Email:')).toBeInTheDocument();
  expect(getByText('Email is not valid')).toBeInTheDocument();
});
```
这个测试检测包含不合法的邮件地址的表单是否会在用户尝试提交表单会展示错误信息。表单渲染以后，通过getByRole方法找到邮箱输入。fireEvent函数被用来模拟将邮件地址变成不合法的值。提交按钮找到以后像以前的测试一样使用同样的步骤点击。使用getByText方法找到错误信息并断言存在于文档中。

- 当右边的输入被给定的时候，测试我们的表单是否被提交： 

```javascript
it('submit the form with correct data when the submit button is clicked', () => {
  const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
  const { getByLabelText, getByText } = render(<App />);
  const nameInput = getByLabelText('Name:');
  const emailInput = getByLabelText('Email:');
  const messageInput = getByLabelText('Message:');
  const submitButton = getByText('Submit');
  fireEvent.change(nameInput, { target: { value: 'John Doe' } });
  fireEvent.change(emailInput, { target: { value: 'johndoe@example.com' } });
  fireEvent.change(messageInput, {
    target: { value: 'Hello, I would like to get in touch.' },
  });
  fireEvent.click(submitButton);
  expect(console.log).toHaveBeenCalledWith({
    name: 'John Doe',
    email: 'johndoe@example.com',
    message: 'Hello, I would like to get in touch.',
  });
  spy.mockRestore();
});
```
这个例子中，我们使用Jest的spyOn方法创建对console.log方法的监听，然后使用 mockImplementation来用mock函数替代真正的方法。这允许我们验证 console.log 方法可以在不往控制台记录任何信息的情况下被调用。然后我们使用来自@testing-library/react的render方法渲染App组件，使用getByText从已经渲染的组件中获取到按钮元素。使用fireEvent.change，我们可以给输入域提供输入。接下来使用fireEvent.click来模拟点击按钮，断言有预期消息的console.log方法被调用。最后使用mockRestore来恢复原始的console.log方法，所以spy不会影响任何未来的测试。

## 运行测试
到目前为止，我们已经学习了如何为React应用搭建单元测试。为了运行我们已经写好的测试，需要做以下这些事：
- 将你的测试文件保存在组件文件的同级目录，命名为[component-name].test.js。
- 在你的终端，导航到项目的根目录，运行下面的命令：npm run test，如果你使用的是yarn,可以运行yarn test
- test runner会自动找到你项目里的所有测试文件并运行，在终端展示结果。
- 如果你想要运行指定的测试文件，可以使用 npm run test [test-file-path]或者yarn test [test-file-path]命令。
- 终端上展示了我们测试的结果，包含了所有的测试和他们的结果。这是当测试全部通过的时候的输出：

  ![](https://blog.openreplay.com/images/unit-testing-with-the-react-testing-library/images/Z92HEh8.png)

  现在我们让其中一个测试失败，看看是什么样子；

  ![](https://blog.openreplay.com/images/unit-testing-with-the-react-testing-library/images/iYziRAC.png)
  我们可以看到React Testing Library 向我们精确地展示了什么原因导致了错误，因此我们能够快速纠正错误。
## 写有效单元测试用例的一些建议

- **保持测试内容小且集中**: 每个测试应该只测试组件特定的行为或者方面，避免在单个test中测试多个行为。这可以提高你的测试包的可靠性，可读性和可维护性。这里是一个反面例子：

```javascript
import React from 'react';
import MyComponent from './MyComponent';
import { render, fireEvent } from '@testing-library/react';

describe('MyComponent', () => {
  it('tests multiple behaviors', () => {
    const { getByText, getByRole } = render(<MyComponent title="Test title" />);
    expect(getByText('Test title')).toBeInTheDocument();
    fireEvent.click(getByRole('button'));
    expect(getByText('Button clicked')).toBeInTheDocument();
  });
});
```
这同时测试了标题的展示和按钮点击的行为，这使得它在失败的时候难以理解和debug。这里是同样的测试更好的写法：

```javascript
import React from 'react';
import MyComponent from './MyComponent';
import { render, fireEvent } from '@testing-library/react';

describe('MyComponent', () => {
  it('renders the title', () => {
    const { getByText } = render(<MyComponent title="Test title" />);
    expect(getByText('Test title')).toBeInTheDocument();
  });

  it('handles button click', () => {
    const { getByText, getByRole } = render(<MyComponent title="Test title" />);
    fireEvent.click(getByRole('button'));
    expect(getByText('Button clicked')).toBeInTheDocument();
  });
});
```
在这个例子中，我们使用来自@testing-library/react的render方法渲染组件和来自jest的fireEvent.click模拟按钮点击事件。然后getByText 和 getByRole函数被用来在页面中定位元素。这些测试被写在单独的test块中，遵循建议的做法，这让他们即使随着时间的流逝也能易于理解和维护。

- **测试特定结果**: 当我们专注于测试组件特定的结果或者某些方面的行为，而不是专注于渲染的整体正确性，单元测试会更高效。通过测试特定的结果，我们可以确保组件功能在一些特殊的场景下能按照预期运行。举例来说，你可以测试当传入指定prop的时候这个组件是否会正确展示指定的数据，或者也可以测试当点击指定的按钮时触发操作。这些类型的测试提供了关于组件的行为更特定的和更有意义的信息，这使得捕获可能发生的问题或者bug更加容易。
- **同时测试符合预期和不符合预期的行为**: 测试组件在给定合法输入的时候是否行为正常，同时测试它是否能处理不合法的输入和边缘用例。这里是一个例子；假设有这样一个React组件，有一个数字value作为prop,返回基于值的信息：

```javascript
import React from "react";

const ValueMessage = ({ value }) => {
  let message = "";
  if (value > 10) {
    message = "Value is greater than 10";
  } else if (value < 0) {
    message = "Value is negative";
  } else {
    message = "Value is between 0 and 10";
  }
  return <div>{message}</div>;
};

export default ValueMessage;
```

为了给这个组件写有效的单元测试，我们应该同时测试符合预期和不符合预期的行为：测试符合预期的行为；

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import ValueMessage from './ValueMessage';

test('displays "Value is greater than 10" when value is greater than 10', () => {
  const value = 11;
  const { getByText } = render(<ValueMessage value={value} />);
  expect(getByText('Value is greater than 10')).toBeInTheDocument();
});

test('displays "Value is between 0 and 10" when value is between 0 and 10', () => {
  const value = 5;
  const { getByText } = render(<ValueMessage value={value} />);
  expect(getByText('Value is between 0 and 10')).toBeInTheDocument();
});

test('displays "Value is negative" when value is negative', () => {
  const value = -5;
  const { getByText } = render(<ValueMessage value={value} />);
  expect(getByText('Value is negative')).toBeInTheDocument();
});
```

现在来测试一些不符合预期的行为；

```javascript
import React from 'react';
import { render } from '@testing-library/react';
import ValueMessage from './ValueMessage';

test('displays "Value is between 0 and 10" when value is undefined', () => {
  const { getByText } = render(<ValueMessage value={undefined} />);
  expect(getByText('Value is between 0 and 10')).toBeInTheDocument();
});

test('displays "Value is between 0 and 10" when value is null', () => {
  const { getByText } = render(<ValueMessage value={null} />);
  expect(getByText('Value is between 0 and 10')).toBeInTheDocument();
});

test('displays "Value is between 0 and 10" when value is NaN', () => {
  const { getByText } = render(<ValueMessage value={NaN} />);
  expect(getByText('Value is between 0 and 10')).toBeInTheDocument();
});
```
在这个例子中，我们通过提供给组件合法的输入（大于10，1-10，负数的数字）测试符合预期的行为。我们也测试了不符合预期的行为，比如给组件的value的props提供undefined，null和NaN。边缘用例帮助确保组件可以优雅处理不合法输入，避免app崩溃。


- **使用合理的测试方式**: React Testing Library 提供了不同的测试组件的方法，比如：render,fireEvent和wait。为你要测试的行为选择合理的方法。

- **避免测试还没有实现的细节**: 组件也许内部会变化，但是只要他们的行为不变，我们的测试仍然可以通过。避免测试内部的实现细节，而是专注于测试组件的公共API。举例来说,假设你有一个<Counter /> 组件,在屏幕上显示一个数字,允许用户增加或减少这个数字.这里是一个例子展示了你在<Counter />组件也许想要测试什么:

```javascript
it("renders the correct number", () => {
  const wrapper = shallow(<Counter value={3} />);
  expect(wrapper.text()).toEqual("3");
});

it("increments the value correctly", () => {
  const wrapper = shallow(<Counter value={3} />);
  wrapper.find("[data-test='increment-button']").simulate("click");
  expect(wrapper.text()).toEqual("4");
});

it("decrements the value correctly", () => {
  const wrapper = shallow(<Counter value={3} />);
  wrapper.find("[data-test='decrement-button']").simulate("click");
  expect(wrapper.text()).toEqual("2");
});
```
在这个例子中,测试专注于<Counter />组件的行为。他们检测组件是否渲染了正确的数字，同时也检测用户是否可以增加或减少数字。即使组件的执行变了，只要行为不变，测试应该仍然会通过。避免测试内部实现细节非常重要，比如用于展示一个数字或者按钮的特定HTML元素。举例来说，组件也许会从使用<p> 元素展示数字变成使用自定义的<Display>组件展示。只要组件表现一致，测试应该仍然会通过；就不需要更新测试。

- **使用测试替身**: 
使用测试替身，比如mock,spy和stub来隔离他们的依赖和组件，让测试更快和更可靠。测试替身可以隔离组件和依赖，让测试更加快速和可靠。举例来说，假设你有<FetchData />组件，它从API获取数据并且在屏幕上展示。当测试<FetchData />组件的时候，你不想发送一个API的网络请求，因为这会减缓测试速度，并且没有那么可靠（比如，API会挂掉，响应在每次返回都不同）。取而代之的是，你可以使用测试替身来模拟API响应。这里演示了如何使用mock来测试<FetchData /> 组件：
```javascript
it("renders data correctly", () => {
  const apiResponse = [
    { id: 1, name: "John" },
    { id: 2, name: "Jane" },
  ];
  const mockFetchData = jest.fn().mockResolvedValue(apiResponse);
  const wrapper = shallow(<FetchData fetchData={mockFetchData} />);

  // 等待组件渲染
  setTimeout(() => {
    expect(wrapper.text()).toContain("John");
    expect(wrapper.text()).toContain("Jane");
  }, 0);
});
```
这个例子中， mockFetchData函数模仿API响应。mockFetchData函数作为prop传递给<FetchData />组件，所以会调用mockFetchData而不是真正的网络请求。这让测试更加快捷且可靠，因为测试不再依赖API。
你也可以使用spies和stubs来隔离组件和他们的依赖。举例来说，你也许会使用spy检测某个功能是否被调用或者使用stub用简单版本的对象代替真正的对象来测试。使用测试替身是把组件和依赖有效的隔离开来，让测试更加快捷和可靠。这是测试工具包中的一项珍贵的技术。

- 保持测试用例最新:让测试用例跟随代码的最新修改而更新。这可以确保测试用例一直合法和有作用。
- 隔离测试： 尽可能隔离测试组件避免测试依赖项。
 
## 总结
单元测试帮助我们确保组件正常工作以及对代码库做的修改不会破坏已有功能。这可以显著提高React应用的整体质量和可靠性。 除此之外，React testing library 也很容易使用。它能和其他测试框架很好的集成，这对任何一个期望在他们项目里实现单元测试的React开发者都是一个好的选择。

