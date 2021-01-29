# -*- coding: utf-8 -*-
from selenium import webdriver
import time

EXECUTABLE_PATH = "C:\Python\Selenium\ChromeDriver\chromedriver.exe"


class webEngine(object):
    def __init__(self):
        if EXECUTABLE_PATH:
            self.driver = webdriver.Chrome(EXECUTABLE_PATH)
        else:
            self.driver = webdriver.Chrome()

    def find_element_by_class_name(self, clsname):
        return self.driver.find_element_by_class_name(clsname)

    def find_element_by_id(self, id):
        return self.driver.find_element_by_id(id)

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def open(self, url):
        self.driver.get(url)

    def max_window(self):
        self.driver.maximize_window()

    def min_window(self):
        self.driver.minimize_window()

    def quit(self):
        self.driver.quit()


def execut_download_day_glod_price(url):
    dr = webEngine()
    dr.open(url)
    dr.max_window()

    dr.find_element_by_class_name("b_controll").click()

    price = {}
    price["quote_time"] = dr.find_element_by_id("quote_time").text

    while dr.find_element_by_id("status_em").text == "交易中":
        try:
            if price["quote_time"] != dr.find_element_by_id("quote_time").text:
                price.update({"name": dr.find_element_by_xpath(
                    '//*[@id="realtime_showname"]/span').text})
                price.update(
                    {"quote_time": dr.find_element_by_id("quote_time").text})
                price.update(
                    {"now_price": dr.find_element_by_id("now_price").text})
                price.update(
                    {"average_price": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[2]/span[4]').text})
                # price.update(
                #     {"deal": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[5]/td/span').text})
                price.update(
                    {"upordown": dr.find_element_by_id("upOrDown_div").text})
                price.update(
                    {"buy_price": dr.find_element_by_id("buy_price").text})
                price.update(
                    {"sell_price": dr.find_element_by_id("sell_price").text})
                price.update(
                    {"open_price": dr.find_element_by_id("open_price").text})
                price.update(
                    {"close_price": dr.find_element_by_id("close_price").text})
                price.update(
                    {"high_price": dr.find_element_by_id("high_price").text})
                price.update(
                    {"low_price": dr.find_element_by_id("low_price").text})
                print(price["name"], price["quote_time"],
                      price["now_price"], price["average_price"])
        except Exception as e:
            pass
        time.sleep(1)
