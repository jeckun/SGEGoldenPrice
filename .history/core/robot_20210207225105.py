# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
import time
import datetime


class BaseRobot(object):
    @staticmethod
    def run():
        # 加载页面
        # 检查交易状态
        # 如果在交易中，或者即将开盘，就循环获取最近10分钟的最新交易价格和交易量
        # 如果不在交易中，获取最近5天的交易数据

    @staticmethod
    def load():
