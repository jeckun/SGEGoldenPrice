# -*- coding: utf-8 -*-
from spiders import Spider, Module


class Robot(object):
    def __init__(self, spider: Spider, script: list):
        self.spider = spider
        self.module = spider.module
        self.script = script

    def run(self, **kwargs):
        self.module.run(self, **kwargs)
