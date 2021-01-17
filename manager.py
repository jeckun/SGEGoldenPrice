# -*- coding: utf-8 -*-

import os
from core import PageList
from config import BASE_PATH, URL, Catalog_List


if __name__ == "__main__":

    number = 50

    pg = PageList(URL)
    pg.download_trade(number=number, xpath=Catalog_List)
