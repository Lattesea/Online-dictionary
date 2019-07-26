#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 19-7-23 下午7:07 
# @Author : 黄国鑫 
# @File : 字典客户端.py 
"""
    1.第一步先实现客户端与服务端的网络连接
"""
from socket import *
import sys

# 声明服务端地址
ADDR = ('127.0.0.1', 8000)
# 套接字
s = socket()
s.connect(ADDR)


def do_register():
    while True:
        name = input("User:")
        passwd = input("password:")

        if ' ' in name or ' ' in passwd:
            print("用户名或者密码内不能有空格")
            continue

        msg = "R %s %s" % (name, passwd)  # 将用户名和密码打包
        s.send(msg.encode())  # 转化为字节码发给服务端
        data = s.recv(128).decode()  # 接受客户端信息
        if data == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return


# 登录
def do_login():
    name = input("User：")
    passwd = input("Password：")
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())  # 打包发送给服务器
    data = s.recv(128).decode()  # 接收服务器回复
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")


# 查单词
"""
考虑到后面有查询历史记录的功能，因此可以考虑在查单词的时候
将名字也直接加在发过去的信息中，在服务端数据库生成记录，以
便于后续查询
"""


def do_query(name):
    while True:
        word = input("请输入查找的单词：")
        if word == '##':
            break
        msg = "Q %s %s" % (name, word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)


# 查历史记录
def do_hist(name):
    msg = "H %s" % (name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(4096).decode()
            if data == '##':
                break
            print(data)
    else:
        print("您还没有查询记录")


# 登陆后的二级界面
def login(name):
    while True:
        print("""
                ===============Query==============
                1. 查单词    2. 历史记录     3.注销
                ==================================
                """)
        cmd = input("请输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_hist(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确的选项")


# 在这里可以先写客户端界面，想一下需要实现什么功能
# 先把方法名写出来，后续慢慢补充
def main():
    while True:
        print("""
                ===========Welcome===========
                1. 注册    2. 登录     3.退出
                =============================
                """)
        cmd = input("请输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':  # 退出客户端的时候给服务器发送一个信号，让其结束进程
            s.send(b'E')
            sys.exit("谢谢使用")  # 客户端退出
        else:
            print("请输入正确的选项")


main()  # 启动客户端
