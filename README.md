# 知乎用户爬虫

## 具体的使用请见目录下的development 文档

## 数据流
1. Login 登录类 -> 生成登录会话
2. ParseBasic -> 生成用户token
3. ParseAll -> 接收token,遍历用户信息, 顺带解析话题, 专栏信息(此处冗余比较大,应拆分)
4. Schedule -> 调度爬取并入库(谈不上调度, 就是相当于主函数)

## 数据字段
### 用户信息表(UserInfo)
| 字段              |   描述        |
|------------------|---------------|
|RecId             | 自增id         |
|id                | 用户ID          |
|Name              | 用户名         |
|Token             | 用户token值    |
|HeadLine          | 一句话介绍      |
|Introduction      | 简介           |
|Education         | 教育程度        |
|Major             | 主修           |
|Business          | 行业           |
|Work              | 工作           |
|CoverUrl          | 封面图         |
|HeadImg           | 头像           |
|Location          | 地区           |
|Badge             | 个人勋章        |
|Gender            | 性别          |
|PersonalAnswerCount | 个人回答数   |
|PersonalQuestionCount | 个人问题数  |
|PersonalArticlesCount | 个人文章数   |
|PersonalColumnCount  | 个人专栏数    |
|PersonalIdeasCount   | 个人想法数    |
|FollowedCount        | 被关注数        |
|FollowingCount       | 关注数         |
|CollectAnswersCount  | 被知乎收录回答数 |
|CollectArticlesCount | 收录文章数    |
|GetAwardCount        | 获得赞同数    |
|GetThanksCount       | 获得感谢数    |
|GetCollectCount      | 获得收藏数    |
|PublicEditeCount     | 公共编辑数    |
|TakeLiveCount        | 参与live数    |
|SproveLiveCount      | 赞助live数    |
|ParticuteLiveCount    | 参与live数   |
|FollowTopicCount    | 关注话题数      |
|FollowColumnCount    | 关注专栏数     |
|FollowQuestionsCount | 关注问题数     |
|FollowCollectCount   | 关注收藏数     |
|FollowTopics         | 关注哪些话题   |
|FollowColumns         | 关注哪些专栏  |
|Url                  | url          |
### 话题信息表(Topic)
| 字段              |   描述        |
|------------------|---------------|
|Columnid          | 专栏id        |
|ColumnName        | 专栏名称      |
|Permission        | 是否允许公开   |
|ColumnAuthor      | 专栏发起者    |
|Introduction       | 专栏简介     |
|HeadImg           | 专栏头像      |
|FollowedCount     | 关注数        |
|ArticleCount      | 专栏文章数     |
|Url               | url          |
|UpdateTime        | 专栏更新时间   |
### 专栏信息表(Column)
| 字段              |   描述        |
|------------------|---------------|
|TopicId           | 话题id        |
|TopicName         | 话题名称     |
|HeadImg           | 话题头像     |
|Introduction       | 话题简介    |
|TopicQuestionsCount | 话题问题数  |
|FollowedCount     | 关注数      |
|GoodAnswersCount  | 优秀回答数  |
|GoodAnswerersCount| 优秀回答者数 |
|Url               | url         |

### 大v关系链表(relation), 同用户信息表字段一致,只不过加了relation字段用于标识用户间的关系

## 数据分析报告

1. 具体请见我写的知乎文章 https://zhuanlan.zhihu.com/p/38926273

## 本项目参考
1. http://pyecharts.org

2. https://zhuanlan.zhihu.com/p/34073256


