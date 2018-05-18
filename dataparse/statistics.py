# encoding:utf-8

'''
Statistics zhihu info,  一个函数对应一个图表
'''
import os
import sys
from pyecharts import Pie, Bar, WordCloud, Style, Gauge, HeatMap, Funnel, Page, Graph
from sql.sqloperat import db
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


# 统计运行情况的装饰器
def debug(func):
    def wrapper():
        print("[DEBUG]: enter {}()".format(func.__name__))
        return func()
    return wrapper


'''男女比例统计部分'''


# 男女比例
@debug
def gender():
    men = db.query("select Count(*) from UserInfo where Gender=1")
    for man in men:
        male = man['Count(*)']
    women = db.query("select Count(*) from UserInfo where Gender=0")
    for woman in women:
        female = woman['Count(*)']
    attr = ['男生', '女生']
    pie = Pie("知乎男女比例", title_pos='auto')
    pie.add("", attr, [male, female], is_label_show=True)
    return pie


# 地区男女比例
@debug
def location_gender():
    pie = Pie('知乎top10地区男女比例', "", title_pos='auto')
    style = Style()
    pie_style = style.add(
        label_pos="center",
        is_label_show=True,
        label_text_color=None
    )
    rows = db.query("select  Location ,Count(*) from UserInfo where Location!='' "
                    "group by Location order by Count(*) DESC LIMIT 10")
    centers = [[10, 30], [30, 30], [50, 30], [70, 30], [90, 30],
               [10, 70], [30, 70], [50, 70], [70, 70], [90, 70]]
    i = 0
    for row in rows:
        male_loca = db.query('select Count(*) from UserInfo where gender=1 and Location="{}"'.format(row['Location']))
        for male in male_loca:
            males = male['Count(*)']
        female_loca = db.query('select Count(*) from UserInfo where gender=0 and Location="{}"'.format(row['Location']))
        for female in female_loca:
            females = female['Count(*)']
        # 计算百分比
        format_male = round(males/(males+females)*100, 2)
        format_female = round(females/(males+females)*100, 2)
        pie.add("", ['{}'.format(row['Location']), ""], [format_male, format_female], center=centers[i],
                radius=[18, 24], **pie_style, legend_top='center')
        i += 1
    return pie


# 高校男女比例
@debug
def education_gender():
    pie = Pie('知乎top10高校男女比例', "", title_pos='auto')
    style = Style()
    pie_style = style.add(
        label_pos="center",
        is_label_show=True,
        label_text_color=None
    )
    rows = db.query("select  Education ,Count(*) from UserInfo where Education!='' "
                    "group by Education order by Count(*) DESC LIMIT 1,10")
    centers = [[10, 30], [30, 30], [50, 30], [70, 30], [90, 30],
               [10, 70], [30, 70], [50, 70], [70, 70], [90, 70]]
    i = 0
    for row in rows:
        male_loca = db.query('select Count(*) from UserInfo where gender=1 and Education="{}"'.format(row['Education']))
        for male in male_loca:
            males = male['Count(*)']
        female_loca = db.query('select Count(*) from UserInfo where gender=0 and Education="{}"'.format(row['Education']))
        for female in female_loca:
            females = female['Count(*)']
        # 计算百分比
        format_male = round(males / (males + females) * 100, 2)
        format_female = round(females / (males + females) * 100, 2)
        pie.add("", ['{}'.format(row['Education']), ""], [format_male, format_female], center=centers[i],
                radius=[18, 24], **pie_style, legend_top='center')
        i += 1
    return pie


# 知乎top10职业男女比例, 去除学生
@debug
def work_gender():
    pie = Pie('知乎top10职业男女比例', "", title_pos='auto')
    style = Style()
    pie_style = style.add(
        label_pos="center",
        is_label_show=True,
        label_text_color=None
    )
    rows = db.query("select  Work ,Count(*) from UserInfo where Work!='' "
                    "group by Work order by Count(*) DESC LIMIT 1,10")
    centers = [[10, 30], [30, 30], [50, 30], [70, 30], [90, 30],
               [10, 70], [30, 70], [50, 70], [70, 70], [90, 70]]
    i = 0
    for row in rows:
        male_loca = db.query('select Count(*) from UserInfo where gender=1 and Work="{}"'.format(row['Work']))
        for male in male_loca:
            males = male['Count(*)']
        female_loca = db.query(
            'select Count(*) from UserInfo where gender=0 and Work="{}"'.format(row['Work']))
        for female in female_loca:
            females = female['Count(*)']
        # 计算百分比
        format_male = round(males / (males + females) * 100, 2)
        format_female = round(females / (males + females) * 100, 2)
        pie.add("", ['{}'.format(row['Work']), ""], [format_male, format_female], center=centers[i],
                radius=[18, 24], **pie_style, legend_top='center')
        i += 1
    return pie


