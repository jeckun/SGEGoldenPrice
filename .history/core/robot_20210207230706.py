# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
import time
import datetime


class Robot(object):
    def __init__(self, url):
        self._url = url
        self._spider = SpiderSelenium()

    def run(self):
        # 加载页面
        self.load(self._url)
        # 检查交易状态
        if get_state == "闭市":
            # 如果不在交易中，获取最近5天的交易数据
            pass
        else:
            # 如果在交易中，或者即将开盘，就循环获取最近10分钟的最新交易价格和交易量
            pass

    def refresh(self):
        self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/').click()

    def load(self, url):
        self._spider.open(url)
        self._spider.max_window()

        # 关闭弹幕
        self._spider.find_element_by_class_name("b_controll").click()

        # 关闭广告条
        elements = self._spider.find_elements_by_class_name("close")
        for el in elements:
            if el.tag_name == 'img':
                el.click()

    def get_state(self):
        return self._spider.find_element_by_id("status_em", self.text)

    @staticmethod
    def text(element):
        return element.text
