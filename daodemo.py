#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'Li Zhengxian'

import pymysql

global conn
try:
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='wechat_game', port=3306, charset='utf8')
    print("与MySQL建立了链接")
except Exception as e:
    print(e)


def insert_user():
    global conn
    try:
        cur = conn.cursor()
        cur.execute('SELECT 1 as a,2 as b,3 as c')
        data = cur.fetchall()
        print(data)
        for d in data:
            print(d[0])
        cur.close()
    except Exception as e:
        print(e)


def save_chat_log(msg_id, content, nickname, actual_nick_name, group_name, time):
    global conn
    try:
        cur = conn.cursor()
        cur.execute('insert into chat_log(msg_id, content, nickname, actual_nick_name, group_name, received_time)VALUE ("%s", "%s","%s", "%s","%s","%s")' % (msg_id, content, nickname, actual_nick_name, group_name, time))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)


def find_log_by_msg_id(msg_id):
    global conn
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT nickname,content from chat_log where msg_id = "{msg_id}"')
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(e)
