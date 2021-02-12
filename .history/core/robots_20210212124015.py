# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from config import sge_xpath


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
                self.module.get_catalog_list(sge_xpath['catalog_list'])
            elif task == 'get_table':
                self.module.get_table(
                    sge_xpath['tbody'], sge_xpath['row'], sge_xpath['col'])
            elif task == 'save_to_db':
                pass
