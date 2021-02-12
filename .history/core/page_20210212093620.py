# -*- coding: utf-8 -*-
import time
from core import SpiderLxml
from datetime import datetime
from core.db import Trade
from lib.os import save_log, exists, join, save_list_by_json, read_list_from_json
from config import Table_xpath, col_xpath, row_xpath


class BaseWeb(object):
    _url = ''
    _spider = None
    _list = []
    _table = []
    _session = None

    def __init__(self, url=None):
        self._url = url
        self._session = Trade().session
        pass

    def __repr__(self):
        return "<BaseWeb(Host=%s)>" % self._url

    @property
    def list(self):
        return self._list

    @property
    def table(self):
        return self._table

    def cache(self, filename, content):
        save_list_by_json(filename, content)

    def load_by_params(self, url, params=None):
        self._url = url
        self._params = params
        self._spider = SpiderLxml()
        self._spider.open(url, params=params)
        time.sleep(3)

    def get_list_by_xpath(self, xpath, function):
        lst = []
        lst += self._spider.get_element_by_xpath(
            xpath=xpath, fun=function)
        return lst.copy()

    def get_table_by_xpath(self, xpath, function):
        # 获取页面中表格数据
        table = []
        item = self._spider.get_element_by_xpath(
            xpath=col_xpath, fun=function)

        lines = {}
        columns = []
        for i in range(1, len(item)):
            line_xpath = row_xpath % i
            ls = self._spider.get_element_by_xpath(
                xpath=line_xpath, fun=function)
            if ls == [] or item[0] == ls[0]:
                columns = ls
                continue
            for x in range(0, len(columns)):
                lines[columns[x]] = ls[x]
            if lines != {}:
                table.append(lines.copy())
        return table.copy()


class PageList(BaseWeb):

    def download(self, number, xpath):
        self.download_trade(1, number, xpath)

    def download_trade(self, star, end, xpath):

        print('获取下载列表...')

        # 获取下载列表
        self.get_glod_quotation_list(star, end, xpath)

        print('下载 %d 天交易数据' % len(self.list))

        for item in self.list:
            print('下载交易记录： %s  \t\t\t 网址：' % item[0], item[1])
            # 判断是否已经下载
            filename = join('data', 'cache', item[0]+'.txt')
            if not exists(filename):
                print('下载 %s 日数据\n' % item[0])
                self.load_by_params(item[1])
                tb = self.get_daily_glod_quotation_price(Table_xpath, item[0])
                self.cache(filename=filename, content=tb)
            else:
                print('从缓存加载 %s 日数据\n' % item[0])
                self._table.append(read_list_from_json(filename))

        self.save_to_db()
        # 下载没有下载的数据，并且保存到数据库

    def get_glod_quotation_list(self, star, end, xpath):
        for i in range(star, end + 1):
            params = {'p': '%d' % i}
            print('正在读取第 %d 页.' % i)
            self.load_by_params(self._url, params=params)
            self._list += self.get_list_by_xpath(
                xpath=xpath, function=self.analysis_list)

    def analysis_list(self, elements):
        # 解析每日交易列表
        ls = []
        for i in range(0, len(elements), 2):
            ls.append([elements[i+1].text, self._spider.host +
                       elements[i].attrib['href']])
        return ls.copy()

    def get_daily_glod_quotation_price(self, xpath, day):
        # 获取每天各类合约的上海黄金交易数据
        item = {}
        tb = []
        item['交易日期'] = day

        tb = self.get_table_by_xpath(xpath, function=self.text)
        for i in tb:
            i.update(item)
        self._table.append(tb)
        return tb.copy()

    def text(self, elements):
        cl = []
        for item in elements:
            cl.append(item.text.replace('\r', '').replace(
                '\t', '').replace('\n', '').replace(',', ''))
        return cl

    def convert_float(self, item):
        val = str(item).replace('%', '').replace(',', '')
        return 0.0 if len(val) == 0 else float(val)

    def trade_exists(self, code, trade_date):
        # 判断交易记录是否已经存在
        our_trade = self._session.query(
            Trade).filter_by(trans_date=trade_date).filter_by(code=code).first()
        if our_trade:
            return True
        else:
            return False

    def save_to_db(self):
        for dt in self._table:
            try:
                for line in dt:
                    try:
                        if not self.trade_exists(line['合约'], line['交易日期']):
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
                                        turnover=self.convert_float(self.convert_float(
                                            line['成交金额'])),
                                        hold=0.0 if line[hold_tag] == '-' or line[hold_tag] == '' else self.convert_float(
                                            line[hold_tag]),
                                        settlement=str(
                                            line['交收方向'] if line['交易日期'] <= '2014-09-04' else '').replace('-', ''),
                                        settlement_volume=self.convert_float(
                                            line['交收量'])
                                        )
                            self._session.add(row)
                            print('保存到数据库:', line['交易日期'], line['合约'])
                        else:
                            print('已有数据，跳过。 日期：%s  合约：%s' %
                                  (line['交易日期'], line['合约']))
                    except Exception as e:
                        print('error :', e)
                        save_log(e.args[0])
                self._session.commit()
            except Exception as e:
                print('error :', e)
                save_log(e.args[0])
