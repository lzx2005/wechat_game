#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'Li Zhengxian'

import pymysql

global conn

import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='wechat_game', port=3306, charset='utf8mb4')
print("与MySQL建立了链接")


def insert_user(menber, group_user_name, group_nick_name):
    global conn
    try:
        cur = conn.cursor()
        sql = 'insert into user(userName,nickName,remarkName,displayName,hp,power,level,exp,groupUserName,groupNickName,minDamage,maxDamage,lastAttack)VALUE ("%s", "%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s")'
        sql = sql + 'ON DUPLICATE KEY UPDATE\n'
        sql = sql + 'userName =  "%s",\n'
        sql = sql + 'groupUserName =  "%s",\n'
        sql = sql + 'groupNickName = "%s"\n'
        sql = sql % (
            menber['UserName'],
            menber['NickName'],
            menber['RemarkName'],
            menber['DisplayName'],
            500,
            24,
            1,
            0,
            group_user_name,
            group_nick_name,
            1,
            10,
            0,
            menber['UserName'],
            group_user_name,
            group_nick_name,
        )
        # print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)


def save_chat_log(msg_id, content, nickname, actual_nick_name, group_name, time):
    global conn
    try:
        cur = conn.cursor()
        cur.execute('insert into chat_log(msg_id, content, nickname, actual_nick_name, group_name, received_time)VALUE ("%s", "%s","%s", "%s","%s","%s")' % (
            msg_id,
            content,
            nickname,
            actual_nick_name,
            group_name,
            time
        ))
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
