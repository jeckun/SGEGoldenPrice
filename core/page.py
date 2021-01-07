# -*- coding: utf-8 -*-

from core import SpiderLxml


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
            xpath=col_xpath, fun=self.column)

        lines = {}
        columns = []
        for i in range(1, len(item)):
            line_xpath = row_xpath % i
            ls = self._spider.get_element_by_xpath(
                xpath=line_xpath, fun=self.column)
            if ls == [] or item[0] == ls[0]:
                columns = ls
                continue
            for x in range(0, len(columns)):
                lines[columns[x]] = ls[x]
            if lines != {}:
                table.append(lines)
        return table

    def column(self, elements):
        cl = []
        for item in elements:
            cl.append(item.text.replace('\r', '').replace(
                '\t', '').replace('\n', '').replace(',', ''))
        return cl
