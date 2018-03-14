#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import itchat
import codecs
from itchat.content import *
jsonStr = ""
with codecs.open('./json/reply.json', 'r', 'utf8') as f:
    jsonStr += f.read()
print(jsonStr)
jsonArray = json.loads(jsonStr)


@itchat.msg_register([TEXT], isGroupChat=False)
def text_reply(msg):
    print(json.dumps(msg))
    content = msg['Content']
    for jsonObject in jsonArray:
        keyword = jsonObject['keyword']
        keywords = keyword.split("|")
        for key in keywords:
            if key in content:
                reply = jsonObject['reply']
                itchat.send(reply)


itchat.auto_login(enableCmdQR=2)
itchat.run()
