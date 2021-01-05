# -*- coding: UTF-8 -*-
# 开发团队： 洪虎小队
# 开发人员： Administrator
# 开发时间： 2020/12/20 23:11
# 文件名称： Thread.py

# Author: Eric
# time:

import threading
import os


def thread_run(fun, task_list, args):
    """
    # 多线程方式执行一个列表的任务
    :param fun:  保存函数
    :param task_list:  下载列表[名称, 链接]
    :param args: 函数参数
    :return: 无
    """
    thread_list = []

    # 创建线程
    for lst in task_list:
        thd = threading.Thread(target=fun, args=(lst, args))
        thread_list.append(thd)

    # 启动线程
    for thd in thread_list:
        thd.setDaemon(True)
        thd.start()

    # 阻塞主线程到子线程执行结束
    for thd in thread_list:
        thd.join()

    return
