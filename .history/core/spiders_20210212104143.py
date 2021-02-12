# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Module:
    __hostname__ = ''

    @property
    def hostname(self):
        return self.__hostname__


class Spider:
    module = Module()
    parser = None

    def __init__(self, module):
        self.module = module

    def load(self, url=None):
        if url:
            return self.load_by_params(url, None)
        else:
            return self.load_by_params(self.module.url, None)

    def load_by_params(self, url, params, headers=None, cookies=None):
        try:
            self.module.url = url
            if params:
                response = requests.get(url, params=params)
            else:
                response = requests.get(url)
            response.encode = 'utf-8'
            html_doc = response.text
            self.parser = BeautifulSoup(html_doc, 'lxml')
            print('网页：%s 加载成功.' % self.module.hostname)
        except Exception as e:
            print('Error: %s' % e)
