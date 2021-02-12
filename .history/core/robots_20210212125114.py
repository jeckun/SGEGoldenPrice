# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from lib.db import Engine


class Robot(object):
    def __init__(self, spider: Spider, script: list):
        self.spider = spider
        self.module = spider.module
        self.script = script

    def run(self):
        self.module.run(self)
