#!/usr/bin/env python
# coding=utf8

import itchat
from itchat.content import *
import weixinmsghandler

'''
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register([FRIENDS])
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.get('isAt'):
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
'''


class WeixinD:

    def __init__(self):
        self.mps = []
        self.friends = []

    def initialize(self):
        itchat.auto_login(enableCmdQR=True, hotReload=True)
        self.mps = itchat.get_mps(update=False)
        self.friends = itchat.get_friends(update=False)

    def get_friend_by_id(self, userId):
        for user in self.friends:
            if userId == user.get('UserName'):
                return user
        return None

    def start(self):
        itchat.run(debug=True)

weixind = WeixinD()


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, RECORDING, VIDEO, ATTACHMENT, SYSTEM, PICTURE], isFriendChat=True, isGroupChat=False, isMpChat=False)
def friend_msg(msg):
    user = weixind.get_friend_by_id(msg['FromUserName'])
    nick_name = user.get('NickName')
    weixinmsghandler.handle_friend_msg(nick_name, msg)
        #itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    # print msg['Content']
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


if __name__ == '__main__':
    weixind.initialize()
    weixind.start()