'''地区分布统计部分'''


# 地区分布直方图
@debug
def location():
    location = db.query("select  Location ,Count(*) from UserInfo where Location!='' "
                        "group by Location order by Count(*) DESC LIMIT 10")
    locas = []
    counts = []
    for loca in location:
        locas.append(loca['Location'])
        counts.append(loca['Count(*)'])
    bar = Bar("知乎用户地区分布")
    bar.add("", locas, counts, label_color=['rgba(0,0,0,0)'], is_stack=True)
    bar.add("location", locas, counts, is_label_show=True, is_stack=True, label_pos='inside')
    bar.render()
    return bar


# 地区词云
@debug
def location_graph():
    locas = []
    counts = []
    location = db.query("select  Location ,Count(*) from UserInfo where Location!='' "
                        "group by Location order by Count(*) DESC LIMIT 100")
    for loca in location:
        locas.append(loca['Location'])
        counts.append(loca['Count(*)'])
    wordcloud = WordCloud("地区词云", width=1300, height=620)
    wordcloud.add("", locas, counts, word_size_range=[20, 100], shape='diamond')
    return wordcloud


'''用户活跃度分析'''


# 僵尸用户率 统计标准 回答数+提问数+关注数=0
@debug
def dead_user():
    rows = db.query("select Count(*) from UserInfo where (FollowedCount+PersonalAnswerCount+PersonalQuestionCount) =0")
    for row in rows:
        count = row['Count(*)']
    all = db.query("select Count(*) from UserInfo")
    for user in all:
        all_count = user['Count(*)']
    gauge = Gauge("知乎僵尸用户率")
    gauge.add("知乎僵尸用户率", "僵尸用户率",  round((count / all_count)*100, 2))
    return gauge


# 关注用户数分布 无, 1-9, 10~99, 100~999, 1000~9999, 10000~
@debug
def followed():
    classes = ['无', '1-9', '10-99', '100-999', '1000-9999', '10000+']
    values = []
    zero_followed = db.query('select Count(*) from UserInfo where FollowedCount=0')
    for zero in zero_followed:
        values.append(zero['Count(*)'])
    one_followed = db.query('select Count(*) from UserInfo where FollowedCount between 1 and 9')
    for one in one_followed:
        values.append(one['Count(*)'])
    two_followed = db.query('select Count(*) from UserInfo where FollowedCount between 10 and 99')
    for two in two_followed:
        values.append(two['Count(*)'])
    three_followed = db.query('select Count(*) from UserInfo where FollowedCount between 100 and 999')
    for three in three_followed:
        values.append(three['Count(*)'])
    four_followed = db.query('select Count(*) from UserInfo where FollowedCount between 1000 and 9999')
    for four in four_followed:
        values.append(four['Count(*)'])
    five_followed = db.query('select Count(*) from UserInfo where FollowedCount>=10000')
    for five in five_followed:
        values.append(five['Count(*)'])
    pie = Pie("知乎关注数分布", title_pos='auto')
    pie.add("", classes, values, is_label_show=True)
    return pie


# 回答数用户分布 未回答过问题, 回答有赞同, 回答无赞同
@debug
def answers():
    classes = ['无回答', '有回答,有赞同', '有回答, 无赞同']
    values = []
    zero_answer = db.query("select Count(*) from UserInfo where PersonalAnswerCount=0")
    for zero in zero_answer:
        values.append(zero['Count(*)'])
    two_answer = db.query("select Count(*) from UserInfo where PersonalAnswerCount>0 and GetAwardCount>0")
    for two in two_answer:
        values.append(two['Count(*)'])
    three_answer = db.query("select Count(*) from UserInfo where PersonalAnswerCount>0 and GetAwardCount=0")
    for three in three_answer:
        values.append(three['Count(*)'])
    pie = Pie("知乎回答数分布", title_pos='auto')
    pie.add("", classes, values, is_label_show=True)
    return pie


# 获得赞同数用户分布
@debug
def voteup():
    pass

# 知乎赞数最多100位, 及直方图统计


# 知乎关注数图top100
@debug
def follow():
    follows = []
    counts = []
    location = db.query("select Name,FollowedCount from UserInfo order by FollowedCount DESC LIMIT 100")
    for loca in location:
        follows.append(loca['Name'])
        counts.append(loca['FollowedCount'])
    wordcloud = WordCloud("关注数top100词云", width=1300, height=620)
    wordcloud.add("", follows, counts, word_size_range=[20, 100], shape='diamond')
    # wordcloud.render()
    # pass
    return wordcloud

# 回答问题最多top100


