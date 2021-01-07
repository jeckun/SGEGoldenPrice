# -*- coding: utf-8 -*-

import os
from core import PageList


if __name__ == "__main__":

    url = 'https://www.sge.com.cn/sjzx/mrhqsj'
    xpath = '''//div[@class="articleList border_ea mt30 mb30"]/ul/li/a |
               //div[@class="articleList border_ea mt30 mb30"]/ul/li/a/span[2]
    '''
    number = 1

    pg = PageList(url)
    pg.get_list(number, xpath)

    print('获取到 %d 天的交易数据：' % len(pg.list))

    col = '//table[@class="ke-zeroborder"]/tbody/tr/td[1]'
    row = '//table[@class="ke-zeroborder"]/tbody/tr[%d]/td'

    for item in pg.list:
        print(item[0], item[1])
        pg.load(item[1])
        pg.get_table_xpath(col, row)
