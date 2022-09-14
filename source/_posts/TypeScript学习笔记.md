---
title: TypeScript学习笔记
date: 2022-08-31 10:37:50
tags: ['JavaScript','前端']
categories: TypeScript
---

## TypeScript类型来源：
- 通过赋的值自动进行类型推论
- 通过 `interface` 和 `type` 定义类型
>JS自带的基础类型：
>`boolean, bigint, null, number, string, symbol,undefined`
- 多个简单类型组合成复杂的类型
  - Unions：联合类型

  {% asset_img typeof.jpg typeof 结果 %}

  ```TypeScript
  type WindowStates = "open" | "closed" | "minimized";
  function wrapInArray(obj: string | string[]) {
    if (typeof obj === "string") {
      return [obj];
    }
    return obj;
  } 
  ```

  - Generics：泛型
```TypeScript
type StringArray = Array<string>;

interface Backpack<Type> {
  add: (obj: Type) => void;
  get: () => Type;
}
// 告诉TypeScript 有一个常量叫做 `backpack` 
declare const backpack: Backpack<string>;
// object 是一个字符串类型, 因为在上面声明了Backpack的变量
const object = backpack.get();
//由于backpack 变量是一个字符串, 不能传一个number给add方法
backpack.add(23);//报错：Argument of type 'number' is not assignable to parameter of type 'string'.
```
## TypeScript的鸭子类型(structural typing)
**定义**：如果两个对象有一样的shape,他们就会被认为是一样的类型
```TypeScript
interface Point {
  x: number;
  y: number;
}
function logPoint(p: Point) {
  console.log(`${p.x}, ${p.y}`);
}

// logs "12, 26"
const point = { x: 12, y: 26 };
logPoint(point);
```
如上述代码所示：变量point从来没有被声明为Point类型。但是TypeScript在类型检查中比较了Point和point的shape,完全一致，所以代码不会报错


**注意**:shape-matching 匹配对象字段的一个子集。
```TypeScript
interface Point {
  x: number;
  y: number;
}
function logPoint(p: Point) {
  console.log(`${p.x}, ${p.y}`);
}
const point3 = { x: 12, y: 26, z: 89 };
logPoint(point3); // logs "12, 26"
const color = {  x: 33,hex: "#187ABF" };
logPoint(color);//此处报错，因为缺少缺少y
```

## TypeScript的额外功能
- 输入的时候提供错误消息
- 代码补全功能
- 通过重构来轻松地重新组织代码
- 通过导航功能来跳转到变量的定义
- 查找给定变量的所有引用

## TypeScript编译器——tsc
```bash
npm install -g typescript
tsc hello.ts
tsc --noEmitOnError hello.ts //报错时不生成输出文件
```
## tsconfig.json配置文件
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom","dom.iterable","esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "experimentalDecorators": true,
    "downlevelIteration":true
  },
  "include": [
    "src",
  ]
} 
```
## 日常类型
- 原始类型：
  - boolean
  - number
  - string
  - bigint
  - symbol
- Array
  - Array\<T\>
  - T[]
- any:
  - 任意类型，不推荐使用
  - 在tsconfig.json中设置{"noImplicitAny": true}可使得它报错
- Function
  - 需要指定 入参类型，返回值类型
  - 匿名函数:当一个函数出现在TypeScript可以决定如何调用它的地方时，该函数的参数会自动指定类型，不需要指定入参和返回值
- 对象类型
  - 可选属性,`name?:string`
- 联合类型unions
  - 类型1|类型2|类型3
  - 类型别名 `type UserInputSanitizedString = string;`

## interface和type的区别
- type创建类型后不能被修改添加新的属性
  {% asset_img interface.jpg interface %}
  {% asset_img error.jpg error %}

上图中左边等价于：
```TypeScript
interface Window{
  title:string;
  ts:TypeScriptAPI
}
```
## 类型断言
1. 使用as关键字
```TypeScript
const myCanvas = document.getElementById("main_canvas") as HTMLCanvasElement;
```
2. 使用尖角括号 —— 代码在.tsx文件中
```TypeScript
const myCanvas = <HTMLCanvasElement>document.getElementById("main_canvas");
```
3. 类型转换使用 as any/unknown as 
```TypeScript
const expr=2
type T = { a: 1; b: 2; c: 3 };
// ---cut---
const a = (expr) as unknown as T;
```
## 字面量类型
1. 如果是let,var定义的变量，他会被认为是基础类型-类型推论
2. 如果是const 定义的常量，它的类型就是常量值，不可修改
3. 如果const 字面量类型推论不符合预期，可通过以下方法解决
```TypeScript
// Change 1:
const req = { url: "https://example.com", method: "GET" as "GET" };
// change 2:
const req = { url: "https://example.com", method: "GET" } as const;
handleRequest(req.url, req.method);