# 均值统计, 回答数, 提问数, 点赞数, 被关注量, 关注量, 感谢数
@debug
def avg_info():
    bar = Bar("均值统计")
    classes = ['回答数', '提问数', '赞同数', '感谢数', '被关注量', '关注量']
    names = ['PersonalAnswerCount', 'PersonalQuestionCount', 'GetAwardCount', 'GetThanksCount',
             'FollowedCount', 'FollowingCount']
    counts = []
    besides_counts = []
    for name in names:
        sql = 'select avg({}) as info from UserInfo where {}!=0'.format(name, name)
        rows = db.query(sql)
        for row in rows:
            counts.append(int(row['info']))
    for name in names:
        sql = 'select avg({}) as info from UserInfo where {}!=0 and FollowedCount>10000'.format(name, name)
        rows = db.query(sql)
        for row in rows:
            besides_counts.append(int(row['info']))
    bar.add("所有", classes, counts, is_convert=True)
    bar.add("大v", classes, besides_counts, is_convert=True)
    # bar.render()
    # pass
    return bar


# 总值统计
@debug
def sum_info():
    bar = Bar("总值统计")
    classes = ['回答数', '提问数', '赞同数', '感谢数', '被关注量', '关注量']
    names = ['PersonalAnswerCount', 'PersonalQuestionCount', 'GetAwardCount', 'GetThanksCount',
             'FollowedCount', 'FollowingCount']
    counts = []
    besides_counts = []
    for name in names:
        sql = 'select sum({}) as info from UserInfo where {}!=0'.format(name, name)
        rows = db.query(sql)
        for row in rows:
            counts.append(int(row['info']))
    for name in names:
        sql = 'select sum({}) as info from UserInfo where {}!=0 and FollowedCount>1000'.format(name, name)
        rows = db.query(sql)
        for row in rows:
            besides_counts.append(int(row['info']))
    bar.add("所有", classes, counts, is_convert=True)
    bar.add("大v", classes, besides_counts, is_convert=True)
    # bar.render()
    return bar
    pass


# 漏斗图生成
@debug
def parse():
    attr = ["回答者", "注册读者", "未注册,日报精选读者", "其他媒体转载读者"]
    value = [20, 40, 60, 80]
    funnel = Funnel("知乎传播路径")
    funnel.add("", attr, value, is_label_show=True,
               label_pos="inside", label_text_color="#fff")
    # funnel.render()
    return funnel


'''职业分析'''


# 职业分布直方图
@debug
def work():
    works = db.query("select  Work ,Count(*) from UserInfo where Work!='' "
                     "group by Work order by Count(*) DESC LIMIT 1,10")
    locas = []
    counts = []
    for loca in works:
        locas.append(loca['Work'])
        counts.append(loca['Count(*)'])
    bar = Bar("知乎用户职业分布")
    bar.add("", locas, counts, label_color=['rgba(0,0,0,0)'], is_stack=True)
    bar.add("职业", locas, counts, is_label_show=True, is_stack=True, xaxis_rotate=90, xaxis_label_textsize=9)
    return bar


# 职业词云
@debug
def work_graph():
    works = []
    counts = []
    location = db.query("select  Work ,Count(*) from UserInfo where Work!='' "
                        "group by Work order by Count(*) DESC LIMIT 60")
    for loca in location:
        works.append(loca['Work'])
        counts.append(loca['Count(*)'])
    wordcloud = WordCloud("职业词云", width=1300, height=620)
    wordcloud.add("", works, counts, word_size_range=[20, 100], shape='diamond')
    # wordcloud.render()
    return wordcloud
    pass


# 职业地区热力图
@debug
def work_heatmap():
    x_axis = []
    y_axis = []
    data = []
    xs = db.query("select Work, Count(*) from UserInfo where Work!='' group by Work order by Count(*) DESC LIMIT 1,8")
    for x in xs:
        x_axis.append(x['Work'])
    ys = db.query("select Location, Count(*) from UserInfo where Location!='' "
                  "group by Location order by Count(*) DESC LIMIT 10")
    for y in ys:
        y_axis.append(y['Location'])
    for xw in x_axis:
        for yw in y_axis:
            cs = db.query("select Count(*) from UserInfo where Work='{}' and Location='{}'".format(xw, yw))
            for css in cs:
                count = css['Count(*)']
            data.append([xw, yw, count])
    heatmap = HeatMap()
    heatmap.add("职业热力图", x_axis, y_axis, data, is_visualmap=True,
                visual_text_color="#000", visual_orient='horizontal',
                visual_range_color=['#FFFFFF', '#32CD32', '#548B54'])
    # heatmap.render()
    return heatmap
    pass


'''知乎高校分析'''


