# Online-dictionary
============================================
## 项目简介
这是适合新手练习的小项目，一个不掺杂其他内容的简易英英词典，主要实现的功能：客户端输入需要查询的单词，然后自动发送给服务端，服务端返回单词释义给客户端。

## 配置信息
* python3 推荐使用pycharm或者vscode作为集成开发工具.
* Mysql数据库
* Ubuntu 18.04.2 LTS
* python模块 socket，sys，multiprocessing,signal,time,pymysql
> socket : 套接字,是应用层与传输层(TCP/UDP协议)的接口。是对TCP/IP的封装。是操作系统的通信机制。应用程序通过socket进行网络数据的传输。Python中的socket是我们常用的模块，当然还有socketserver模块（对socket模块的进一步封装）

> sys : 提供访问解释器使用或维护的变量，和与解释器进行交互的函数。通俗来讲，sys模块负责程序与python解释器的交互，提供了一系列的函数和变量，用于操控python运行时的环境。

> multiprocessing : multiprocessing是一个管理进程的包，这里主要引用其中的Process模块，该模块是一个创建进程的模块

> signal : 信号模块，该模块主要用于进程间通讯，在这里主要用它来处理僵尸进程或者孤儿进程，值得注意的是这个模块window系统上面是不支持的

> time : 时间模块，这里主要用其中的子模块sleep,用于传送数据时认为添加时间延迟，避免粘包

> pymysql : python中的数据库操作模块，用于程序与数据库之间的交互

## 技术方案
* TCP套接字
* 多进程
* 历史记录查询，返回前十条记录
* 注册成功之后直接登录

## 数据库创建
> 创建数据库 dict  （utf8）

> 单词 words  ->id word mean
create table words (id int primary key auto_increment,word char(32),mean text);

> 用户 user -> id  name  passwd
   create table user (id int primary key auto_increment,name varchar(32) not null,passwd varchar(128) not null);

> 历史记录 hist-> id name  word  time
   create table hist (id int primary key auto_increment,name varchar(32) not null, word varchar(28) not null,time datetime default now() );

## 功能分析 和 通信搭建

>并发通信
登录
注册
查单词
历史记录

## 客户端服务端协议

>注册   R
登录   L
查单词  Q
历史记录  H
退出  E

## 功能逻辑 
每个功能确定服务端和客户端该做什么，编写代码测试

#### 注册  
>客户端： 
>* 输入注册信息
>* 发送请求 R+name+password
>* 得到反馈

>服务端 : 
>* 接收请求
>* 判断是否允许注册
>* 允许注册将信息存入数据库
>* 给客户端反馈结果

#### 登录  
> 客户端： 
>* 输入用户名密码 
>* 发送请求给服务器 L+name+password
>* 得到服务器反馈

>服务端： 
>* 接收请求
>* 判断是否允许登录
>* 发送结果

#### 查单词 
>客户端： 
>* 输入单词
>* 发送请求 Q+name+word
>* 等待接收结果

>服务端： 
>* 接收请求
>* 查找单词
>* 发送结果
>* 插入历史记录

####查历史记录
>客户端：
>* 发送请求 H+name
>* 等待接受结果
>* 得到服务器反馈

>服务端：
>* 接受请求
>* 判断是否有历史记录
>* 查找历史记录
>* 返回前十条结果

## 后续可追加功能
>* 密码屏蔽：有时为了防止别人看到，输入的时候隐藏内容
>* 密码加密：在存入数据库的时候对密码进行加密，防止非用户可以在数据库直看到用户及密码的情况
