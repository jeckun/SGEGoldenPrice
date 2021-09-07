# -*- coding: utf-8 -*-

import sys






def main(args):
    print('数据采集工具2.0')
    print('数据来源：上海黄金交易所')
    print('网络地址：https://www.sge.com.cn/')
    print('本次任务：采集最近%s的数据。' % args[0]) 

if __name__ == "__main__":
    main(sys.argv[1:])