# encoding:utf-8

'''
because of the nunber of request to zhihu in zhihuuser.py is frequent, so i decided to rewrite the class
that parse zhihu info
'''


import json
import arrow
import time
import random
from parsel import Selector
from lxml import etree
from random import uniform
from ipproxy import UAProxy
from login import ZhihuAccount

# set random relay  设置随机延迟
relay = [1, 1.5, 2]

# UA池
ua = UAProxy()
headers = ua.ua_proxy()


# prse the basic information,
class ParseBasic(object):
    # init the user and session 初始化会话信息和url接口,起始user
    def __init__(self, s, user):
        self.s = s
        self.user = user

    # cacluate offset 解析出该用户下的关注者的多少并简单计算offset
    def parse_page(self):
        url = "https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carti" \
              "cles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_ans" \
              "werer)%5D.topics&offset=1&limit=20".format(self.user)
        response = self.s.get(url, headers=random.choice(headers)).content.decode('utf-8')
        jsdata = json.loads(response)
        page = int(jsdata['paging']['totals'])
        return int(page)

    # parse the name and toke and save it to the dict解析出基本信息,存入字典
    def parse_basic(self, page):
        info_dict = {}
        if page != 0:
            for i in range(0, page, 20):
                if i % 30000 == 0 and i != 0:
                    print('SPIDER INFO: SLEEP ONE HOUR TO AVOID IP ERROR')
                    time.sleep(60*60)
                    pass
                uri = "https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carti" \
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
                        # 关注者人数
                        # info_dict['FollowedCount'] = userdata[j]['follower_count']
                        # time.sleep(random.choice(relay))
                        yield info_dict


# parse the all information about user by the json in the html sourcecode
class ParseAll(object):
    def __init__(self, s, user):
        self.s = s
        self.user = user

    # this function is used to create a json object contained userinfo
    def create_json(self):
        url = 'https://www.zhihu.com/people/{}/activities'.format(self.user)
        response = self.s.get(url, headers=random.choice(headers))
        sel = Selector(response.text)
        jsdata = sel.css('div#data::attr(data-state)').extract_first()
        itemdata = json.loads(jsdata)
        return itemdata

    # this function is used to parse the num information
    def parse_success(self, data):
        info_dict = {}
        itemdata = data['entities']['users']['{}'.format(self.user)]
        # 个人回答数
        info_dict['PersonalAnswerCount'] = itemdata['answerCount']
        # 个人提问数
        info_dict['PersonalQuestionCount'] = itemdata['questionCount']
        # 个人文章数
        info_dict['PersonalArticlesCount'] = itemdata['articlesCount']
        # 个人专栏数
        info_dict['PersonalColumnCount'] = itemdata['columnsCount']
        # 个人想法数
        info_dict['PersonalIdeasCount'] = itemdata['pinsCount']
        # 收录回答数
        info_dict['CollectAnswersCount'] = itemdata['includedAnswersCount']
        # 收录文章数
        info_dict['CollectArticlesCount'] = itemdata['includedArticlesCount']
        # 获得赞同数
        info_dict['GetAwardCount'] = itemdata['voteupCount']
        # 获得感谢数
        info_dict['GetThanksCount'] = itemdata['thankedCount']
        # 获得收藏数
        info_dict['GetCollectCount'] = itemdata['favoritedCount']
        # 参与公共编辑数
        info_dict['PublicEditeCount'] = itemdata['logsCount']
        # 关注了多少人
        info_dict['FollowingCount'] = itemdata['followingCount']
        # 多少人关注他
        info_dict['FollowedCount'] = itemdata['followerCount']
        # 举办的live数
        info_dict['TakeLiveCount'] = itemdata['hostedLiveCount']
        # 赞助的live数
        # info_dict['SproveLiveCount'] = itemdata['']
        # 参加的live数
        # 关注话题数
        info_dict['FollowTopicCount'] = itemdata['followingTopicCount']
        # 关注专栏数
        info_dict['FollowColumnCount'] = itemdata['followingColumnsCount']
        # 关注问题数
        info_dict['FollowQuestionsCount'] = itemdata['followingQuestionCount']
        # 关注收藏夹数
        info_dict['FollowCollectCount'] = itemdata['followingFavlistsCount']
        return info_dict
        pass

    # this function is used to parse the personal detail information
    def parse_detail(self, data):
        info_dict = {}
        itemdata = data['entities']['users']['{}'.format(self.user)]
        # 教育经历 默认取最新的教育经历(包括学校和专业)
        if itemdata['educations']:
            if 'major' in itemdata['educations'][0].items():
                major = itemdata['educations'][0]['major']['name']
            else:
                major = ''
            if 'school' in itemdata['educations'][0]:
                school = itemdata['educations'][0]['school']['name']
            else:
                school = ''
            info_dict['Education'] = school
            info_dict['Major'] = major
        else:
            info_dict['Education'] = ''
            info_dict['Major'] = ''
        # headline 个人签名
        info_dict['HeadLine'] = itemdata['headline']
        # 个人简介 description
        info_dict['Introduction'] = itemdata['description']
        # 所属行业 business
        if 'business' in itemdata.items():
            info_dict['Business'] = itemdata['business']['name']
        else:
            info_dict['Business'] = ''
        # 职业经历 employments,默认取第一个
        if itemdata['employments']:
            if 'job' in itemdata['employments'][0].items():
                info_dict['Work'] = itemdata['employments'][0]['job']['name']
            else:
                info_dict['Work'] = ''
        else:
            info_dict['Work'] = ''
        # 个人主页背景图 coverUrl
        info_dict['CoverUrl'] = itemdata['coverUrl']
        # 个人头像 avatarUrl
        info_dict['HeadImg'] = itemdata['avatarUrl']
        # 居住地 locations,取的是现居住地，所以默认取第一个
        if itemdata['locations']:
            info_dict['Location'] = itemdata['locations'][0]['name']
        else:
            info_dict['Location'] = ''
        # 个人所得认证称号badge
        if itemdata['badge']:
            info_dict['Badge'] = itemdata['badge'][0]['description']
        else:
            info_dict['Badge'] = ''
        # 性别gender
        info_dict['Gender'] = itemdata['gender']
        # 这里遗漏了一个数字信息，暂时写这了，该用户参加的live场数
        info_dict['ParticuteLiveCount'] = itemdata['participatedLiveCount']
        return info_dict


