# -*- coding: utf-8 -*-
import sys
from core import PageList
from core.webdriver import execut_download_price, execut_get_all_price
from config import URL, Catalog_List


def main(args):

    star = 1
    end = 1

    try:
        if len(args) == 2:
            star = int(args[0])
            end = int(args[1])
        elif len(args) == 1 and args[0] == 'today':
            # 获取日线记录
            url = "https://quote.cngold.org/gjs/jjs_hjtd.html"
            execut_get_all_price(url)
            # execut_download_price(url)
        elif len(args) == 1:
            end = int(args[0])
        else:
            pass
    except Exception as e:
        print('Error: %s' % e.args)
        sys.exit(2)

    pg = PageList(URL)
    pg.download_trade(star=star, end=end, xpath=Catalog_List)
    # pg.download(number=number, xpath=Catalog_List)


if __name__ == "__main__":

    main(sys.argv[1:])
