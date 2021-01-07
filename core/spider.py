# -*- coding: utf-8 -*-


import requests
from lxml import etree
from urllib.parse import urlparse


class BaseSpider(object):
    _url = ''
    _html = None
    _host = ''

    def __init__(self):
        pass

    def open(self, url, headers=None, cookies=None, params=None):
        self._url = url
        ul = urlparse(self._url)
        if ul.scheme and ul.hostname:
            self._host = ul.scheme + '://' + ul.hostname
        try:
            self._url = url
            response = requests.get(url, params=params)
            response.encode = 'utf-8'
            self._html = response.text
        except Exception as e:
            print('Error: %s' % e)

    @property
    def host(self):
        return self._host


class SpiderLxml(BaseSpider):
    def open(self, url, headers=None, cookies=None, params=None):
        try:
            super(SpiderLxml, self).open(url, headers, cookies, params)
            self._html = etree.HTML(self._html)
        except Exception as e:
            print('Error: %s' % e)

    def get_element_by_xpath(self, xpath, fun):
        try:
            # return fun(self._html.xpath(xpath))
            elements = self._html.xpath(xpath)
            return fun(elements)
        except Exception as e:
            print('Error: %s' % e)

    def get_element(self, xpath):
        return self._html.xpath(xpath)
