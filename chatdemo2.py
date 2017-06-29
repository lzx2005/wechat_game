import re, sys, json

import itchat
from itchat.content import *

itchat.auto_login(True)

@itchat.msg_register(SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    ins = itchat.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    print('** Uin Updated **')
    for username in msg['Text']:
        member = itchat.utils.search_dict_list(
            fullContact, 'UserName', username)
        print(('%s: %s' % (
            member.get('NickName', ''), member['Uin']))
            .encode(sys.stdin.encoding, 'replace'))

itchat.run(True)