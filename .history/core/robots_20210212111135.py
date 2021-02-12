# -*- coding: utf-8 -*-
from .spiders import Spider, Module


class Robot(object):
    def __init__(self, spider: Spider, script: list):
        self.spider = spider
        self.module = spider.module
        self.script = script

    def run(self):
        for task in self.script:
            if task == 'load':
                self.spider.load()
            elif task == 'get_catalog_list':
                self.spider.get_catalog_list()
                pass
            elif task == 'get_table':
                pass
            elif task == 'save_to_db':
                pass
