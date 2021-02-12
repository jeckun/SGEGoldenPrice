# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from lib.db import Engine


class Robot(object):
    def __init__(self, spider: Spider, script: list, database: Engine):
        self.spider = spider
        self.module = spider.module
        self.script = script
        self.database = database

    def run(self):
        self.module.run(self)
