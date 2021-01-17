# -*- coding: UTF-8 -*-

import os
import json

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def join(*args):
    path = os.path.join(BASE_PATH)
    for item in args:
        path = os.path.join(path, item)
    return path


def exists(path):
    return os.path.exists(path)


def makdir(path):
    os.mkdir(path)


def save_to_file(filename, content, fun, overwrite=False):
    '''
    # 保存列表或者字典等集合内容到文件。
    # 默认不覆盖已有文件。
    # 需要提供解析函数fun，对列表或者字典内容解释为一行字符串。
    '''

    if os.path.exists(filename) and overwrite == False:
        print('WARNING: %s 文件已存在，跳过该文件。（覆盖需设置 overwrite=True）' % filename)
        return
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in content:
                f.writelines(fun(line))


def save_list(filename, lst):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lst:
            f.writelines(line.text+'\t'+line.attrib['href']+'\n')


def save_dict(filename, dict):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in dict:
            f.writelines(item + '\t' + dict[item]+'\n')


def save_list_B(filename, list):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(json.dumps(list, ensure_ascii=False))


def save_log(content):
    filename = os.path.join(BASE_PATH, 'data', 'error.log')
    with open(filename, 'a', encoding='utf-8') as f:
        f.writelines(content + '\n')


def save_to_file(filename, lst, args):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lst:
                if line in args["exc"]:    # 如果到文件结尾，就跳出
                    break
                f.writelines(str(line)+'\n')
    except Exception as e:
        print(e)
