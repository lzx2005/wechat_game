#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import itchat
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 判断是否是自己发的
    if msg['ToUserName'] == msg['User']['UserName']:
        # 收到信息的是对方，所以是自己发的
        show_string = "[" + now + "][type:" + msg['Type'] + "]自己 : " + msg['Content']
    else:
        show_string = "[" + now + "][type:" + msg['Type'] + "]" + msg['User']['NickName'] + "," + msg['User'][
            'RemarkName'] + " : " + msg['Content']
    f = open("logs/2017.log", "a")
    f.write(show_string)
    f.write("\n")
    f.close()
    print(show_string)
    # itchat.send('你好，我收到了您的消息"%s"，但是我现在不在手机身边，稍后我会联系您~' % (msg['Text']), msg['FromUserName'])


# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if msg['ToUserName'] == msg['User']['UserName']:
        # 收到信息的是对方，所以是自己发的
        before = "[" + now + "][type:" + msg['Type'] + "]自己 : "
        show_string = '%s@%s@%s' % (before, {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    else:
        before = "[" + now + "][type:" + msg['Type'] + "]" + msg['User']['NickName'] + "," + msg['User'][
            'RemarkName'] + " : "
        show_string = '%s@%s@%s' % (before, {'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

    f = open("logs/2017v.log", "a")
    f.write(show_string)
    f.write("\n")
    f.close()
    msg['Text'](msg['FileName'])  # 下载图片
    print(show_string)

itchat.auto_login(enableCmdQR=2)
itchat.run()
