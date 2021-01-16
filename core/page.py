# -*- coding: utf-8 -*-
import time
from core import SpiderLxml
from datetime import datetime
from core.db import Trade, session


# 这个类用来解析网页
class PageList(object):
    _url = ''
    _params = None
    _spider = None
    _list = []
    _table = []

    def __init__(self, url):
        self._url = url
        pass

    @property
    def list(self):
        return self._list

    def get_glod_quotation_list(self, number, xpath):
        for i in range(1, number + 1):
            params = {'p': '%d' % i}
            self.load(self._url, params=params)
            self.get_list_xpath(xpath=xpath)

    def load(self, url, params=None):
        self._url = url
        self._params = params
        self._spider = SpiderLxml()
        self._spider.open(url, params=params)
        time.sleep(3)

    def get_list_xpath(self, xpath):
        self._list += self._spider.get_element_by_xpath(
            xpath=xpath, fun=self.analysis_list)
        return self._list

    def analysis_list(self, elements):
        # 解析每日交易列表
        ls = []
        for i in range(0, len(elements), 2):
            ls.append([elements[i+1].text, self._spider.host +
                       elements[i].attrib['href']])
        return ls

    def get_daily_glod_quotation_price(self, xpath, day):
        # 获取每天各类合约的上海黄金交易数据
        item = {}
        item['交易日期'] = day
        tb = self.get_table_xpath(xpath)
        for i in tb:
            i.update(item)
        self._table.append(tb)

    def get_table_xpath(self, xpath):
        table = []
        col_xpath = xpath + '/tr/td[1]'
        row_xpath = xpath + '/tr[%d]/td'
        item = self._spider.get_element_by_xpath(
            xpath=col_xpath, fun=self.text)

        lines = {}
        columns = []
        for i in range(1, len(item)):
            line_xpath = row_xpath % i
            ls = self._spider.get_element_by_xpath(
                xpath=line_xpath, fun=self.text)
            if ls == [] or item[0] == ls[0]:
                columns = ls
                continue
            for x in range(0, len(columns)):
                lines[columns[x]] = ls[x]
            if lines != {}:
                table.append(lines)
        return table

    def text(self, elements):
        cl = []
        for item in elements:
            cl.append(item.text.replace('\r', '').replace(
                '\t', '').replace('\n', '').replace(',', ''))
        return cl

    def save_to_db(self):
        for dt in self._table:
            for line in dt:
                row = Trade(code=line['合约'],
                            open_price=float(0.0 if (
                                len(line['开盘价']) == 0) else line['开盘价']),
                            high_price=float(0.0 if (
                                len(line['最高价']) == 0) else line['最高价']),
                            low_price=float(0.0 if (
                                len(line['最低价']) == 0) else line['最低价']),
                            close_price=float(0.0 if (
                                len(line['收盘价']) == 0) else line['收盘价']),
                            spread=float(0.0 if (
                                len(line['涨跌（元）']) == 0) else line['涨跌（元）']),
                            extent=float(0.0 if len(line['涨跌幅']) == 0 else line['涨跌幅'].replace(
                                '%', '')) / 100,
                            VWAP=float(0.0 if (
                                len(line['加权平均价']) == 0) else line['加权平均价']),
                            volume=float(0.0 if (
                                len(line['成交量']) == 0) else line['成交量']),
                            turnover=float(0.0 if (
                                len(line['成交金额']) == 0) else line['成交金额']),
                            hold=float(0.0 if (
                                len(line['市场持仓']) == 0) else line['市场持仓']),
                            settlement=line['交收方向'],
                            settlement_volume=float(0.0 if (
                                len(line['交收量']) == 0) else line['交收量']),
                            trans_date=datetime.strptime(
                                line['交易日期'], "%Y-%m-%d")
                            )
                print(row)
                session.add(row)
            session.commit()
