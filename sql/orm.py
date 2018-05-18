# encoding:utf-8

'''
use sqlalchemy to create table
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, TEXT, TIMESTAMP

engine = create_engine('mysql+pymysql://root:root@localhost:3306/zhihu?charset=utf8')
Base = declarative_base()


# 用户token表 已经和userinfo表进行了合表
class UserToken(Base):
    __tablename__ = 'UserToken'
    RecId = Column(Integer,autoincrement=True, nullable=False, primary_key=True)
    id = Column(String(128), primary_key=True, index=True)
    Token = Column(String(128), nullable=False, index=True)
    Name = Column(String(128), nullable=False)
    FollowerCount = Column(Integer, nullable=True)
    CreatTime = Column(TIMESTAMP(True), nullable=False)
    pass


# 用户主要信息
class UserInfo(Base):
    __tablename__ = 'UserInfo'
    RecId = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    id = Column(String(128), nullable=False)
    Name = Column(String(128), index=True)
    Token = Column(String(128), nullable=False, index=True, unique=True)
    HeadLine = Column(String(512), nullable=True)
    Introduction = Column(String(1024), nullable=True)
    Education = Column(String(64))
    Major = Column(String(64))
    Business = Column(String(64))
    Work = Column(String(64))
    CoverUrl = Column(String(512), nullable=True)
    HeadImg = Column(String(512), nullable=True)
    Location = Column(String(64), nullable=True)
    Badge = Column(String(64), nullable=True)
    Gender = Column(Integer)
    PersonalAnswerCount = Column(Integer)
    PersonalQuestionCount = Column(Integer)
    PersonalArticlesCount = Column(Integer)
    PersonalColumnCount = Column(Integer)
    PersonalIdeasCount = Column(Integer)
    FollowedCount = Column(Integer)
    FollowingCount = Column(Integer)
    CollectAnswersCount = Column(Integer)
    CollectArticlesCount = Column(Integer)
    GetAwardCount = Column(Integer)
    GetThanksCount = Column(Integer)
    GetCollectCount = Column(Integer)
    PublicEditeCount = Column(Integer)
    TakeLiveCount = Column(Integer)
    SproveLiveCount = Column(Integer)
    ParticuteLiveCount = Column(Integer)
    FollowTopicCount = Column(Integer)
    FollowColumnCount = Column(Integer)
    FollowQuestionsCount = Column(Integer)
    FollowCollectCount = Column(Integer)
    FollowTopics = Column(TEXT)
    FollowColumns = Column(TEXT)
    Url = Column(String(512))
    CreateTime = Column(TIMESTAMP(True), nullable=False)
    LastModifyTime = Column(DateTime)
    pass


# 知乎专栏信息表
class Columns(Base):
    __tablename__ = 'Columns'
    RecId = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    Columnid = Column(String(64), index=True, primary_key=True, unique=True)
    ColumnName = Column(String(64), index=True)
    Permission = Column(String(32))
    ColumnAuthor = Column(String(128))
    Introduction = Column(String(1024))
    HeadImg = Column(String(512))
    FollowedCount = Column(Integer)
    ArticleCount = Column(Integer)
    Url = Column(String(512))
    UpdateTime = Column(DateTime)
    CreateTime = Column(TIMESTAMP(True), nullable=False)
    LastModifyTime = Column(DateTime)
    pass


# 知乎话题信息表
class Topics(Base):
    __tablename__ = 'Topics'
    RecId = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    TopicId = Column(String(64), index=True, primary_key=True, unique=True)
    TopicName = Column(String(64))
    HeadImg = Column(String(512))
    Introduction = Column(String(1024))
    TopicQuestionsCount = Column(Integer)
    FollowedCount = Column(Integer)
    GoodAnswersCount = Column(Integer)
    GoodAnswerersCount = Column(Integer)
    Url = Column(String(512))
    CreateTime = Column(TIMESTAMP(True), nullable=False)
    LastModifyTime = Column(DateTime)
    pass


# 新增大V用户关系表relation, 最后和UserInfo合表
class Relation(Base):
    __tablename__ = 'Relation'
    RecId = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    id = Column(String(128), nullable=False)
    Name = Column(String(128), index=True)
    Token = Column(String(128), nullable=False, index=True)
    HeadLine = Column(String(512), nullable=True)
    Introduction = Column(String(1024), nullable=True)
    Education = Column(String(64))
    Major = Column(String(64))
    Business = Column(String(64))
    Work = Column(String(64))
    CoverUrl = Column(String(512), nullable=True)
    HeadImg = Column(String(512), nullable=True)
    Location = Column(String(64), nullable=True)
    Badge = Column(String(64), nullable=True)
    Gender = Column(Integer)
    PersonalAnswerCount = Column(Integer)
    PersonalQuestionCount = Column(Integer)
    PersonalArticlesCount = Column(Integer)
    PersonalColumnCount = Column(Integer)
    PersonalIdeasCount = Column(Integer)
    FollowedCount = Column(Integer)
    FollowingCount = Column(Integer)
    CollectAnswersCount = Column(Integer)
    CollectArticlesCount = Column(Integer)
    GetAwardCount = Column(Integer)
    GetThanksCount = Column(Integer)
    GetCollectCount = Column(Integer)
    PublicEditeCount = Column(Integer)
    TakeLiveCount = Column(Integer)
    SproveLiveCount = Column(Integer)
    ParticuteLiveCount = Column(Integer)
    FollowTopicCount = Column(Integer)
    FollowColumnCount = Column(Integer)
    FollowQuestionsCount = Column(Integer)
    FollowCollectCount = Column(Integer)
    FollowTopics = Column(TEXT)
    FollowColumns = Column(TEXT)
    Url = Column(String(512))
    CreateTime = Column(TIMESTAMP(True), nullable=False)
    LastModifyTime = Column(DateTime)
    Relation = Column(String(128))
    pass


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    pass
