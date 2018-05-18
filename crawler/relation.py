# encoding:utf-8

'''
crawle the relationship
'''

import json
import arrow
import time
import random
import dataset
import traceback
from io import StringIO
from login import ZhihuAccount
from random import uniform
from ipproxy import UAProxy
from parseall import ParseAll
from sql.sqloperat import db

# UA池
ua = UAProxy()
headers = ua.ua_proxy()

# 简单维护url列表
s = ZhihuAccount().login('', '')
new_url = []
old_url = []
rows = db.query("select Relation from Relation group by Relation")
virtual = []
for row in rows:
    virtual.append(row['Relation'])
try:
    db = dataset.connect('mysql+pymysql://root:root@localhost:3306/zhihu?charset=utf8')
except Exception:
    print('MySql Connect Error')


# basic
class FollowBasic(object):
    # init the user and session
    def __init__(self, s, user):
        self.s = s
        self.user = user

    # cacluate offset
    def parse_page(self):
        url = "https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carti" \
              "cles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_ans" \
              "werer)%5D.topics&offset=1&limit=20".format(self.user)
        response = self.s.get(url, headers=random.choice(headers)).content.decode('utf-8')
        try:
            jsdata = json.loads(response)
            page = int(jsdata['paging']['totals'])
        except Exception:
            print('SPIDER INFO: JSONDECODE ERROR')
        return int(page)

    # parse the name and toke and save it to the dict
    def parse_basic(self, page):
        info_dict = {}
        if page != 0:
            for i in range(0, page, 20):
                if i % 30000 == 0 and i != 0:
                    print('SPIDER INFO: SLEEP ONE HOUR TO AVOID IP ERROR')
                    time.sleep(60*60)
                    pass
                uri = "https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carti" \
                      "cles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_ans" \
                      "werer)%5D.topics&offset={}&limit=20".format(self.user, i)
                response = self.s.get(uri, headers=random.choice(headers)).content.decode('utf-8')
                try:
                    jsdata = json.loads(response)
                    userdata = jsdata['data']
                except Exception:
                    print('SPIDER INFO: JSONDECODE ERROR OR IPERROR')
                    print(response)
                    time.sleep(50)
                    continue
                print('SPIDER INFO TIME:' + arrow.now().format('YYYY-MM-DD hh:mm:ss') + ' HAD CRAWLED {} USERS'.format(i))
                for j in range(0, len(userdata)):
                    if userdata[j]['type'] == 'people':
                        # url_token 用户id
                        user = userdata[j]['url_token']
                        info_dict['Token'] = user
                        # id 可以以此作为数据库主键
                        id = userdata[j]['id']
                        info_dict['id'] = id
                        # name
                        info_dict['Name'] = userdata[j]['name']
                        yield info_dict


# 广度优先遍历+递归爬去大v关系链
def relation_chain(start):
    basic = FollowBasic(s, '{}'.format(start))
    max = basic.parse_page()
    table = db['Relation']
    for info_dict in basic.parse_basic(max):
        try:
            info_dict['Relation'] = start
            user = ParseAll(s, info_dict['Token'])
            data = user.create_json()
            success = user.parse_success(data)
            if success['FollowedCount'] > 100000:
                table.insert({**info_dict, **success, **user.parse_success(data)})
                new_url.append(info_dict['Token'])
                print('SPIDER INFO: SAVED DATA FROM THE USER NAMED {}'.format(info_dict['Token']))
            time.sleep(uniform(0.5, 1.2))
        except Exception:
            fp = StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            print(message)
            continue
    for l in new_url:
        if l not in old_url:
            old_url.append(l)
            if l not in virtual:
                relation_chain(l)


if __name__ == '__main__':
    relation_chain('kaifulee')