# parse tag or columns and use it to parse user
class ParseUserTag(object):
    # 初始化user 和用户token
    def __init__(self, s, user):
        self.s = s
        self.user = user

    # create a xml object根据相应页面关键字构造url,并返回该页面的一个xml对象
    def create_xml(self, word):
        full_url = 'https://www.zhihu.com/people/{}/following/{}'.format(self.user, word)
        response = self.s.get(full_url, headers=random.choice(headers))
        html = etree.HTML(response.content.decode('utf-8'))
        return html

    # parse the page of topics or columns 解析相应的页数,默认为1
    def parse_page(self, html):
        if html.xpath('//div[@class="List-item"]'):
            if html.xpath('//div[@class="Pagination"]'):
                page = int(html.xpath('//div[@class="Pagination"]//text()')[-2])
                return page
            else:
                page = 1
                return page
        else:
            page = 0
            return page
        pass

    # parse column information 解析专栏的信息
    def parse_column(self, page):
        info_dict = {}
        if page == 0:
            print('this user has no follow columns')
            return False
        else:
            for i in range(1, page + 1):
                url = 'https://www.zhihu.com/people/{}/following/columns?page={}'.format(self.user, i)
                response = self.s.get(url, headers=random.choice(headers))
                sel = Selector(response.text)
                jsdata = sel.css('div#data::attr(data-state)').extract_first()
                itemdata = json.loads(jsdata)
                # columns id 列表
                id_list = itemdata['people']['followingColumnsByUser']['{}'.format(self.user)]['ids']
                new_id_list = [id for id in id_list if id]
                # 专栏详情页列表
                columns_detail_dict = itemdata['entities']['columns']
                for id in new_id_list:
                    column_detail = columns_detail_dict[id]
                    # 最新更新时间
                    updated_time = arrow.get(column_detail['updated']).format('YYYY-MM-DD hh:mm:ss')
                    info_dict['UpdateTime'] = updated_time
                    # 专栏名称
                    column_name = column_detail['title']
                    info_dict['ColumnName'] = column_name
                    # 专栏url
                    column_url = column_detail['url']
                    info_dict['Url'] = column_url
                    # 公开允许
                    commentPermission = column_detail['commentPermission']
                    info_dict['Permission'] = commentPermission
                    # 专栏创建者
                    column_author = column_detail['author']['name']
                    info_dict['ColumnAuthor'] = column_author
                    # 专栏简介
                    column_intro = column_detail['intro']
                    info_dict['Introduction'] = column_intro
                    # 专栏头像
                    column_headimg = column_detail['imageUrl']
                    info_dict['HeadImg'] = column_headimg
                    # 专栏关注者
                    column_followers_count = column_detail['followers']
                    info_dict['FollowedCount'] = column_followers_count
                    # 专栏id
                    column_id = column_detail['id']
                    info_dict['Columnid'] = column_id
                    # 专栏文章数
                    column_article_coumnt = column_detail['articlesCount']
                    info_dict['ArticleCount'] = column_article_coumnt
                    info_dict['LastModifyTime'] = arrow.now().format('YYYY-MM-DD hh:mm:ss')
                    time.sleep(uniform(0.5, 1.2))
                    yield info_dict

    # parse the user what had follwed columns 解析该user关注的专栏
    def parse_personal_column(self, page):
        info_dict = {}
        if page == 0:
            print('this user has no follow columns')
        else:
            columns = []
            for i in range(1, page + 1):
                url = 'https://www.zhihu.com/people/{}/following/columns?page={}'.format(self.user, i)
                response = self.s.get(url, headers=random.choice(headers))
                html = etree.HTML(response.content.decode('utf-8'))
                sel = Selector(response.text)
                jsdata = sel.css('div#data::attr(data-state)').extract_first()
                itemdata = json.loads(jsdata)
                # columns id 列表
                id_list = itemdata['people']['followingColumnsByUser']['{}'.format(self.user)]['ids']
                new_id_list = [id for id in id_list if id]
                # 专栏详情页列表
                columns_detail_dict = itemdata['entities']['columns']
                for id in new_id_list:
                    columns.append(columns_detail_dict[id]['title'])
            info_dict['followed_columns'] = ','.join(columns)
            return info_dict

    # parse topics information 解析话题信息
    def parse_topic(self, page):
        info_dict = {}
        if page == 0:
            print('this user has no follow topics')
            return False
        else:
            for i in range(1, page + 1):
                url = 'https://www.zhihu.com/people/{}/following/topics?page={}'.format(self.user, i)
                response = self.s.get(url, headers=random.choice(headers))
                sel = Selector(response.text)
                jsdata = sel.css('div#data::attr(data-state)').extract_first()
                itemdata = json.loads(jsdata)
                # 关注的话题id列表
                id_list = itemdata['people']['followingTopicsByUser']['{}'.format(self.user)]['ids']
                new_id_list = [id for id in id_list if id]
                # 关注的话题的详细信息的字典
                topic_detail_dict = itemdata['entities']['topics']
                for id in new_id_list:
                    topic_detail = topic_detail_dict[id]
                    # 该话题id
                    topic_id = topic_detail['id']
                    info_dict['TopicId'] = topic_id
                    # 该话题头像
                    headimg = topic_detail['avatarUrl']
                    info_dict['HeadImg'] = headimg
                    # 话题名称
                    topic_name = topic_detail['name']
                    info_dict['TopicName'] = topic_name
                    # 话题简介
                    topic_intro = topic_detail['introduction']
                    info_dict['Introduction'] = topic_intro
                    # 话题url
                    topic_url = topic_detail['url']
                    info_dict['Url'] = topic_url
                    '''利用登录会话访问话题url'''
                    topic_info = json.loads(self.s.get(topic_url, headers=random.choice(headers)).content.decode('utf-8'))
                    # 该话题下问题总数
                    topic_question_count = topic_info['questions_count']
                    info_dict['TopicQuestionsCount'] = topic_question_count
                    # 该话题下关注人数
                    topic_follow_count = topic_info['followers_count']
                    info_dict['FollowedCount'] = topic_follow_count
                    # 该话题下优秀回答数
                    best_answers_count = topic_info['best_answers_count']
                    info_dict['GoodAnswersCount'] = best_answers_count
                    # 话题下优秀回答者
                    best_answerers_count = topic_info['best_answerers_count']
                    info_dict['GoodAnswerersCount'] = best_answerers_count
                    info_dict['LastModifyTime'] = arrow.now().format('YYYY-MM-DD hh:mm:ss')
                    time.sleep(uniform(0.5, 1.2))
                    yield info_dict

    # parse the user what had followed topics and topics weight 解析该user关注的话题及对应回答数，并计算权重
    def parse_personal_topic(self, page):
        info_dict = {}
        if page == 0:
            print('this user has no follow topics')
            return False
        else:
            topics_answers = []
            sum = 0  # 计算一下所有话题下的回答总数,用于后续数据分析的标签权重计算
            for i in range(1, page + 1):
                url = 'https://www.zhihu.com/people/{}/following/topics?page={}'.format(self.user, i)
                response = self.s.get(url, headers=random.choice(headers))
                sel = Selector(response.text)
                jsdata = sel.css('div#data::attr(data-state)').extract_first()
                itemdata = json.loads(jsdata)
                # 关注的话题id列表
                id_list = itemdata['people']['followingTopicsByUser']['{}'.format(self.user)]['ids']
                new_id_list = [id for id in id_list if id]
                # 关注的话题的详细信息的字典
                topic_detail_dict = itemdata['entities']['topics']
                # 用户在该话题下的回答数字典
                topic_answers_count = itemdata['people']['followingTopicsByUser']['{}'.format(self.user)][
                    'contributions']
                for id in new_id_list:
                    topic_name = topic_detail_dict[id]['name']
                    topic_answer = topic_answers_count[id]
                    sum += topic_answer
                    topics_answers.append(topic_name + '/' + str(topic_answer))
            info_dict['FollowTopics'] = ','.join(topics_answers)
            return info_dict, sum


# test the code 测试代码
if __name__ == '__main__':
    pass
