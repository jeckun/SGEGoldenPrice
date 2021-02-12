# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

from .spiders import Module
from .robots import Robot
from config import sge_xpath
from lib.base import text, cache, exists, join, load_by_json, save_to_json


class Sge(Module):
    __hostname__ = '上海黄金交易所'
    trade_record = []

    # 执行脚本
    def run(self, robot: Robot, **kwargs):
        self.robot = robot
        for task in robot.script:
            if task == 'get_catalog_list':
                self.get_catalog_list(
                    sge_xpath['catalog_list'], sge_xpath['catalog_list_span'], **kwargs)
            elif task == 'get_table':
                self.get_days_data(sge_xpath['row'], sge_xpath['col'])
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

    def get_days_data(self, row, col):
        # 获取每日行情各类合约交易数据
        for day in self.catalog_list:
            print('收集 %s 日的交易数据.' % day[0])
            # 判断交易数据是否已经下载，如果已经下载就从缓存加载
            filename = join('data', 'cache', day[0]+'.txt')
            if exists(filename):
                self.trade_record.append(load_by_json(filename))
                continue
            # 没有下载过的交易数据，开始下载
            self.robot.spider.load(day[1])
            self.trade_record.append(
                self.analysis_table_data(day[0], row, col))

    def analysis_table_data(self, day, row, col):
        # 将网页中表格数据转换为字典集合
        data = []
        rows = self.parser.select(col)
        for i in range(1, len(rows)+1):
            r = row % i
            item = self.parser.select(r)
            if i == 1:
                fields = list(text(i.text) for i in item)
                fields.append('交易日期')
                continue
            else:
                rst = list(text(i.text) for i in item)
                rst.append(day)
                data.append(dict(zip(fields, rst)))
        return data.copy()

    def save_to_db(self, data):
        print('保存数据')
