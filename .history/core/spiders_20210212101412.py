# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Spider:
    module = None

    def __init__(self, module):
        self.module = module

    def load(self, url):
        return self.load_by_params(url, None)

    def load_by_params(self, url, params):
        try:
            self.module.url = url
            response = requests.get(url, params=params)
            response.encode = 'utf-8'
            self._html = response.text
        except Exception as e:
            print('Error: %s' % e)
