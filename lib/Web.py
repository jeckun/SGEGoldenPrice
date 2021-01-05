# -*- coding: UTF-8 -*-
# 开发团队： 洪虎小队
# 开发人员： Administrator
# 开发时间： 2020/12/20 23:13
# 文件名称： Web.py

import requests
from lxml import etree
from urllib.parse import urlparse

cookies = {
    # '__51cke__': '',
    # 'Hm_lvt_4b7e3399425533b25385d99f54903f35': '1600142209',
    # 'Hm_lvt_e7f8576aca22821dcc64d5aa7593c228': '1600405588',
    # 'Hm_lpvt_e7f8576aca22821dcc64d5aa7593c228': '1600405588',
    # '__tins__993853': '%7B%22sid%22%3A%201600441045201%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201600442859682%7D',
    # '__51laig__': '123',
    # 'Hm_lpvt_4b7e3399425533b25385d99f54903f35': '1600441060',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'iframe',
    'Referer': 'https://zhaoze.icu/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

params = (
    ('idzone', '3608587^'),
    ('type', '300x50^'),
    ('p', 'https^%^3A//zhaoze.icu/^'),
    ('dt', '1609077756953^'),
    ('sub', '^'),
    ('tags', '^'),
    ('screen_resolution', '1536x864^'),
    ('el', '^%^22'),
)


def get_host(url):
    """ 返回域名，如：https://www.baidu.com """
    ul = urlparse(url)
    return ul.scheme + '://' + ul.hostname


def add_host(url, path):
    return get_host(url) + path


def get_Html(url, headers, cookies=None, params=None):
    """ 返回网页内容 """
    if cookies:
        r = requests.get(url=url, headers=headers, cookies=cookies)
    else:
        r = requests.get(url=url, headers=headers)
    r.encoding = "utf-8"
    return etree.HTML(r.text)


def get_list(html, xpath):
    """ 返回指定位置的列表 """
    return html.xpath(xpath)


def get_List_xpath(html, text, href):
    """ 从网页指定位置获取列表并返回列表 """
    return dict(zip(get_list(html, text), get_list(html, href)))


def get_link(html, xpath):
    """ 返回指定位置的链接 """
    try:
        rs = html.xpath(xpath)[0]
    except IndexError as e:
        return ''
    return rs


def get_text(html, xpath):
    """ 返回指定位置的链接 """
    return html.xpath(xpath)
