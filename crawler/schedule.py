# encoding:utf-8

'''
schedule the spider
'''

import traceback
import time
import sys
import os
from random import uniform
from io import StringIO
from login import ZhihuAccount
from sql.sqloperat import QueryInfo
from parseall import ParseAll, ParseBasic, ParseUserTag

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


# schedule the spider
class SpiderSchedule(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        zhihu = ZhihuAccount()
        self.s = zhihu.login(user, password)
        pass

    def schedule_user_spider(self):
        basic = ParseBasic(self.s, 'kaifulee')
        max = basic.parse_page()
        database = QueryInfo()
        ids = database.query('UserInfo')
        for info_dict in basic.parse_basic(max):
            try:
                if info_dict['id'] in ids:
                    print('SPIDER INFO: THE USER IN THE DataBase,DONT REPEAT')
                    continue
                user = ParseAll(self.s, info_dict['Token'])
                data = user.create_json()
                tag_dict = {}
                # print({**info_dict, **user.parse_detail(data), **user.parse_success(data), **tag_dict})
                dic = {**info_dict, **user.parse_detail(data), **user.parse_success(data), **tag_dict}
                database.save_info(dic, 'UserInfo')
                print('SPIDER INFO: SAVED DATA FROM THE USER NAMED {}'.format(info_dict['Token']))
                time.sleep(uniform(0.5, 1.2))
            except Exception:
                fp = StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                print(message)
                continue
        pass

    def schedule_topic_spider(self):
        basic = ParseBasic(self.s, 'kaifulee')
        max = basic.parse_page()
        database = QueryInfo()
        for info_dict in basic.parse_basic(max):
            try:
                parse = ParseUserTag(self.s, info_dict['Token'])
                response = parse.create_xml('topics')
                page = parse.parse_page(response)
                if parse.parse_topic(page):
                    for topic_dict in parse.parse_topic(page):
                        database.save_info(topic_dict, 'Topics')
                        print('TOPIC SPIDER INFO: SAVED DATA FROM THE TOPIC NAMED {}'.format(topic_dict['TopicName']))
                        time.sleep(uniform(0.5, 1.2))
            except Exception:
                fp = StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                if 'Duplicate entry' in message:
                    print('TOPIC SPIDER INFO: DONT REPEAT')
                else:
                    print('TOPIC SPIDER INFO:DONT REPEAT')
                continue
        pass

    def schedule_column_spider(self):
        basic = ParseBasic(self.s, 'kaifulee')
        max = basic.parse_page()
        database = QueryInfo()
        for info_dict in basic.parse_basic(max):
            try:
                parse = ParseUserTag(self.s, info_dict['Token'])
                response = parse.create_xml('columns')
                page = parse.parse_page(response)
                if parse.parse_column(page):
                    for column_dict in parse.parse_column(page):
                        database.save_info(column_dict, 'Columns')
                        time.sleep(uniform(0.5, 1.2))
                        print('Column SPIDER INFO: SAVED DATA FROM THE Column NAMED {}'.format(column_dict['ColumnName']))
                pass
            except Exception:
                fp = StringIO()
                traceback.print_exc(file=fp)
                message = fp.getvalue()
                print('Column SPIDER INFO: DONT REPEAT')
                # print(message)
                continue

    def schedule_main(self):
        try:
            if sys.argv[1] == 'userspider':
                self.schedule_user_spider()
            elif sys.argv[1] == 'topicspider':
                self.schedule_topic_spider()
            elif sys.argv[1] == 'columnspider':
                self.schedule_column_spider()
            else:
                print('SPIDER SCHEDULE INFO: YOU NEED A ARGUEMENT')
                pass
        except Exception:
            print('SPIDER SCHEDULE INFO: YOU NEED A ARGUEMENT')


if __name__ == '__main__':
    user_schedule = SpiderSchedule('', '')
    # user_schedule.schedule_main()
    user_schedule.schedule_user_spider()
    # user_schedule.schedule_column_spider()
    # user_schedule.schedule_topic_spider()
    pass
