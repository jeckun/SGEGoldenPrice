# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

from .spiders import Module
from .robots import Robot
from config import sge_xpath


class Sge(Module):
    __hostname__ = '上海黄金交易所'
    trade_record = {}

    # 执行脚本
    def run(self, robot: Robot, **kwargs):
        self.robot = robot
        for task in robot.script:
            if task == 'get_catalog_list':
                self.get_catalog_list(
                    sge_xpath['catalog_list'], sge_xpath['catalog_list_span'], **kwargs)
            elif task == 'get_table':
                self.get_table(
                    sge_xpath['tbody'], sge_xpath['row'], sge_xpath['col'])
            elif task == 'save_to_db':
                self.save_to_db(robot.module.trade_record)
                pass

    def get_catalog_list(self, a_path, text_path, **kwargs):
        # 获取每日行情列表
        for i in range(kwargs['star'], kwargs['end'] + 1):
            params = {'p': '%d' % i}
            print('正在读取第 %d 页.' % i)
            self.robot.spider.load_by_params(self.url, params=params)
            a = self.parser.select(a_path)
            t = self.parser.select(text_path)
            self.catalog_list += list(zip(list(i.text for i in t),
                                          list(self.host + i.get('href') for i in a)))

    def get_table(self, tbody, row, col):
        # 获取每日行情各类合约交易数据
        for day in self.catalog_list:
            print('收集 %s 日的交易数据.' % day[0])
            self.robot.spider.load(day[1])
            tbody = self.parser.find('')
            print('加载成功')

    def save_to_db(self, data):
        print('保存数据')
