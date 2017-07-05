#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import _thread
import itchat
import re, sys, json, time, random
from itchat.content import *
import mysql_dao

# 要监听的群的UserName
global group_user_name
group_user_name = ""


# 定义键盘输入线程
def print_time( threadName, delay):
   while True:
        say = input()
        # print(say)
        itchat.send(say, group_user_name)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    global group_user_name
    from_user_name = msg['User']['UserName']
    # print(u'%s,%s' % (msg['User']['UserName'], group_user_name))
    if from_user_name == group_user_name:
        print(json.dumps(msg))
        # 找到真实的用户
        nick_name = ''
        member_list = msg['User']['MemberList']
        for member in member_list:
            if member['UserName'] == msg['ActualUserName']:
                nick_name = member['NickName']
                break

        Content = msg['Content']
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