# 高校获得赞数TOP10
@debug
def vote():
    education = db.query("select Education , sum(GetAwardCount) from UserInfo where Education!='' "
                         "group by Education order by sum(GetAwardCount) DESC Limit 1, 11")
    educs = []
    counts = []
    for educ in education:
        educs.append(educ['Education'])
        counts.append(int(educ['sum(GetAwardCount)']))
    bar = Bar("知乎用户高校赞数Top10", height=500)
    bar.add("", educs, counts, label_color=['rgba(0,0,0,0)'], is_stack=True)
    bar.add("高校", educs, counts, is_label_show=True, is_stack=True, label_pos='inside', xaxis_rotate=35,
            xaxis_label_textsize=9)
    # bar.render()
    return bar


# 活跃高校统计, 统计标准 回答数+提问数
@debug
def active():
    education = db.query("select Education , sum(PersonalAnswerCount+PersonalQuestionCount) as info from UserInfo"
                         " where Education!=''  group by Education order by info DESC Limit 1, 11")
    educs = []
    counts = []
    for educ in education:
        educs.append(educ['Education'])
        counts.append(int(educ['info']))
    bar = Bar("知乎用户高校赞数Top10", height=500)
    bar.add("", educs, counts, label_color=['rgba(0,0,0,0)'], is_stack=True)
    bar.add("高校", educs, counts, is_label_show=True, is_stack=True, label_pos='inside', xaxis_rotate=35,
            xaxis_label_textsize=9)
    # bar.render()
    return bar


# 高校词云
@debug
def education_graph():
    works = []
    counts = []
    location = db.query("select  Education ,Count(*) from UserInfo where Education!='' "
                        "group by Education order by Count(*) DESC LIMIT 50")
    for loca in location:
        works.append(loca['Education'])
        counts.append(loca['Count(*)'])
    wordcloud = WordCloud("高校词云", width=1300, height=620)
    wordcloud.add("", works, counts, word_size_range=[20, 100], shape='diamond')
    # wordcloud.render()
    # pass
    return wordcloud


# 高校地区热力图
@debug
def education_heatmap():
    x_axis = ['北京', '上海', '广州', '西安', '成都']
    y_axis = []
    data = []
    for x in x_axis:
        rows = db.query("select Education, Count(*)  from UserInfo where Location='{}' and Education!='' and "
                        "Education!='大学' group by Education order by Count(*) DESC LIMIT 5".format(x))
        for row in rows:
            y_axis.append(row['Education'])
            data.append([row['Education'], x, row['Count(*)']])
    heatmap = HeatMap("地区活跃高校top5")
    heatmap.add("高校", y_axis, x_axis, data, is_visualmap=True,
                visual_text_color="#000", visual_orient='vertical',
                visual_range_color=['#FFFFFF', '#32CD32', '#548B54'],
                xaxis_rotate=40,
                xaxis_label_textsize=7
                )
    # heatmap.render()
    return heatmap


# 大V关系链
@debug
def relation():
    node = []
    nodes = []
    links = []
    rows = db.query("select Token from Relation")
    for row in rows:
        name = db.query("select Name from Relation where Token='{}'".format(row['Token']))
        for na in name:
            node.append(na['Name'])
    node = list(set(node))
    for some in node:
        nodes.append({'name': some})

    columns = db.query("select Token, Relation from Relation")
    for column in columns:
        snames = db.query("select Name from Relation where Token='{}'".format(column['Token']))
        for sname in snames:
            source = sname['Name']
        tnames = db.query("select Name from Relation where Token='{}'".format(column['Relation']))
        for tname in tnames:
            target = tname['Name']
        links.append({'source': source, 'target': target})
    graph = Graph("用户关系图", width=1500, height=1000)
    graph.add("", nodes, links, lable_pos='right', graph_repulsion=50, is_legend_show=False,
              line_curve=0.2, label_text_color='#4876FF', label_emphasis_textcolor='#4876FF')
    graph.render('relation.html')
    pass


'''知乎话题部分'''


# 话题词云
@debug
def topic_graph():
    topics = []
    counts = []
    location = db.query("select TopicName , FollowedCount from Topics order by FollowedCount DESC LIMIT 100")
    for loca in location:
        topics.append(loca['TopicName'])
        counts.append(loca['FollowedCount'])
    wordcloud = WordCloud("知乎话题词云", width=1300, height=620)
    wordcloud.add("", topics, counts, word_size_range=[20, 100], shape='diamond')
    # wordcloud.render()
    # pass
    return wordcloud
    pass


# 话题直方图
def topic():
    pass


'''知乎专栏部分'''
# 专栏词云

# 专栏直方图


if __name__ == '__main__':
    graphs = [
        gender(),
        work_gender(),
        location_gender(),
        education_gender(),
        location_graph(),
        location(),
        vote(),
        active(),
        education_graph(),
        education_heatmap(),
        work(),
        work_heatmap(),
        work_graph(),
        dead_user(),
        followed(),
        answers(),
        follow(),
        avg_info(),
        sum_info(),
        parse(),
        topic_graph()]
    page = Page()
    page.add(graphs)
    page.render('parse.html')
    relation()
    pass