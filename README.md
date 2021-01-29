# Golden Spider

*这个爬虫可以获取上海黄金交易所各类合约的交易价格，只要将其放入定时任务就可以每天自动进行数据爬取。*

## 数据来源

数据来自上海黄金交易所[每日行情](https://www.sge.com.cn/sjzx/mrhqsj?p=1)

## 目录结构

```
shGlodPrice
|__ core                 主要代码
|__ lib
|__ manager.py           程序入口
```

## 使用方法

修改 manager.py 中的 number 值，这个表示需要爬取的列表页数，默认一页10天的数据。然后执行下面的命令即可。
```
$ python manager.py           # 默认下载最新一页的数据
$ python manager.py 10        # 带一个数字，表示下载最新10页数据
$ python manager.py 10 20     # 带两个数字，表示从几页开始下载到第几页，可以有选择性的下载历史某段时间的数据。
```

## 更新记录

- 2021-1-30 增加当天实时行情数据爬取。
- 2021-1-25 合并glodTrade分支，作为主要分支。
- 2021-1-22 开启glodTrade分支。
- 2021-1-19 完善shgoldprice命令行参数
- 2021-1-18 实现数据保存时去重与爬取效率提升
- 2021-1-17 实现上海黄金交易所每日交易数据爬取以及保存数据库

## Api接口

由于不想把这个小爬虫弄得太复杂，所以接口改为在另一个Django项目中实现。届时将开放免费的公开API接口供给大家使用。

## 其他

- 2014-09-04 日前无“交收方向”
- 2018-12-31 日前叫“持仓量”，之后叫“市场持仓”
