# -*- coding: utf-8 -*-
from .spiders import Spider, Module
from lib.db import Engine
from config import sge_xpath


class Robot(object):
    def __init__(self, spider: Spider, script: list):
        self.spider = spider
        self.module = spider.module
        self.script = script

    def run(self):
        self.module.run(self)
