# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Spider:
    module = None

    def __init__(self, module):
        self.module = module

    def load(self, url):
        pass

    def load_by_params(self, url, params=None):
        pass
