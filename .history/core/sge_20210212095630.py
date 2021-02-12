# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

class Sge:
    __hostname__ = '上海黄金交易所'
    _url = ''
    _params = None
    _catalog_list = []
    _trade_record = {}
