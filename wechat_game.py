#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import _thread
import json

import itchat
from itchat.content import *
from service import game_service
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


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    global group_user_name
    from_user_name = msg['User']['UserName']
    if from_user_name == group_user_name:
        # print(json.dumps(msg))
        # 找到真实的用户
        nick_name = ''
        user_name = msg['ActualUserName']
        member_list = msg['User']['MemberList']
        for member in member_list:
            if member['UserName'] == msg['ActualUserName']:
                nick_name = member['NickName']
                break

        content = msg['Content']
        print(u'@%s\u2005 : %s' % (nick_name, content))
        if content.startswith('attack') or content.startswith('use'):
            attack_result = game_service.attack(user_name=user_name, content=content, group_user_name=group_user_name)  # 进行攻击
            print(attack_result)
            if attack_result["code"] != -1:
                attack_result_info = ""
                if attack_result["code"] == 0:
                    # 攻击成功
                    damage_type = attack_result["damage_type"]
                    damage_to = attack_result["damage_to"]
                    damage = attack_result["damage"]
                    damage_times = attack_result["damage_times"]
                    rest_hp = attack_result["rest_hp"]
                    if damage_type == 1:
                        # 普通攻击
                        attack_result_info = '[信息][普通伤害]' + nick_name + '对' + damage_to + '造成了' + str(int(damage)) + '点伤害'
                    elif damage_type == 2:
                        #暴击
                        attack_result_info = '[信息][' + str(damage_times) + '倍暴击]' + nick_name + '对' + damage_to + '造成了' + str(damage) + '点暴击伤害'
                    attack_result_info = attack_result_info + "\n" + damage_to + "剩余血量:" + str(rest_hp) + "/500"
                    isDead = attack_result['isDead']
                    if isDead:
                        # 击杀
                        attack_result_info = attack_result_info + "\n" + nick_name + "杀死了" + damage_to + "！"
                else:
                    # 攻击失败
                    attack_result_info = '[信息]['+nick_name+'攻击失败]' + attack_result['msg']
                # 发送消息
                print(attack_result_info)
                itchat.send(attack_result_info, from_user_name)
        elif content == "info":
            result = game_service.info(group_user_name=group_user_name)
            info = "所有群员的血量信息如下："
            for k, v in result.items():
                info = info + "\n" + k + " : " + v
            print(info)
            itchat.send(info, from_user_name)
        elif content == "myinfo":
            result = game_service.my_info(user_name=user_name)
            info = "用户["+nick_name+"]的信息如下："
            for k, v in result.items():
                info = info + "\n" + k + " : " + v
            print(info)
            itchat.send(info, from_user_name)
        elif content == "help":
            info = "命令列表\n"
            info = info + "攻击：attack AtXXX\n"
            info = info + "群员信息：info\n"
            info = info + "我的信息：myinfo\n"
            info = info + "帮助：help"
            print(info)
            itchat.send(info, from_user_name)


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
    # try:
    #     _thread.start_new_thread(print_time, ("Thread-1", 2,))
    # except:
    #     print("Error: 无法启动线程")
    itchat.run()
