# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

from config import URL, Table_xpath, col_xpath, row_xpath


class Sge:
    __hostname__ = '上海黄金交易所'
    url = ''
    params = None
    catalog_list = []
    trade_record = {}
