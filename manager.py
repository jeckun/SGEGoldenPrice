# -*- coding: utf-8 -*-

import os
from core import PageList
from config import BASE_PATH


if __name__ == "__main__":

    url = 'https://www.sge.com.cn/sjzx/mrhqsj'
    xpath = '''//div[@class="articleList border_ea mt30 mb30"]/ul/li/a |
               //div[@class="articleList border_ea mt30 mb30"]/ul/li/a/span[2]
    '''
    number = 35

    print('开始获取交易数据...')

    pg = PageList(url)
    pg.get_glod_quotation_list(number, xpath)

    print('下载 %d 天交易数据' % len(pg.list))

    xpath = '//table[@class="ke-zeroborder"]/tbody'

    for item in pg.list:
        print('下载交易记录： %s  \t\t\t 网址：' % item[0], item[1])
        pg.load(item[1])
        pg.get_daily_glod_quotation_price(xpath, item[0])

    pg.save_to_db()
