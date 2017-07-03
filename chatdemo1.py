#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import re, sys, json, time, random
from itchat.content import *
import daodemo
from bs4 import BeautifulSoup

# 要监听的群的UserName
global group_user_name
group_user_name = ""


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
        data = daodemo.find_log_by_msg_id(msgid)
        for d in data:
            print(u"{}撤回了'{}'这条信息".format(d[0].decode(encoding='utf-8'), d[1].decode(encoding='utf-8')))
            itchat.send('%s撤回了"%s"这条信息' % (d[0].decode(encoding='utf-8'), d[1].decode(encoding='utf-8')), msg['FromUserName'])


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
        daodemo.save_chat_log(msg['MsgId'], Content, nick_name, msg['ActualNickName'], msg['User']['NickName'],
                              now)
        print(u'@%s\u2005 : %s' % (nick_name, Content))

        if Content.startswith('attack'):
            conts = Content.split(" ")
            attacked_name = conts[1]
            sh = random.uniform(10, 2000)
            sh = round(sh, 2)
            print(nick_name, "对", attacked_name, "造成了", str(sh), "点伤害")
            itchat.send('%s 对 %s 造成了 %s 点伤害' % (nick_name, attacked_name, str(sh)), from_user_name)


# @itchat.msg_register(SYSTEM)
# def get_uin(msg):


itchat.auto_login(enableCmdQR=2)

# 获取群id
# group_name = "距离血祭全群还有七天"
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
    itchat.run()
