# encoding:utf-8

import sys
import os
import dataset
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


try:
    db = dataset.connect('mysql+pymysql://root:root@localhost:3306/zhihu?charset=utf8')
except Exception:
    print('MySql Connect Error')


#  sql operate
class QueryInfo(object):
    def __init__(self):
        pass

    def read_info(self, data, queue):
        queue.put(data)

    def save_info(self, data, table):
        # value = queue.get(True)
        info = db['{}'.format(table)]
        info.insert(data)
        pass

    def query(self, table):
        info = db['{}'.format(table)]
        ids = []
        for user in info:
            ids.append(user['id'])
        return ids

    def query_coulmn(self, table, keyword):
        info = db['{}'.format(table)]
        keywords = []
        for user in info:
            keywords.append(user['{}'.format(keyword)])
        return keywords


if __name__ == '__main__':
    pass