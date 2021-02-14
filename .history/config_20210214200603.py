import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_PATH, 'data', 'foo.db')

URL = {
    'sge': 'https://www.sge.com.cn/sjzx/mrhqsj',
    'cngold': "https://quote.cngold.org/gjs/jjs_hjtd.html",
}

sge_script = ['get_catalog_list', 'get_table', 'save_to_db']

sge_xpath = {
    'catalog_list': ".articleList ul li a",
    'catalog_list_span': ".articleList .fr",
    'col':  ".ke-zeroborder tbody tr td:nth-child(1)",
    'col2': ".content table tbody tr td:nth-child(1)",
    'row': ".ke-zeroborder tbody tr:nth-child(%d) td",
    'row2': ".content tbody tr:nth-child(%d) td",
    'row2': ".content  table tbody tr:nth-child(2) td",
}
