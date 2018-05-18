# encoding:utf-8
'''
this function use to get zhihu captche,
验证码由字符验证码变成了滑动验证码
'''

import faker
import requests
import os
import sys
from login import Login
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class GetCaptche(object):
    def __init__(self):
        pass

    def get_captche(self, count):
        if not os.path.exists('./train'):
            os.mkdir('./train')
        os.chdir('./train')
        username = ''
        password = ''
        zhihu = Login(username, password)
        s = zhihu.login()
        for i in range(0, count):
            headers = {
                'User_Agent': faker.Faker().user_agent()
            }
            url = 'https://www.zhihu.com/captcha.gif'
            response = s.get(url, headers=headers)
            if response.status_code != 200:
                break
            with open('{}.gif'.format(i), 'wb') as f:
                f.write(response.content)


if __name__ == '__main__':
    # captche = GetCaptche()
    # captche.get_captche(40000)
    pass
