# zhihuspider

基本模块分为5个
1, 验证码处理模块 capture
2, 数据抓取模块 crawler
3, 数据分析模块 dataparse
4, 数据库处理模块 sql
5, 日志收集处理模块 log

下面将简单介绍每个模块下面各个文件的功能和具体实现逻辑,
一, 验证码处理模块 capture
目前尚未处理(参考github zheye), 知乎验证码改变, 此模块作废, 不做处理

二, 数据抓取模块 crawler
1, 登录类Login实现 login.py
   .1 Login 类(返回带登录信息的会话，供给其他模块访问zhihu使用)
    FAQ: 知乎登陆5月份改版, token不在暴露在源码中,而是在请求的第一次set-cookie里

2, 解析类实现  zhihuuser.py , parseall.py
   .1 ParseBasic类(访问抓包接口拿到用户的唯一标识url_token)
   .2 ParseSuccess类(抓取个人成就信息)
   .3 ParseDetail类(个人详细信息)
   .4 ParseUserTag类(解析关注的话题，专栏信息，并做权重处理)
   .5 对解析类进行重构, 用户信息的解析全部在ParseAll类中

3, ip代理池、UA池实现 ipproxy.py
   .1 UaProxy类(利用faker造一个500的UA池，不考虑重复)
   .2 IpProxy类(参考github上的项目haipiproxy)
   FAQ1:一直没搞懂ip代理的校验规则，直接访问目标网站，判断状态码有时候总会不管用
   FAQ2:去掉了ip代理池,只保留UA池

4, 小工具模块实现 tool.py
   .1 delete_comma (用来去除数字信息中的逗号)
   .2 重构了解析类以后, 便没有调用tool

5, 抓取逻辑测试文件 schedule.py
   .1 分别调度User, Topic, Column信息抓取
   .2 程序放在阿里云服务器上后台运行, 默认采用nohup日志

三, 数据分析模块
FAQ1:对introduction, headline,Education进行分词,统计还是学生的数量,哪个学校的最多,也可以以此统计行业分布,也可以统计大家最常用
      的headline关键词，看看有什么有意思的东西
FAQ2:work字段几乎没有, 从introduction 和headline中提取
1, 数据清洗模块cleandata.py
   .1 主要用于清洗Education, Location, Work字段, 从Headline提取补全Work字段
   .2
2, 数据统计可视化模块statistics.py, 可视化部分基于开源的pyecharts

3, querysql.py 主要统计了一些查询信息的sql

四, 日志收集处理模块
1, 由于程序在服务器上后台运行, 可以直接使用nohup
2, 本地直接使用logging模块

五, 数据库处理模块
FAQ1：dataset高层库没有显式的关闭数据库连接的方法，直接继承sqlalchemy的数据连接池复用,这里的原理不太清楚,一定程度上会出现mysql
      1045 error,解决办法是在数据库层面增大连接数，或者改用低层库如pymysql.这个地方还是要搞懂sqlalchemy数据库连接池的原理。
数据库选用Mysql
1, 数据表生成模块 orm.py
2, 数据库操作模块 sqloperate 模块


六, Adding
1, UserInfo 表添加Relation字段, 用于制作人物互相关注图
2, crawler模块添加relation.py , 用于爬取关系图, 暂时不加入调度schedule.py 中
3,数据可视化生成的图表在dataparse目录下的3个html文件中，大V关系链最后的定点中心是知乎的CEO周源,这是个很有意思的东西。
自己没有很好的解决代码的复用
本项目参考：
http://pyecharts.org/
https://zhuanlan.zhihu.com/p/34073256


