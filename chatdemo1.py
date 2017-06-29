import itchat
import re, sys, json
from itchat.content import *

group_user_name = ""


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    itchat.send('你好，我收到了您的消息"%s"，但是我现在不在手机身边，稍后我会联系您~' % (msg['Text']), msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    print(u'%s,%s' % (msg['FromUserName'], group_user_name))
    from_user_name = msg['FromUserName']
    if from_user_name == group_user_name:
        print(u'@%s\u2005 发了一句话: %s,%s' % (msg['ActualNickName'], msg['Content'], msg['FromUserName']))


@itchat.msg_register(SYSTEM)
def get_uin(msg):
    chatroom = itchat.search_chatrooms(name='只要我绝对，尬聊没有极限')
    group_user_name = chatroom[0]['UserName']

itchat.auto_login(enableCmdQR=2)
itchat.run()
