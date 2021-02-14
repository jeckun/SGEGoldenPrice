import json
import os
from config import BASE_PATH


def callback(fun, args=(), **kwargs):
    """ 回调函数
    fun: 被回调函数名称
    args: 回调函数的参数
    kwargs: 其他参数
    """
    a = []
    if len(args) != len(fun.__code__.co_varnames):
        raise Exception("参数数量不一致")
    cmd = "fun("
    for i in range(len(fun.__code__.co_varnames)):
        item = "args[%d]" % i
        a.append(item)
    cmd = cmd + ', '.join(a) + ')'
    return eval(cmd)


def add(x, y):
    return x + y


# a = callback(add, (2, 4))
# print(a)


def text(text):
    return text.replace('\r', '').replace('-', '').replace(
        '\t', '').replace('\n', '').replace(',', '').replace(' ', '')


def save_to_json(filename, list):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in list:
            f.writelines(json.dumps(line, ensure_ascii=False)+'\n')


def load_by_json(filename):
    fs = []
    for line in open(filename, 'r', encoding='utf-8'):
        fs.append(json.loads(line, encoding='utf-8'))
    # with open(filename, 'r', encoding='utf-8') as f:
    #     fs += f.readline()
    # return json.loads(fs, encoding='utf-8')
    return fs


def cache(filename, content):
    save_to_json(filename, content)


def join(*args):
    path = os.path.join(BASE_PATH)
    for item in args:
        path = os.path.join(path, item)
    return path


def exists(path):
    return os.path.exists(path)


def makdir(path):
    os.mkdir(path)


def delfile(filename):
    os.remove(filename)


def save_log(content):
    filename = os.path.join(BASE_PATH, 'data', 'error.log')
    with open(filename, 'a', encoding='utf-8') as f:
        f.writelines(content + '\n')
