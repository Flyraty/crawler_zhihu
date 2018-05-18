# encoding:utf-8

'''
UA Proxy  and IPProxy
'''
import os
import sys
import faker
# from haipproxy.client.py_cli import ProxyFetcher
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class UAProxy(object):
    def __init__(self):
        pass

    # 实现一个500个UA的池子
    def ua_proxy(self):
        headers = []
        for i in range(500):
            headers.append({'User_Agent': faker.Faker().user_agent()})
        return headers


class IPProxy(object):
    def __init__(self):
        pass

    # 从redis代理池中取出haipproxy检验过的ip
    # def ip_proxy(self):
    #     args = dict(host='127.0.0.1', port=6379, password='', db=0)
    #     fetcher = ProxyFetcher('zhihu', strategy='greedy', length=5, redis_args=args)
    #     # 获取一个可用代理
    #     return fetcher.get_proxy()
    #     pass

    # 获取ip代理的类型
    def ip_type(self, ip):
        return ip.split('://')[0]
        pass


if __name__ == '__main__':
    pass