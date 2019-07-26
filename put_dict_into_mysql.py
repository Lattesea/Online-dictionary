#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 19-7-23 下午7:12 
# @Author : 黄国鑫 
# @File : put_dict_into_mysql.py 
"""
    完整的项目，数据库的搭建需要放在第一位
    # dict.txt文件中的单词与解释导入进数据库，以便于后续操作
"""
import pymysql  # 用该模块操作数据库
import re  # 用正则表达式来匹配txt文件

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='123456',
                     database='dict',
                     charset='utf8'
                     )

f = open('dict.txt')

# 获取游标，其作用是操作数据库，执行sql语句
cur = db.cursor()

# sql执行语句，在里面写上sql语法
sql = "insert into words (word,mean) values(%s,%s)"

for line in f:
    tup = re.findall(r'(\S+)\s+(.*)', line)[0]
    try:
        cur.execute(sql, tup)  # 该函数执行sql语句
        db.commit()  # 提交到数据库
    except:
        db.rollback()  # 这一步很重要，出错可以回滚
f.close()
