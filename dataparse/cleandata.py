# encoding: utf-8
'''
just for testing something, clean data
'''
import os
import sys
from sql.sqloperat import db

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


# clean location info
def clean_location():
    rows = db.query("select Name, Location from UserInfo where Location!=''")
    for row in rows:
        try:
            if '市' in row['Location']:
                new = row['Location'].replace('市', '')
                db.query("update UserInfo set Location='{}' where Name='{}'".format(new, row['Name']))
                print(row['Location'], ' clean one data success')
            elif '北京' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('北京', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '广州' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('广州', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '深圳' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('深圳', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '杭州' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('杭州', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '上海' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('上海', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '成都' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('成都', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '长沙' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('长沙', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '南京' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('南京', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '西安' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('西安', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '广东' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('广东省', row['Name']))
                print(row['Location'], ' clean one data success')
            elif row['Location'] == '江苏':
                db.query("update UserInfo set Location='{}' where Name='{}'".format('江苏省', row['Name']))
                print(row['Location'], ' clean one data success')
            elif '伦敦' in row['Location']:
                db.query("update UserInfo set Location='{}' where Name='{}'".format('伦敦（City of London）', row['Name']))
                print(row['Location'], ' clean one data success')
        except Exception as e:
            print(e)
    print('clean finished')


# create work info
def create_work():
    rows = db.query("select Name, HeadLine from UserInfo where Headline!=''")
    for row in rows:
        try:
            if '学生' in row['HeadLine']:
                db.query("update UserInfo set Work='{}' where Name='{}'".format('学生', row['Name']))
                print(row['HeadLine'] + ' create one data success')
            if '师' in row['HeadLine'] and len(row['HeadLine']) <= 10:
                db.query("update UserInfo set Work='{}' where Name='{}'".format(row['HeadLine'], row['Name']))
                print(row['HeadLine'] + ' create one data success')
        except Exception as e:
            print(e)
            continue
    print('create finished')


# clean work info
def clean_work():
    rows = db.query("select Name, Work from UserInfo where Headline!=''")
    for row in rows:
        if '老师' in row['Work'] or '教师' in row['Work']:
            db.query("update UserInfo set Work='{}' where Name='{}'".format('教师', row['Name']))
            print(row['Work'], ' Clean data success')
        elif '建筑' in row['Work']:
            db.query("update UserInfo set Work='{}' where Name='{}'".format('建筑工程师', row['Name']))
            print(row['Work'], ' Clean data success')
        elif '网络工程师' in row['Work'] or 'Java' in row['Work'] or 'python' in row['Work'] or '算法' in row['Work']\
                or '软件' in row['Work'] or '开发' in row['Work'] or '程序' in row['Work'] or '前端' in row['Work']\
                or 'IT' in row['Work']:
            db.query("update UserInfo set Work='{}' where Name='{}'".format('程序员', row['Name']))
            print(row['Work'], ' Clean data success')
            pass
    print('Clean work finished')


# clean education info
def clean_education():
    rows = db.query("select Name, Education from UserInfo where Education!=''")
    for row in rows:
        if row['Education'] == '大学本科' or row['Education'] == '本科':
            db.query("update UserInfo set Education='{}' where Name='{}'".format('大学', row['Name']))
            print(row['Education'], ' Clean data success')
        elif row['Education'] == '中山大学':
            db.query("update UserInfo set Education='{}' where Name='{}'".format('中山大学（SYSU）', row['Name']))
            print(row['Education'], ' Clean data success')
        elif row['Education'] == '华南理工大学':
            db.query("update UserInfo set Education='{}' where Name='{}'".format('华南理工大学（SCUT）', row['Name']))
            print(row['Education'], ' Clean data success')


# merge tables
def merge():
    user = db['UserInfo']
    relation = db['Relation']
    for rela in relation:
        # del rela['RecId']
        try:
            user.upsert(rela, 'Token')
            print('insert success')
        except Exception as e:
            print(e)
            continue
    pass


if __name__ == '__main__':
    # clean_location()
    # create_work()
    # clean_work()
    # create_business()
    # clean_education()
    # merge()
    pass