# -*- coding: utf-8 -*-

import os
import sys
import getopt
from conf.config import CONFIG


def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'hv', ['version', 'help'])
        for arg in args:
            if arg == "update":
                print("开始更新数据")
            else:
                print("\nERROR: 错误的参数。\n\n请输入 -h 或者 --help 查看帮助文档。\n\n")

    except getopt.GetoptError:
        print('Error: 参数错误.')
        sys.exit(2)

    for op, value in opts:
        if op == '-h' or op == '--help':
            print('shGlodPrice 使用帮助')
        elif op == '-v' or op == '--version':
            print('shGlodPrice version: 1.0')
        else:
            print(value)


if __name__ == "__main__":
    main(sys.argv[1:])
