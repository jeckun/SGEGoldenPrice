# -*- coding: utf-8 -*-

import sys
from lib.db import Engine
from Sge.sge import Sge
from core import Spider, Robot
from config import URL, sge_script


def main(args):
    # 根据命令行参数分情况执行
    try:
        sg = Sge(URL['sge'], Engine)
        sp = Spider(sg)
        rt = Robot(spider=sp, script=sge_script)
        if len(args) == 2:
            rt.run(star=int(args[0]), end=int(args[1]))
        elif len(args) == 1:
            rt.run(star=1, end=int(args[0]))
        elif len(args) == 1 and args[0] == 'robot':
            # 获取日线记录
            # url = "https://quote.cngold.org/gjs/jjs_hjtd.html"
            # rt = Robot(url)
            # rt.run()
            # execut_get_all_price(url, 5)
            # execut_download_price(url)
        elif len(args) == 1 and args[0] == 'export':
            # 获取日线记录
            rt.export_json
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
