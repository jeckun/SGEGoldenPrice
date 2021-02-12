# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Spider:
    parser = None

    def __init__(self, module):
        self.module = module

    def load(self, url=None, headers=None, cookies=None):
        if url:
            return self.load_by_params(url=url, params=None, headers=headers, cookies=cookies)
        else:
            return self.load_by_params(url=self.module.url, params=None, headers=headers, cookies=cookies)

    def load_by_params(self, url, params, headers=None, cookies=None):
        try:
            self.module.url = url
            if params:
                response = requests.get(
                    url, params=params, headers=headers, cookies=cookies)
            else:
                response = requests.get(url, headers=headers, cookies=cookies)
            response.encode = 'utf-8'
            html_doc = response.text
            self.parser = BeautifulSoup(html_doc, 'lxml')
            self.module.parser = self.parser
            print('网页：%s 加载成功.' % self.module.hostname)
        except Exception as e:
            print('Error: %s' % e)


class Module:
    __hostname__ = ''
    parser = None
    url = ''
    catalog_list = []

    def __init__(self, url):
        self.url = url

    @property
    def hostname(self):
        return self.__hostname__

    def get_catalog_list(self, xpath=None):
        print('获取下载列表', xpath)

    def get_table(self, tbody, row, col):
        print('')
