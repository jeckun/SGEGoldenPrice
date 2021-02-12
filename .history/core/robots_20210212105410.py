# -*- coding: utf-8 -*-
from .spiders import Spider, Module


class Robot(object):
    def __init__(self, spider: Spider, module: Module, script: list):
        self.spider = spider
        self.module = module
        self.script = script

    def run(self):
        # 加载页面
        self.spider.load()
