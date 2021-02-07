# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
import time
import datetime


class Robot(object):
    def __init__(self, url):
        self._url = url

    @staticmethod
    def run():
        # 加载页面
        self.load()
        # 检查交易状态
        # 如果在交易中，或者即将开盘，就循环获取最近10分钟的最新交易价格和交易量
        # 如果不在交易中，获取最近5天的交易数据

    @staticmethod
    def load(url):
        dr = SpiderSelenium()
        dr.open(url)
        dr.max_window()

        # 关闭弹幕
        dr.find_element_by_class_name("b_controll").click()

        # 关闭广告条
        elements = dr.find_elements_by_class_name("close")
        for el in elements:
            if el.tag_name == 'img':
                el.click()
