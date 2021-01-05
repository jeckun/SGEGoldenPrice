# shGlodPrice

*采用爬虫每天自动获取每天上海黄金交易所各类合约的交易价格*

## 数据来源

数据来自上海黄金交易所[每日行情](https://www.sge.com.cn/sjzx/mrhqsj?p=1)
计划每天早盘和午盘收盘后更新。

## 目录结构

```
shGlodPrice                 
|__ bin                  编译后代码
|__ conf                 配置文件
|__ core
|  |__ Spider            爬虫类用来获取网页数据
|  |__ TradeData         数据处理类用来格式化获得的交易数据
|__ db                   数据存放目录
|__ lib                  公共库
|__ log                  同步日志
|__ manager.py           程序入口
```


## 待解决问题

由于上海黄金交易所每日行情的数据格式在不同时期会有所不同，所以这一块需要特殊处理。


## Api接口

计划写一个API接口，待上诉问题解决以后就开始。
