import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_PATH, 'data', 'foo.db')

URL = 'https://www.sge.com.cn/sjzx/mrhqsj'

Catalog_List = '''//div[@class="articleList border_ea mt30 mb30"]/ul/li/a |
               //div[@class="articleList border_ea mt30 mb30"]/ul/li/a/span[2]
    '''

Table_xpath = '//table[@class="ke-zeroborder"]/tbody'
col_xpath = Table_xpath + '/tr/td[1]'
row_xpath = Table_xpath + '/tr[%d]/td'

sge_script = ['load', 'get_catalog_list', 'get_table']
