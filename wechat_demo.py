#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import _thread
import json
import random
import time

import itchat
from bs4 import BeautifulSoup
from itchat.content import *

from dao import mysql_dao

# 要监听的群的UserName
global group_user_name
group_user_name = ""


# 定义键盘输入线程
def print_time( threadName, delay):
   while True:
        say = input()
        # print(say)
        itchat.send(say, group_user_name)


@itchat.msg_register([NOTE], isGroupChat=True)
def text_reply(msg):
    global group_user_name
    # print(msg)
    if msg['MsgType'] == 10002 and msg['FromUserName'] == group_user_name:
        # 这个表示撤回一条信息，我们拦截这个，再去数据库里找被拦截的那条语句
        Content = msg['Content']
        soup = BeautifulSoup(Content, 'html.parser')
        msgid = soup.find('msgid').get_text()
        # print("撤回了{}这条信息".format(msgid))
        data = mysql_dao.find_log_by_msg_id(msgid)
        for d in data:
            print(u"{}撤回了'{}'这条信息".format(d[0], d[1]))
            itchat.send('%s撤回了"%s"这条信息' % (d[0], d[1]), group_user_name)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # print(msg)
    itchat.send('你好，我收到了您的消息"%s"，但是我现在不在手机身边，稍后我会联系您~' % (msg['Text']), msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # print(json.dumps(msg))
    global group_user_name
    from_user_name = msg['User']['UserName']
    # print(u'%s,%s' % (msg['User']['UserName'], group_user_name))
    if from_user_name == group_user_name:
        # 找到真实的用户
        nick_name = ''
        member_list = msg['User']['MemberList']
        for member in member_list:
            if member['UserName'] == msg['ActualUserName']:
                nick_name = member['NickName']
                break

        Content = msg['Content']
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        mysql_dao.save_chat_log(msg['MsgId'], Content, nick_name, msg['ActualNickName'], msg['User']['NickName'], now)
        print(u'@%s\u2005 : %s' % (nick_name, Content))

        if Content.startswith('attack'):
            conts = Content.split(" ")
            attacked_name = conts[1]
            sh = random.uniform(10, 20)  # 10-20的伤害
            sh = round(sh, 2)

            # 计算暴击 0.2的暴击几率
            if random.random() < 0.2:
                times = sh*random.uniform(2, 10)  # 2到10倍的伤害
                times = round(times, 0)
                sh = sh * times
                print("[", times, "倍伤害]", nick_name, "对", attacked_name, "造成了", str(sh), "点暴击伤害！")
                itchat.send('[%s倍伤害]%s 对 %s 造成了 %s 点暴击伤害！' % (str(times), nick_name, attacked_name, str(sh)), from_user_name)
            else:
                print(nick_name, "对", attacked_name, "造成了", str(sh), "点伤害！")
                itchat.send('%s 对 %s 造成了 %s 点伤害!' % (nick_name, attacked_name, str(sh)), from_user_name)


# @itchat.msg_register(SYSTEM)
# def get_uin(msg):


itchat.auto_login(enableCmdQR=2)

# 获取群id
chatrooms = itchat.get_chatrooms()
x = 0
for chatroom in chatrooms:
    print(x, ":", chatroom['NickName'])
    x += 1
group_number = input("请选择：")

if int(group_number) < 0 or int(group_number) > len(chatrooms)-1:
    print("请输入正确的数字")
else:
    chosen_chatroom = chatrooms[int(group_number)]
    print("选择了群:", chosen_chatroom['NickName'])
    group_user_name = chosen_chatroom['UserName']
    updated_chatroom = itchat.update_chatroom(userName=group_user_name, detailedMember=True)
    print(json.dumps(updated_chatroom))
    MemberList = updated_chatroom['MemberList']
    for menber in MemberList:
        mysql_dao.insert_user(menber=menber, group_user_name=group_user_name, group_nick_name=chosen_chatroom['NickName'])
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
    except:
        print("Error: 无法启动线程")
    itchat.run()
