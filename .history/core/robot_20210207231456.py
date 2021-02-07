# -*- coding: utf-8 -*-
from core.spider import SpiderSelenium
import time
import datetime
import pyautogui


class Robot(object):
    def __init__(self, url):
        self._url = url
        self._spider = SpiderSelenium()

    def run(self):
        # 加载页面
        self.load(self._url)
        # 检查交易状态
        if self.get_state() == "闭市":
            # 如果不在交易中，获取最近5天的交易数据
            self.refresh()
            # 全屏展示
            self._spider.find_element_by_class_name(
                "kke_cfg_fullscreen").click()
            # 显示最近5天的交易数据
            pyautogui.click(150, 170)
            # 获取每天每分钟的行情数据
            pyautogui.click(1630, 500)
            n = 0
            for i in range(780 * 5):
                n += self.get_price()
                if n > 1560:            # 检测到重复数据n次时自动退出
                    break
                pyautogui.typewrite(["left"], 0.25)
                n = 0
                time.sleep(0.1)
        else:
            # 如果在交易中，或者即将开盘，就循环获取最近10分钟的最新交易价格和交易量
            self.refresh()

    def refresh(self):
        self._spider.find_element_by_xpath('//*[@id="fr clearfix"]/a').click()

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

    def get_price(self):
        price = {}
        price.update(
            {"name": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/thead/tr[1]/th/span', text)})
        price.update(
            {"time": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[1]/th/span', cutDate)})
        price.update(
            {"price": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[2]/td/span', text)})
        price.update(
            {"av_price": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[3]/td/span', text)})
        price.update(
            {"upOrdown": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[4]/td/span', text)})
        price.update(
            {"deal": self._spider.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[5]/td/span', text)})
        print(price["time"], price["name"], price["price"],
              price["av_price"], price["upOrdown"], price["deal"])
        return save_to_db(price)
