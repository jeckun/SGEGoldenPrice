# -*- coding: utf-8 -*-
import requests
from lxml import etree
from selenium import webdriver
from urllib.parse import urlparse


class BaseSpider(object):
    _url = ''
    _html = None
    _host = ''

    def __init__(self):
        pass

    def open(self, url, headers=None, cookies=None, params=None):
        self._url = url
        ul = urlparse(self._url)
        if ul.scheme and ul.hostname:
            self._host = ul.scheme + '://' + ul.hostname
        try:
            self._url = url
            response = requests.get(url, params=params)
            response.encode = 'utf-8'
            self._html = response.text
        except Exception as e:
            print('Error: %s' % e)

    @property
    def host(self):
        return self._host


class SpiderLxml(BaseSpider):
    def open(self, url, headers=None, cookies=None, params=None):
        try:
            super(SpiderLxml, self).open(url, headers, cookies, params)
            self._html = etree.HTML(self._html)
        except Exception as e:
            print('Error: %s' % e)

    def get_element_by_xpath(self, xpath, fun):
        try:
            # return fun(self._html.xpath(xpath))
            elements = self._html.xpath(xpath)
            return fun(elements)
        except Exception as e:
            print('Error: %s' % e)

    def get_element(self, xpath):
        return self._html.xpath(xpath)


EXECUTABLE_PATH = "C:\Python\Selenium\ChromeDriver\chromedriver.exe"


class SpiderSelenium(BaseSpider):
    def __init__(self):
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')

        if EXECUTABLE_PATH:
            self.driver = webdriver.Chrome(
                executable_path=EXECUTABLE_PATH)
        else:
            self.driver = webdriver.Chrome()

    def find_element_by_class_name(self, clsname, fun=None):
        if fun:
            return fun(self.driver.find_element_by_class_name(clsname))
        else:
            return self.driver.find_element_by_class_name(clsname)

    def find_elements_by_class_name(self, clsname, fun=None):
        if fun:
            return fun(self.driver.find_elements_by_class_name(clsname))
        else:
            return self.driver.find_elements_by_class_name(clsname)

    def find_element_by_id(self, id, fun=None):
        if fun:
            return fun(self.driver.find_element_by_id(id))
        else:
            return self.driver.find_element_by_id(id)

    def find_elements_by_id(self, id, fun=None):
        if fun:
            return fun(self.driver.find_elements_by_id(id))
        else:
            return self.driver.find_elements_by_id(id)

    def find_element_by_xpath(self, xpath, fun=None):
        if fun:
            return fun(self.driver.find_element_by_xpath(xpath))
        else:
            return self.driver.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath, fun=None):
        if fun:
            return fun(self.driver.find_elements_by_xpath(xpath))
        else:
            return self.driver.find_elements_by_xpath(xpath)

    def open(self, url):
        self._url = url
        ul = urlparse(self._url)
        if ul.scheme and ul.hostname:
            self._host = ul.scheme + '://' + ul.hostname
        self.driver.get(url)

    def max_window(self):
        self.driver.maximize_window()

    def min_window(self):
        self.driver.minimize_window()

    def quit(self):
        self.driver.quit()

    def execute_script(self, js):
        self.driver.execute_script(js)
