#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'memgq'

from PyQt5.QtCore import QThread,pyqtSignal
import itchat
import time,os
import shutil
import re

from itchat.content import *

class weChatWord(QThread):
    getMsgSignal = pyqtSignal(str)
    def __init__(self,parent=None):
        super(weChatWord,self).__init__(parent)
        self.msg_list=[]
        self.type_list=['Picture','Recording', 'Attachment','Video']



    def clearList(self):
        tm_now=time.time()
        len_list=len(self.msg_list)
        if len_list>0:
            for i in range(len_list):
                if tm_now-self.msg_list[i]['msg_time']>121:
                    if self.msg_list[i]['msg_type'] in self.type_list:
                        try:
                            os.remove(".\\BackUp\\"+self.msg_list[i]['msg_content'])
                        except Exception as e:
                            print(e)
                        finally:
                            pass
                else:break
            self.msg_list=self.msg_list[i:]









    def run(self):
        @itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS], isFriendChat=True,
                      isGroupChat=True)
        def getMsg(msg):
            msg_dict={}
            # pprint.pprint(msg)
            msg_id = msg['MsgId']  # 消息ID
            msg_time = msg['CreateTime']
            msg_url=None
            msg_group=""
            if (itchat.search_friends(userName=msg['FromUserName'])):
                if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
                    msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']  # 消息发送人备注
                elif itchat.search_friends(userName=msg['FromUserName'])['NickName']:  # 消息发送人昵称
                    msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 消息发送人昵称
                else:
                    msg_from = r"读取发送消息好友失败"
            else:
                msg_group = msg['User']['NickName']
                msg_from = msg['ActualNickName']
            msg_type = msg['Type']
            if msg_type in ['Text', 'Friends','Sharing']:
                msg_content = msg['Text']
                msg_url = msg['Url']
            elif msg_type in self.type_list:
                msg_content=msg['FileName']
                msg['Text'](msg['FileName'])
                shutil.move(msg_content,r'.\\BackUp\\')
            elif msg['Type'] == 'Card':
                msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
            elif msg['Type'] == 'Map':
                x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*",
                                           msg['OriContent']).group(1,
                                                                    2,
                                                                    3)
                if location is None:
                    msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
                else:
                    msg_content = r"" + location

            msg_dict={'msg_id':msg_id,'msg_time':msg_time,'msg_from':msg_from,'msg_group':msg_group,
                      'msg_content':msg_content,'msg_type':msg_type,'msg_url':msg_url}
            self.msg_list.append(msg_dict)
            self.clearList()


        @itchat.msg_register([NOTE],isFriendChat=True, isGroupChat=True)
        def recall(msg):
            # pprint.pprint(msg)
            msg_content=msg['Content']
            if re.search(r'\<replacemsg\>\<!\[CDATA\[(.*)撤回了一条消息\]\]\>\<\/replacemsg\>',msg_content):
                msg_note=re.search(r'\<replacemsg\>\<!\[CDATA\[(.*)\]\]\>\<\/replacemsg\>',msg_content).group(1)
                old_msg_id=re.search(r'\<msgid\>([0-9]+)\</msgid\>',msg_content).group(1)
                for each in self.msg_list:
                    if each['msg_id']==old_msg_id:
                        timeArray = time.localtime()
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S,", timeArray)
                        msg_note = msg_note + '，撤回内容为：' + each['msg_content']
                        if each['msg_group']!='':
                            msg_note = "群组（"+each['msg_group']+")中"+msg_note
                        msg_note=otherStyleTime+msg_note
                        itchat.send(msg_note,toUserName='filehelper')
                        self.msg_list.pop(self.msg_list.index(each))
                        self.getMsgSignal.emit(msg_note)
                        break


        if not os.path.exists(".\\BackUp\\"):
            os.mkdir('.\\BackUp\\')
        itchat.auto_login(hotReload=True)
        itchat.run()




