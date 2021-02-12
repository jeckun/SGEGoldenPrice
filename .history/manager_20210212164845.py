# -*- coding: utf-8 -*-

import sys
from lib.db import Engine
from Sge.sge import Sge
from core import Spider, Robot
from config import URL, sge_script


def main(args):

    star = 1
    end = 1

    try:
        if len(args) == 2:
            star = int(args[0])
            end = int(args[1])
            pg.download_trade(star=star, end=end, xpath=Catalog_List)
        elif len(args) == 1 and args[0] == 'robot':
            # 获取日线记录
            url = "https://quote.cngold.org/gjs/jjs_hjtd.html"
            rt = Robot(url)
            rt.run()
            # execut_get_all_price(url, 5)
            # execut_download_price(url)
        elif len(args) == 1:
            sg = Sge(URL, Engine)
            sp = Spider(sg)
            rt = Robot(spider=sp, script=sge_script)
            rt.run(star=1, end=args[0])
        else:
            # 用来清理垃圾数据
            # sql = "delete from timeSharing where id >= 3510 and id <= 3650;"
            # sql = "select * from timeSharing where id >= 3510 and id <= 3650;"
            # eg = sqliteEngine('data/foo.db')
            # eg.execut_sql(sql)
            pass
    except Exception as e:
        print('Error:', e)
        sys.exit(2)


if __name__ == "__main__":

    main(sys.argv[1:])
