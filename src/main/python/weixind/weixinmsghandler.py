#!/usr/bin/env python
# coding=utf8

from itchat.content import *
import json
import os
from os.path import expanduser
import time

MSG_STORAGE_HOME = '%s/weixinmsg' % (expanduser("~"))

def handle_friend_msg(nick_name, msg):
    msg_type = msg['Type']
    if msg_type == TEXT:
        save_text_msg(nick_name, msg)
    elif msg_type == PICTURE or msg_type == RECORDING or msg_type == VIDEO or msg_type == ATTACHMENT:
        msg = download_multi_media_msg(nick_name, msg)
        save_text_msg(nick_name, msg)
    else:
        print "NOT INTERESTED MESSAGE OF TYPE: %s" % msg_type

def handle_mp_msg(nick_name, msg):
    return

def handle_chatroom_msg(nick_name, msg):
    return

def save_text_msg(fromUser, msg):
    home = expanduser("~")
    text_msg_home = '%s/%s' % (MSG_STORAGE_HOME, fromUser)
    if not os.path.isdir(text_msg_home):
        os.makedirs(text_msg_home)
    msg_file = os.path.join(text_msg_home, '%s.json' % msg['MsgId'])
    with open(msg_file, 'w+') as fp:
        fp.write(json.dumps(msg, indent=4))

def download_multi_media_msg(fromUser, msg):
    download_fn = msg['Text']
    media_file_path = "%s/%s/media/%s" % (MSG_STORAGE_HOME, fromUser, msg['FileName'])
    if not os.path.isdir(os.path.dirname(media_file_path)):
        os.makedirs(os.path.dirname(media_file_path))
    msg['MediaFilePath'] = media_file_path
    msg['Text'] = ""  #Text is an address of download function, is not json serializable
    response = download_fn(media_file_path)
    msg['DownloadResponse'] = {}
    msg['DownloadResponse']['ErrMsg'] = response['BaseResponse']['ErrMsg']
    msg['DownloadResponse']['Ret'] = response['BaseResponse']['Ret']
    return msg

def is_text_msg(msg_type):
    return msg_type == TEXT or msg_type == MAP

def is_picture_msg(msg_type):
    return msg_type == PICTURE

def is_voice_msg(msg_type):
    return msg_type == RECORDING

def is_attachment_msg(msg_type):
    return msg_type == ATTACHMENT

def is_video_msg(msg_type):
    return msg_type == VIDEO

