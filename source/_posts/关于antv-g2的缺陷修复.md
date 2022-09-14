---
title: 关于antv/g2的缺陷修复
date: 2022-09-14 11:35:29
tags: ['图表','可视化']
categories: '缺陷修复'
---

## 缺陷链接
http://10.186.18.11/jira/browse/DMP-13821
## 问题复现和解决链接
https://codesandbox.io/s/tu-biao-xiu-fu-forked-1rqvwe?file=/src/index.data.ts

## 问题复现截图
{% asset_img error.png  测试提供截图 %}

## 定位问题
1. 通过查看接口返回，发现接口返回数据是符合要求的，那么问题就是出在前端了
2. 查看相关代码，发现是使用antv/g2的Chart实现的
3. 思考可能是传入数据的原因导致的：type轴值重复了
4. 有两种修复方法：
a. data里新增属性id，由type+device
b. 修改对应的type值，使它唯一，然后再通过formatter选项设置type轴的显示
5. 尝试了方法a，发现BarChart这个组件在多个父组件中被调用，如果使用该方案需要修改所有的父组件的data，所以最终选择方案2
## 修复前后代码对比
{% asset_img 修复1.jpg  BarChart组件 %}

{% asset_img 修复2.jpg  调用BarChart的父组件 %}

### 使用antv/g2实现一个条形图的过程

```TypeScript
  // 初始化图表
  const initChart = () => {
    chart.current = new Chart({
      container: `${titleKey}_chart`,
      autoFit: true,
      height: 295,
      padding: [30, 50, 30, 200],
    });
  };
```
```TypeScript
  // 绘制图表
  const drawChart = (data: IChartData[]) => {
    chart.current?.data(data);
    chart.current?.axis('type', {
      label: {
        autoEllipsis: true,
        style: {
          fill: currentThemeData.chart.linkColor,
          textAlign: 'left',
          fontSize: 14,
        },
        offsetX: -180,
        formatter: (val) => getIp(val),
      },
      tickLine: null,
      line: null,
      verticalLimitLength: 180,
    });
    chart.current?.axis('value', {
      grid: null,
      label: null,
    });
    chart.current?.tooltip(false);
    chart.current?.legend(false);
    chart.current?.coordinate('rect').transpose();
    if (percent) {
      chart.current
        ?.interval()
        .adjust('stack')
        .position('type*value')
        .color('barType*value', (barType: string, value: string[]) => {
          if (barType === barTypeEnum.background) {
            return '#ebedf0';
          } else {
            return getTypeColor(Number(value[1]));
          }
        })
        .size(15)
        .label('showValue*barType', (val, barType) => {
          if (barType === barTypeEnum.background) {
            return null;
          }
          if (titleKey === 'disk_top10') {
            return {
              content: (data) => {
                let deviceStr = data.device;
                if (deviceStr.length > 20) {
                  deviceStr = data.device.substr(0, 20) + '...';
                }
                return `${Number(val) > 20 ? val : '<20'}% ${deviceStr ?? ''}`;
              },
              offset: Number(val) < 20 ? 2 : 10,
              position: 'left',
              style: {
                fill: '#000',
              },
            };
          }
          return {
            content: val + '%',
            style: {
              fill: Number(val) < 20 ? '#000' : '#fff',
            },
            position: 'left',
          };
        });
    } else {
      chart.current
        ?.interval()
        .position('type*value')
        .size(15)
        .color(barColor)
        .label('value', {
          style: {
            fill: currentThemeData.chart.guideColor,
          },
          offset: 20,
        });
    }
  };
```

```TypeScript
  // 渲染图表
  React.useEffect(() => {
    initChart();
    chart.current?.on('axis-label:click', jumpAction);
    return () => {
      chart.current?.off('axis-label:click', jumpAction);
    };
  }, []);
  React.useEffect(() => {
    if (data?.length) {
      drawChart(data);
      chart.current?.render();
    }
    chart.current?.render(true);
  }, [data, currentThemeData]);
```
```TypeScript
  // 监听重绘
  React.useEffect(() => {
    const MutationObserver = window.MutationObserver;
    let observer: MutationObserver;
    const e = document.getElementById(`${titleKey}`);
    if (e) {
      observer = new MutationObserver(() => {
        chart.current?.forceFit();
        chart.current?.render(true);
        chart.current?.changeSize(e.scrollWidth, e.scrollHeight - 30);
      });
      observer.observe(e, {
        attributes: true,
        attributeFilter: ['style'],
        attributeOldValue: true,
      });
    }
    return () => {
      if (observer) {
        observer.disconnect();
      }
    };
  }, []); 
```

## 遗留问题
修复前getIp返回的是xxx.target,但是修复后只能通过xx.type去获取,原因不明
### 修复后使用target
{% asset_img 修复后target.jpg  修复后使用target %}
效果如下:
{% asset_img result.jpg  修复后使用target效果图 %}
