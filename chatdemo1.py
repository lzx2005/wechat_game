import itchat
import re, sys, json
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    itchat.send('你好，我收到了您的消息"%s"，但是我现在不在手机身边，稍后我会联系您~' % (msg['Text']), msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    json_object = json.dumps(msg)
    print(json_object)
    print("\n")
    print(u'@%s\u2005I received: %s,%s' % (msg['ActualNickName'], msg['Content'], msg['FromUserName']))


@itchat.msg_register(SYSTEM)
def get_uin(msg):
    chatroom = itchat.search_chatrooms(name='只要我绝对，尬聊没有极限')
    print(json.dumps(chatroom))

itchat.auto_login(enableCmdQR=2)
itchat.run()
