# -*- coding: utf-8 -*-


class Robot(object):
    isSavetoDB = False
    quote_time = ''

    def __init__(self, url):
        self._url = url
        self._spider = SpiderSelenium()
        # self.isSavetoDB = False

    def run(self):
        # 加载页面
        self.load(self._url)
        while True:
            self.check()
            time.sleep(3)
