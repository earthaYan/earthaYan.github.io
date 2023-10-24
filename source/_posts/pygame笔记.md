---
title: pygame笔记
tags: [Python, pygame, 游戏开发]
categories: Python
---

## 如何在本地阅读 pygame 文档

执行`python -m pygame.docs`

## python 适合哪些游戏开发

游戏=游戏引擎+游戏逻辑
过去：引擎（汇编语言）+逻辑（c 语言）
现在：引擎（c 语言）+ 逻辑（更高级的脚本语言）
pygame:

- 适合 2D 游戏开发
- 可以跨平台运行

## 导入和初始化

- `import pygame`：导入 pygame 包，里面包含所有可用的模块
- `pygame.init()`：初始化导入的所有模块
- `pygame.display.set_mode((1280, 720))`：设置游戏窗口大小并新建游戏的图形窗口
  > 创建了一个新的 Surface 对象代表实际展示的图形化窗口
- `img=pygame.image.load("intro_ball.gif")`：加载图片
- `img.get_react()`：工具对象类型`Rect`,代表 1 块矩形区域
- `ballrect = ballrect.move([2,2])`：移动图像 ballrect
- `screen.fill(black)`：清空屏幕
  > 电脑的动画是一系列的单图实现的，它们依次展示，让人视觉上是移动的。如果不使用 fill()方法，视觉上就会是运动轨迹
  > {%asset_img no_fill.png%}
- `screen.blit(sourceImg, Distination,area=None,)`：将图片绘制到另一个图像或者屏幕上
- `pygame.display.flip()`：更新屏幕展示

### 超出图形化窗口边界成处理

```py
if ballrect.left < 0 or ballrect.right > width:
    speed[0] = -speed[0]
if ballrect.top < 0 or ballrect.bottom > height:
    speed[1] = -speed[1]
```

## 如何使得游戏循环运行

FPS:游戏画面每秒更新的次数

```py
import pygame
# pygame设置
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT 事件意味着用户点击X关闭了弹窗
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 使用一种颜色填充屏幕，清除上一帧留下的所有东西
    screen.fill("purple")
    # 此处渲染游戏
    # ...
    # flip() 将成果展示在屏幕上
    pygame.display.flip()
    clock.tick(60)  # 限制 FPS 为 60
pygame.quit()
```

## pygame 移动游戏元素

```py
import pygame


pygame.init()
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
running=True
dt=0

player_pos=pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    screen.fill("purple")
    # 游戏代码==========================================
    pygame.draw.circle(screen,"red",player_pos,40)
    keys=pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y-= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y+= 300 * dt
    if keys[pygame.K_a]:
        player_pos.x-=300*dt
    if keys[pygame.K_d]:
        player_pos.x+=300*dt
           # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # 两个连续帧之间的时间差（秒）
    dt = clock.tick(60)
    pygame.display.flip()
pygame.quit()
```

## pygame 如何处理文件系统路径

TODO

## pygame.display.update() VS pygame.display.flip()

相同点：两者都是用于更新屏幕显示的函数
区别：

- `pygame.display.update()`：根据需要更新指定的区域或整个屏幕。它接受一个可选的参数，该参数是一个矩形列表，表示要更新的区域。如果不提供参数，它将更新整个屏幕。这个函数的优点是可以选择性地更新屏幕的特定区域，从而减少更新帧的计算量，提高性能。

- `pygame.display.flip()`：将当前内存中的所有改变刷新到屏幕上。它没有任何参数，每次调用它都会更新整个屏幕。这个函数的优点是简单易用，适用于大多数情况下。

## blit()

语法：`target_surface.blit(source_surface, position)`
作用：将图像（Surface 对象）绘制到其他 Surface 上的函数
示例代码

```py
img=pygame.image.load('../pic/yellow.png')
rect=img.get_rect()
rect.center=(400,300)
screen.blit(img,rect)
```

## 移动对象

### move_ip()

语法：`rect.move_ip(dx, dy)`

> dx 和 dy 分别代表 x、y 轴上的偏移量，y 方向上 `up` 为-1，x 方向上 `right` 为 1

作用：移动图像或矩形的位置。是在 Rect 对象上调用的方法，而不是直接在 Surface 上使用的。直接修改原始对象的位置
示例代码

```py
pressed=pygame.key.get_pressed()
if pressed[K_LEFT]:
    rect.move_ip(-1,0)
elif pressed[K_RIGHT]:
    rect.move_ip(1,0)
elif pressed[K_UP]:
    rect.move_ip(0,-1)
elif pressed[K_DOWN]:
    rect.move_ip(0,1)
```

### move()

语法：`rect.move(dx, dy)`
作用：move() 方法返回一个新的矩形对象，而不直接修改原始对象。如果要保留原始矩形对象并获得移动后的副本，可以使用 move()

```py
pressed=pygame.key.get_pressed()
if pressed[K_LEFT]:
    rect=rect.move_ip(-1,0)
elif pressed[K_RIGHT]:
    rect=rect.move(1,0)
elif pressed[K_UP]:
    rect=rect.move(0,-1)
elif pressed[K_DOWN]:
    rect=rect.move_ip(0,1)
```

## scale()

语法：`scaled_surface = pygame.transform.scale(surface, size)`
作用：缩放图像或 Surface 的大小。它可以按照指定的比例因子来缩放图像，也可以根据给定的目标尺寸进行缩放。
参数：size 是一个元组，表示目标尺寸 (width, height)
示例代码：

```py
def loadImage(self):
    self.img=pygame.image.load(BLOCK_RES[self.blockType])
    self.img=pygame.transform.scale(self.img,(self.width,self.height))
```
