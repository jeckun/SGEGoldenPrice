# -*- coding:utf-8 -*-
import time
import datetime


class Robot(object):
    def __init__(self, spider=None, page=None, database=None):
        self._spider = spider
        self._page = page
        self._database = database
        pass

    @staticmethod
    def run():
        while True:
            ts = datetime.datetime.now()
            print('%s: ' % ts.strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1)
