#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 19-7-23 下午7:08 
# @Author : 黄国鑫 
# @File : dict_mysql.py 
"""
    如果在服务端程序直接操作数据库，会造成代码的臃肿
    因此将数据库操作单独封装为一个类，各种操作分别写
    成不同的方法，在dict_server中实例化对象，需要
    的时候直接调用
"""
import pymysql


class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 charset='utf8',
                 database=None
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_database()  # 连接数据库

    # 链接数据库
    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset
                                  )

    # 关闭数据库
    def close(self):
        self.db.close()

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 注册操作
    def register(self, name, passwd):
        sql = "select * from user where name+'%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 查找到用户则返回False，因为用户存在需要提醒客户
        if r:
            return False

        # 没有查询到用户说明可以将用户插入数据库
        # 插入数据库
        sql = "insert into user (name,passwd)values(%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        # 查找语句
        sql = "select * from user where name='%s' and passwd='%s'" % (name, passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        # 有数据则允许登录
        if r:
            return True
        else:
            return False

    def query(self, word):
        # 查找语句
        sql = "select * from words where word='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    # 插入历史记录
    # 每次写方法之前要想一下要传入哪些参数
    def insert_hist(self, name, word):
        # 数据库插入语句
        sql = "insert into hist (name,word) values (%s,%s)"
        # 为了避免插入错误导致后续修复困难，
        # 这里需要写异常处理，数据回滚
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()  # 提交到数据库处理
        except Exception:
            self.db.commit()

    # 查询历史记录
    def hist(self, name):
        # 按照降序取出名字单词时间，通过传入用户名
        sql = "select name,word,time from hist where name='s'order by time desc limit 10" % name
        self.cur.execute(sql)
        return self.cur.fetchall()
