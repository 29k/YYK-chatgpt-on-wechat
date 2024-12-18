from lib import itchat
from lib.itchat.content import *

def login():
    itchat.auto_login(hotReload=True)

def get_group_ids(group_names):
    group_ids = {}
    chatrooms = itchat.get_chatrooms(update=True)
    for room in chatrooms:
        if room["NickName"] in group_names:
            group_ids[room["NickName"]] = room["UserName"]
    return group_ids

def send_message(group_id, message):
    itchat.send(message, toUserName=group_id)
