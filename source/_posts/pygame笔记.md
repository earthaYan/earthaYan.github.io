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
