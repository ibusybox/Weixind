#!/usr/bin/env python
# coding=utf8

import itchat
import time
from itchat.content import *
import json
import os
from os.path import expanduser

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
        self.payment_names = [u'微信支付', u'广发信用卡', u'招商银行信用卡', u'手机充值', u'FarBox']

    def initialize(self):
        itchat.auto_login(enableCmdQR=True, hotReload=True)
        self.mps = itchat.get_mps(update=False)

    def get_user_name_by_id(self, userId):
        print "get user name by id: %s" % userId
        for user in self.mps:
            print "try user: %s" % user.get('UserName')
            if userId == user.get('UserName'):
                return user.get('NickName')
        return None

    def save_msg(self, fromUser, msg):
        home = expanduser("~")
        msgHome = '%s/weixinmsg/%s' % (home, fromUser)
        if not os.path.isdir(msgHome):
            os.makedirs(msgHome)
        msgFile = os.path.join(msgHome, '%s.json' % msg['MsgId'])
        with open(msgFile, 'w+') as fp:
            fp.write(json.dumps(msg, indent=4))

    def start(self):
        itchat.run(debug=True)        


weixind = WeixinD()


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def mp_msg_reply(msg):
    nickName = weixind.get_user_name_by_id(msg['FromUserName'])
    if nickName in weixind.payment_names:
        weixind.save_msg(nickName, msg)
        itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    # print msg['Content']
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


if __name__ == '__main__':
    weixind.initialize()
    weixind.start()
