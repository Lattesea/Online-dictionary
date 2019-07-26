#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 19-7-23 下午7:07 
# @Author : 黄国鑫 
# @File : 字典服务端.py
"""
    涉及到网络的项目，一般先从服务端下手
    需要用到套接字，考虑到面对很多人使用，这时候就需要
    多并发，这里采用多线程，然后遇到线程就要考虑到僵尸
    进程和孤儿进程问题，直接引入信号模块，将之交给系统
    解决
"""
from socket import *
from multiprocessing import Process
import signal
from time import sleep
from mysql import Database
import sys

# 全局变量
# 后面会经常用到的变量将之提取到前面作为全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)
# 建立数据库对象
db = Database(database='dict')


# 服务端注册处理
def do_register(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    # 返回True表示注册成功，False表示失败
    if db.register(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')


# 服务端登录
def do_login(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')


def do_query(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    mean = db.query(word)

    # 插入历史记录
    # 记录包括所查的单词和用户名
    db.insert_hist(name, word)

    # 下面判断，没有单词就返回None，查到就返回单词和解释给客户端
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s %s" % (word, mean)
        c.send(msg.encode())


def do_hist(c, data):
    tmp = data.split(' ')
    name = tmp[1]
    r = db.history(name)
    if not r:
        c.send(b'Fail')
        return
    c.send(b'OK')

    for i in r:
        msg = "%s %-16s %s" % i
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b"##")


# 具体处理客户端请求
def request(c):
    db.create_cursor()  # 每个子进程单独生成游标
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'E':
            sys.exit()  # 对应子进程退出
        elif data[0] == 'R':
            do_register(c, data)
        elif data[0] == 'L':
            do_login(c, data)
        elif data[0] == 'Q':
            do_query(c, data)
        elif data[0] == 'H':
            do_hist(c, data)


# 优先级第二的就是服务端与客户端的网络搭建
# 创建服务端并发网络
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)  # 绑定地址
    s.listen(5)  # 监听套接字,括号内设置监听队列大小

    # 遇到线程需要考虑孤儿僵尸进程的问题
    # 直接交给系统处理最方便
    # 引用signal模块
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环接收客户端连接
    print("Listen the port 8000")  # 这里是接法的端口
    while True:
        # 异常处理
        try:
            c, addr = s.accept()  # 阻塞等待处理客户端请求
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()  # 关闭套接字
            db.close()  # 关闭游标
            sys.exit("服务器退出")  # 退出系统进程
        except Exception as e:
            print("Error:", e)
            continue

        # 为客户端创建子进程
        # 这里很重要，如果不创建子进程的话无法发送数据给客户端
        # 继而出现客户端输入用户名密码然后程序就一直卡在那里
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()


main()  # 启动程序
