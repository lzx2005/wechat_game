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


# 根据userName找到某一个用户
def find_user_by_user_name(user_name):
    global conn
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * from user where userName = "{user_name}" limit 0,1')
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(e)


# 根据name找到某一个用户，这个name有可能是displayName或者是nickName
def find_user_by_name(name, group_user_name):
    global conn
    print(name)
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT * from user where displayName = "{name}" and groupUserName = "{group_user_name}" limit 0,1')
        data = cur.fetchall()
        cur.close()
        if len(data) < 1:
            cur = conn.cursor()
            cur.execute(
                f'SELECT * from user where nickName = "{name}" and groupUserName = "{group_user_name}" limit 0,1'
            )
            data = cur.fetchall()
            cur.close()
            print(data)
            return data
        else:
            print(data)
            return data
    except Exception as e:
        print(e)


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


# 对某人造成伤害
def give_damage(attacker_id, attacked_id, damage, last_attack, now_hour, group_user_name):
    global conn
    try:
        cur = conn.cursor()
        if last_attack >= now_hour:
            # 还在当前时间内
            cur.execute('update user set attack_num = attack_num+1 where id = "%s" and groupUserName = "%s"' % (attacker_id, group_user_name))
        else:
            # 更新新的时间
            cur.execute(
                'update user set lastAttack = "%s",attack_num = 1 where id = "%s" and groupUserName = "%s"' % (now_hour, attacker_id, group_user_name)
            )
        cur.execute(
            'update user set hp = "%s" where id = "%s" and groupUserName = "%s"' % (damage, attacked_id, group_user_name)
        )
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)


def find_all_user_by_group_user_name(group_user_name):
    global conn
    try:
        cur = conn.cursor()
        sql = f'SELECT * from user where groupUserName = "{group_user_name}"'
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        print(e)

# give_damage(72, 73, 10, 17, 18)
