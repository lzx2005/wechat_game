#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itchat
import json


def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

# 登录授权
itchat.auto_login(enableCmdQR=2)
# 获取好友列表
friends = itchat.get_friends(update=True)


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
friends = MemberList

# 分析

# f = open("friend.log", "w")
# f.write(json.dumps(friends))
# f.close()
# print(json.dumps(friends))
man = 0
woman = 0
citys = {}
for friend in friends:
    if man == 1:
        print(json.dumps(friend))

    if friend['Sex'] == 1:
        #男人
        man += 1
    else:
        #女人
        woman += 1
    city = friend['City']
    province = friend['Province']
    if len(city) > 0:
        city_sum = citys.get(city, 0)
        city_sum += 1
        citys[city] = city_sum
    elif len(province) > 0:
        city_sum = citys.get(province, 0)
        city_sum += 1
        citys[province] = city_sum

text = ""
print("该群中，男生共有", man, "人，女生共有", woman, "人\n男女比例为", man/woman)
text += " ".join(["该群中，男生共有", str(man), "人，女生共有", str(woman), "人\n男女比例为", str(man/woman), "\n"])
dict = sorted(dict2list(citys), key=lambda x: x[1], reverse=True)
for item in dict:
    print("来自", item[0], "的共有：", item[1], "人")
    text += " ".join(["来自", str(item[0]), "的共有：", str(item[1]), "人", "\n"])

itchat.send(text, 'filehelper')


#
#
# contact = itchat.get_contact(update=True)
# f = open("contact.log", "w")
# f.write(json.dumps(contact))
# f.close()
#
#
# mps = itchat.get_mps(update=True)
# f = open("mps.log", "w")
# f.write(json.dumps(mps))
# f.close()
