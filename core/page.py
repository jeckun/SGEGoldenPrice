# -*- coding: utf-8 -*-

from core import SpiderLxml


# 这个类用来解析网页
class PageList(object):
    _url = ''
    _params = None
    _spider = None
    _list = []
    _table = {}

    def __init__(self, url):
        self._url = url
        pass

    @property
    def list(self):
        return self._list

    def get_list(self, number, xpath):
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

    def get_table_xpath(self, col, row):
        column = self._spider.get_element_by_xpath(
            xpath=col, fun=self.column)
        print(len(column))
        rows = []
        for i in range(1, len(column)):
            xpath = row % i
            rows += self._spider.get_element_by_xpath(
                xpath=xpath, fun=self.column)

    def column(self, elements):
        cl = []
        for item in elements:
            cl.append(item.text.replace('\r', '').replace(
                '\t', '').replace('\n', ''))
        return cl
