# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from .sge import Sge


class Robot(object):
    def __init__(self, spider: Spider, module: Module):
        self.spider = spider
        self.module = module

    def run(self):
        # 加载页面
        self.load(self._url)
        while True:
            self.check()
            time.sleep(3)
