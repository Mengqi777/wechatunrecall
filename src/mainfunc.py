#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'memgq'

import sys,os,time
import wechatunrecall
from PyQt5.QtWidgets import (QApplication,QMainWindow,QAction,QMenu,QSystemTrayIcon)
from PyQt5.QtGui import QIcon




class mainwindowapp(QMainWindow,wechatunrecall.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.createActions()
        self.createTrayIcon()
        self.pushButton.clicked.connect(self.saveLog)

        self.pushButton_2.clicked.connect(self.clearlog)
        self.pushButton_3.clicked.connect(self.houtai)
        self.trayIcon.activated.connect(self.iconActivated)
        timeArray = time.localtime()
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        self.setLog(otherStyleTime+"，程序运行时，请用手机扫描弹出的二维码进行登录，并确保电脑上自带的Window照片查"
                                   "看器可用，撤回的图片文件等可下载附件连同运行日志保存在程序目录下BackUp文件夹中。\n")
        self.weChatBigWord()


    def saveLog(self):
        if not os.path.exists(".\\BackUp\\"):
            os.mkdir(".\\BackUp\\")
        timeArray = time.localtime()
        otherStyleTime = time.strftime("%Y-%m-%d%H%M%S", timeArray)
        text=self.textBrowser.toPlainText()
        logPath=".\\BackUp\\"+otherStyleTime+'.txt'
        with open(logPath,'w') as f:
            f.write(text)

    def setLog(self,msg):
        self.textBrowser.append(msg)

    def createTrayIcon(self):
        self.trayIconMenu=QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon=QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon('./media/images/maincion.png'))
        self.setWindowIcon(QIcon('./media/images/maincion.png'))
        self.trayIcon.show()

    def createActions(self):
        self.restoreAction=QAction("恢复",self,triggered=self.showNormal)
        self.quitAction=QAction("退出",self,triggered=QApplication.instance().quit)


    def iconActivated(self,reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showNormal()


    def houtai(self):
        self.hide()

    def clearlog(self):
        self.textBrowser.clear()


    def weChatBigWord(self):
        from weChatThread import weChatWord
        self.wcBWThread=weChatWord()
        self.wcBWThread.getMsgSignal.connect(self.setLog)
        self.wcBWThread.start()








#主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainwindowapp()
    win.show()
    win.pushButton_4.clicked.connect(win.weChatBigWord)
    sys.exit(app.exec_())



