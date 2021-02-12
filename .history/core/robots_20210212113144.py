# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from ..config import sge_xpath


class Robot(object):
    def __init__(self, module: Module, script: list):
        self.spider = module.spider
        self.module = module
        self.script = script

    def run(self):
        for task in self.script:
            if task == 'load':
                self.spider.load()
            elif task == 'get_catalog_list':
                self.module.get_catalog_list(
                    catalog_list_xpath=sge_xpath['get_catalog_list'])
                pass
            elif task == 'get_table':
                pass
            elif task == 'save_to_db':
                pass
