# -*- coding: utf-8 -*-

# 从上海黄金交易所下载每日交易数据
# 网址：https://www.sge.com.cn/sjzx/mrhqsj?p=1

import time
from config import sge_xpath
from datetime import datetime
from core import Module, Robot
from Sge.db import Trade
from lib.base import text, cache, exists, join, load_by_json, save_to_json, save_log


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
                self.get_days_data(
                    sge_xpath['row'], sge_xpath['col'])
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
                                          list(self.domainname + i.get('href') for i in a)))

    def get_days_data(self, row, col):
        # 获取每日行情各类合约交易数据
        for day in self.catalog_list:
            print('收集 %s 日的交易数据.' % day[0])
            # 处理 2016-9-21 后列表中夹带文件下载的问题
            if not len(day[0]) == 10:
                continue
            # 判断交易数据是否已经下载，如果已经下载就从缓存加载
            filename = join('data', 'cache', day[0]+'.txt')
            if exists(filename):
                self.trade_record.append(load_by_json(filename))
                continue
            # 没有下载过的交易数据，开始下载
            self.robot.spider.load(day[1])
            data = self.analysis_table_data(day[0], row, col)
            cache(filename, data)               # 缓存交易数据
            self.trade_record.append(data)

    def analysis_table_data(self, day, row, col, **kwargs):
        # 将网页中表格数据转换为字典集合
        data = []
        try:
            rows = self.parser.select(col)
            if not rows:                                     # 处理 2016-12-16 模板改变的问题
                col = sge_xpath['col2']
                row = sge_xpath['row2']
                rows = self.parser.select(col)
            for i in range(1, len(rows)+1):
                r = row % i
                item = self.parser.select(r)
                if not item:                                 # 处理 2010-01-18 模板改变的问题
                    h = sge_xpath['row3']
                    r = h % i
                    item = self.parser.select(r)
                if i == 1:
                    fields = list(text(i.text)
                                  for i in item)             # 处理 &nbsp 字符串问题
                    # 处理 2016-12-22 至 2017-2-20 缺少合约字段名问题
                    if fields[0] == '' or fields[0] != '合约':
                        fields[0] = '合约'
                    if '涨跌' in fields:
                        fields[fields.index('涨跌')] = '涨跌（元）'
                    if '成交量（公斤）' in fields:
                        fields[fields.index('成交量（公斤）')] = '成交量'
                    if '成交金额（元)' in fields:
                        fields[fields.index('成交金额（元)')] = '成交金额'
                    fields.append('交易日期')
                    if '交收方向' not in fields:
                        fields.append('交收方向')
                    continue
                else:
                    rst = list(text(i.text) for i in item)
                    rst.append(day)
                    if len(rst) < len(fields):
                        rst.append('')
                    data.append(dict(zip(fields, rst)))
        except Exception as e:
            print('error :', e)
            save_log(day + ': ' + e.args[0])
        return data.copy()

    def convert_float(self, item):
        val = str(item).replace('%', '').replace(',', '')
        return 0.0 if len(val) == 0 else float(val)

    def save_to_db(self, data):
        # 将数据保存到数据库
        for dt in self.trade_record:
            eg = Trade()
            eg.connect(filename=join('data', 'foo.db'), echo=False)
            try:
                for line in dt:
                    try:
                        rst = eg.session.query(Trade).filter(Trade.code == line['合约'],
                                                             Trade.trans_date == line['交易日期'])
                        if not rst:
                            hold_tag = '市场持仓' if int(
                                line['交易日期'][:4]) > 2018 else '持仓量'
                            row = Trade(code=line['合约'],
                                        trans_date=datetime.strptime(
                                            line['交易日期'], "%Y-%m-%d"),
                                        open=self.convert_float(
                                            line['开盘价']),
                                        high=self.convert_float(
                                            line['最高价']),
                                        low=self.convert_float(
                                            line['最低价']),
                                        close=self.convert_float(
                                            line['收盘价']),
                                        spread=self.convert_float(
                                            line['涨跌（元）']),
                                        extent=self.convert_float(
                                            line['涨跌幅']) / 100,
                                        VWAP=self.convert_float(line['加权平均价']),
                                        volume=self.convert_float(line['成交量']),
                                        turnover=self.convert_float(
                                            line['成交金额']),
                                        hold=0.0 if line[hold_tag] == '-' or line[hold_tag] == '' else self.convert_float(
                                            line[hold_tag]),
                                        settlement=str(
                                            line['交收方向'] if line['交易日期'] <= '2014-09-04' else '').replace('-', ''),
                                        settlement_volume=self.convert_float(
                                            line['交收量'])
                                        )
                            eg.insert(row)
                            print('保存到数据库:', line['交易日期'], line['合约'])
                        else:
                            print('已有数据，跳过。 日期：%s  合约：%s' %
                                  (line['交易日期'], line['合约']))
                    except Exception as e:
                        print('error :', e)
                        save_log(line['交易日期'] + ': ' + e.args[0])
                        continue
            except Exception as e:
                print('error :', e)
                save_log(line['交易日期'] + ': ' + e.args[0])

    def export_json(self, **kwargs):
        # 将数据输出为json
        eg = Trade()
        eg.connect(filename=join('data', 'foo.db'), echo=False)
        rst = eg.session.query(Trade).filter(
            Trade.code == kwargs['code']).order_by(Trade.trans_date)

        def convert_time(date):
            timeArray = time.strptime(date.strftime(
                "%Y-%m-%d 08:00:00"), "%Y-%m-%d %H:%M:%S")
            return int(time.mktime(timeArray) * 1000)

        data = []
        for index, item in enumerate(rst):
            print(item.trans_date, item.code, item.open,
                  item.high, item.low, item.close, item.volume)
            data.append([convert_time(item.trans_date), item.open,
                         item.high, item.low, item.close, item.volume])
        filename = join('data', 'K_json.json')
        exp = {
            'code': 1,
            'msg': '操作成功',
            'data': data,
        }
        save_to_json(filename, exp)