```
## Null和Undefined
- Null：不存在，空对象
- undefined：没有初始化
- 非null的断言操作：使用后缀!（知道类型不可能为null或者undefined）
```TypeScript
function liveDangerously(x?: number | null) {
  //不报错
  console.log(x!.toFixed());
}
```
## 缩小
### 类型保护 typeof
`typeof null ==== 'object'，typeof undefined==='undefined'`
### if检查
```TypeScript
function padLeft(padding: number | string, input: string) {
  if (typeof padding === "number") {
    return " ".repeat(padding) + input;//此时padding类型只有number
  }
  return padding + input;//此时padding类型只有string
}
```
### Truthiness检查：
- `&&`,`||`,`!`,if语句
- <font color="red">0,NaN,"" (the empty string),0n (the bigint version of zero),null,undefined</font>转换为布尔值都是false
### 使用===, !==, ==,  !=
```TypeScript
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    x.toUpperCase();
    y.toLowerCase();
  } else {
    console.log(x);
    console.log(y);
  }
}
```
### in操作符：判断对象中是否有指定的属性
```TypeScript
type Fish = { swim: () => void };
type Bird = { fly: () => void };
type Human = { swim?: () => void; fly?: () => void };

function move(animal: Fish | Bird | Human) {
  if ("swim" in animal) {
    animal;//Fish|Human
  } else {
    animal;//bird/human
  }
}
```
{% asset_img in.jpg in操作符 %}
### instanceof
x instanceof Foo :检测 x的原型链 是否包含 Foo.prototype

### 控制流分析（类型推断）
### 类型判断：parameterName is Type
```TypeScript
type Fish = { swim: () => void };
type Bird = { fly: () => void };
declare function getSmallPet(): Fish | Bird;
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}
let pet = getSmallPet();
if (isFish(pet)) {
  pet.swim();
} else {
  pet.fly();
}
```
### 可区分联合类型
```TypeScript
interface Circle {
  kind: "circle";
  radius: number;
}
interface Square {
  kind: "square";
  sideLength: number;
}
type Shape = Circle | Square;
function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
  }
}
```

---
## Function
### 调用签名
原因：解决无法在函数类型表达式声明其他属性
写法：
```TypeScript
type DescribableFunction = {
  description: string;
  (someArg: number): boolean;
};
function doSomething(fn: DescribableFunction) {
  console.log(fn.description + " returned " + fn(6));
}
```
### 构造函数签名
```TypeScript
type SomeConstructor = {
  new (s: string): SomeObject;
};
function fn(ctor: SomeConstructor) {
  return new ctor("hello");
}
```
### Function的泛型
原因：处理函数输入和输出有关联的情况或者两个函数输入有某种关联关系
```TypeScript
function map<Input, Output>(arr: Input[], func: (arg: Input) => Output): Output[] {
  return arr.map(func);
}
// Parameter 'n' is of type 'string'
// 'parsed' is of type 'number[]'
const parsed = map(["1", "2", "3"], (n) => parseInt(n));
```
### 泛型的约束
- 使用extends
```TypeScript
function minimumLength<Type extends { length: number }>(
  obj: Type,
  minimum: number
): Type {
  if (obj.length >= minimum) {
    return obj;
  } else {
    return { length: minimum };//报错，原因是不能返回只返回符合约束的对象
  }
}
```

> Type '{ length: number; }' is not assignable to type 'Type'.
> '{ length: number; }' is assignable to the constraint of type 'Type', 
> but 'Type' could be instantiated with a different subtype of constraint '{ length: number; }'.
### 可选参数
使用 `name?:type`
### 函数重载
作用：需要调用不同参数个数和类型的函数实现同一个目的
```TypeScript
function makeDate(timestamp: number): Date;
function makeDate(m: number, d: string): Date;
function makeDate(m: number, d: number, y: number): Date;
function makeDate(mOrTimestamp: number, d?: number|string, y?: number): Date {
  if (d !== undefined && y !== undefined) {
    return new Date(y, mOrTimestamp, d);
  } else {
    return new Date(mOrTimestamp);
  }
}
const d1 = makeDate(12345678);
const d2 = makeDate(5, 5, 5);
const d3 = makeDate(1,'3');
```
### 剩余参数
使用 `...变量名` 表示
### 返回类型为void
`type vf = () => void`
- 此时并不强制只返回void,也可以返回其他类型值，但是ts会推论为void
- 但是直接 `function A():void` 返回其他值的时候会报错

---
- 只读属性 readOnly 
`interface SomeType {
  readonly prop: string;
}`
- 可选属性
```TypeScript
interface PaintOptions {
  shape: Shape;
  xPos?: number;
  yPos?: number;
}`
```
- 索引签名:字典
```TypeScript
interface StringArray {
  [index: number]: string;
}
```