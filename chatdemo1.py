import itchat
import re, sys, json,time
from itchat.content import *
import daodemo

#要监听的群的UserName
global group_user_name
group_user_name = ""


@itchat.msg_register([NOTE], isGroupChat=True)
def text_reply(msg):
    print(msg)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    #print(msg)
    itchat.send('你好，我收到了您的消息"%s"，但是我现在不在手机身边，稍后我会联系您~' % (msg['Text']), msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    global group_user_name
    from_user_name = msg['User']['UserName']
    #print(u'%s,%s' % (msg['User']['UserName'], group_user_name))
    if from_user_name == group_user_name:
        #找到真实的用户
        nick_name = ''
        member_list = msg['User']['MemberList']
        for member in member_list:
            if member['UserName'] == msg['ActualUserName']:
                nick_name = member['NickName']
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        daodemo.save_chat_log(msg['MsgId'], msg['Content'], msg['ActualNickName'], nick_name, msg['User']['NickName'], now)
        print(u'@%s\u2005 : %s' % (nick_name, msg['Content']))


# @itchat.msg_register(SYSTEM)
# def get_uin(msg):


itchat.auto_login(enableCmdQR=2)

#获取群id
chatroom = itchat.search_chatrooms(name='只要我绝对，尬聊没有极限')
group_user_name = chatroom[0]['UserName']

itchat.run()
