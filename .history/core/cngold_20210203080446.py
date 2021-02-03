# -*- coding: utf-8 -*-
from selenium import webdriver
from datetime import datetime
from core import SpiderSelenium
from core.db import TimeSharingChart, session
import pyautogui
import time
import re


def execut_get_all_price(url, days):
    # 获取收盘后
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

    # 全屏展示
    dr.find_element_by_class_name("kke_cfg_fullscreen").click()

    width, height = pyautogui.size()
    print("分辨率", width, height)

    pyautogui.click(150, 170)
    pyautogui.click(1630, 500)

    x, y = pyautogui.position()
    print("当前鼠标位置", x, y)

    # 获取每天每分钟的行情数据
    for i in range(780*days):
        pyautogui.typewrite(["left"], 0.25)
        a += get_price(dr)
        if a > 100:            # 判断遇到重复100次时自动退出
            break
        time.sleep(0.1)


def text(element):
    return element.text


def cutDate(element):
    date = element.text[:10].replace('/', '-')
    time = element.text[12:]+":01"
    week = element.text[11:12]
    return date + " " + time


def cutupOrdown(element):
    ls = re.split('[()]', element)
    return ls[:2]


def get_price(dr):
    price = {}
    price.update(
        {"name": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/thead/tr[1]/th/span', text)})
    price.update(
        {"time": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[1]/th/span', cutDate)})
    price.update(
        {"price": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[2]/td/span', text)})
    price.update(
        {"av_price": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[3]/td/span', text)})
    price.update(
        {"upOrdown": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[4]/td/span', text)})
    price.update(
        {"deal": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[3]/div/div[5]/table/tbody/tr[5]/td/span', text)})
    print(price["time"], price["name"], price["price"],
          price["av_price"], price["upOrdown"], price["deal"])
    return save_to_db(price)


def convert_float(item):
    val = str(item).replace('%', '').replace(',', '').replace('手', '')
    return 0.0 if len(val) == 0 else float(val)


def exists(table, code, trade_date):
    # 判断交易记录是否已经存在
    our_trade = session.query(
        table).filter_by(trans_date=trade_date).filter_by(code=code).first()
    if our_trade:
        return True
    else:
        return False


def save_to_db(line):
    if not exists(TimeSharingChart, line['name'], datetime.strptime(
            line['time'], "%Y-%m-%d %H:%M:%S")):
        row = TimeSharingChart(
            code=line['name'],
            trans_date=datetime.strptime(
                line['time'], "%Y-%m-%d %H:%M:%S"),
            price=convert_float(line['price']),
            VWAP=convert_float(line['av_price']),
            spread=convert_float(cutupOrdown(line['upOrdown'])[0]),
            extent=convert_float(cutupOrdown(line['upOrdown'])[1]) / 100,
            volume=convert_float(line['deal'])
        )
        session.add(row)
        session.commit()
        return 0
    else:
        print('已经存在跳过导入：', line['name'], line['time'])
        return 1


def execut_download_price(url):
    # 获取实时行情数据
    dr = SpiderSelenium()
    dr.open(url)
    dr.max_window()

    dr.find_element_by_class_name("b_controll").click()
    dr.find_element_by_xpath(
        "//*[@class='calendar']/div[1]/h3[2]").click()

    price = {}
    price["quote_time"] = dr.find_element_by_id("quote_time").text

    while dr.find_element_by_id("status_em").text != "交易中":
        try:
            if price["quote_time"] == dr.find_element_by_id("quote_time", text):
                price.update({"name": dr.find_element_by_xpath(
                    '//*[@id="realtime_showname"]/span', text)})
                price.update(
                    {"quote_time": dr.find_element_by_id("quote_time", text)})
                price.update(
                    {"now_price": dr.find_element_by_id("now_price", text)})
                price.update(
                    {"average_price": dr.find_element_by_xpath('//*[@id="tkChart_Hq"]/div[2]/span[4]', text)})
                price.update(
                    {"upordown": dr.find_element_by_id("upOrDown_div", text)})
                price.update(
                    {"buy_price": dr.find_element_by_id("buy_price", text)})
                price.update(
                    {"sell_price": dr.find_element_by_id("sell_price", text)})
                price.update(
                    {"open_price": dr.find_element_by_id("open_price", text)})
                price.update(
                    {"close_price": dr.find_element_by_id("close_price", text)})
                price.update(
                    {"high_price": dr.find_element_by_id("high_price", text)})
                price.update(
                    {"low_price": dr.find_element_by_id("low_price", text)})

                price.update({
                    "five_leval": dr.find_element_by_class_name("five_leval", text)
                })

                if len(price["five_leval"].text) > 0:
                    price.update({
                        "five_leval":
                        [item.split(' ')
                         for item in price["five_leval"].text.split('\n')]
                    })
                else:
                    price.update({"five_leval": []})

                print(price["quote_time"],  price["name"],
                      "最新价格", price["now_price"],
                      "均价", price["average_price"],
                      price["five_leval"][4],
                      price["five_leval"][5])
        except Exception as e:
            print(e)
        time.sleep(1)
