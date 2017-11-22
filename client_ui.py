from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
#from PyQt5.QtWidgets import (QFileDialog, QWidget, QTableWidget, QHBoxLayout, QApplication, QDesktopWidget, QTableWidgetItem, QHeaderView, QMessageBox, QListWidgetItem)
from PyQt5.QtWidgets import *
#from PyQt5.QtCore import qDebug, QModelIndex
from PyQt5.QtCore import *
import sys,os
from ui_login import *
from ui_chat import *
import threading, time
from socket import *
from time import ctime,sleep
import random
from sys import argv, exit, stdout
#from Crypto.Random import get_random_bytes
import json
from extra import *
import random
#count = 0

translate = QCoreApplication.translate


class Main_Window(QThread):
    sig_refresh_msg_show = pyqtSignal(str)
    #sig_refresh_msg_show.connect(self.refresh_msg_show)
    sig_handle_msg = pyqtSignal(str)
    #sig_handle_msg.connect(self.handle_msg)
    sig_connect_to = pyqtSignal(str)
    #sig_connect_to.connect(self.connect_to)
    sig_update_add_pri = pyqtSignal(str)
    #sig_update_add_pri.connect(self.update_add_pri)
    sig_update_add_pub = pyqtSignal(str)
    #sig_update_add_pub.connect(self.update_add_pub)
    sig_update_rm_pri = pyqtSignal(str)
    #sig_update_rm_pri.connect(self.update_rm_pri)
    sig_update_rm_pub = pyqtSignal(str)
    #sig_update_rm_pub.connect(self.update_rm_pub)
    sig_test = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.users_record = {}
        self.username = ""
        self.cur_user = "public"
        self.server_ip = ""
        self.server_port = 0
        self.ui_login = Ui_Login()
        self.ui_chat = Ui_Chat()
        self.wl = QtWidgets.QMainWindow()
        self.ui_login.setupUi(self.wl)
        self.wc = QtWidgets.QMainWindow()
        self.ui_chat.setupUi(self.wc)
        self.set_connect()
        self.init_para()
        self.center(1)
        self.Sessions = {}
        self.online_users = {}
        self.threads = {}
        self.status = False
        self.lock = threading.Lock()
        #self.msg_show_lock = threading.Lock()
        self.msg_stack = stack()
        self.register_signals()
        self.sig_test.connect(self.test_sig)
        self.sig_test.emit("hahaha")
        self.init_media()
        self.wl.show()

    def init_conn(self):
        key_pair = load_keys(self.username)
        self.private_key = key_pair[0]
        self.public_key = key_pair[1]
        self.server_addr = (self.server_ip, self.server_port)
        self.server_addr_a = (self.server_ip, self.server_port+1)
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.Sessions["public"] = Session(self.server_addr, get_random_bytes(16))
        self.Sessions["public_a"] = Session(self.server_addr_a, get_random_bytes(16))

    def test_sig(self, test_msg):
        qDebug("test signal "+test_msg)

    def register_signals(self):
        #self.sig_refresh_msg_show = QtCore.pyqtSignal(str)
        self.sig_refresh_msg_show.connect(self.refresh_msg_show)
        #self.sig_handle_msg = QtCore.pyqtSignal(str)
        self.sig_handle_msg.connect(self.handle_msg)
        #self.sig_connect_to = QtCore.pyqtSignal(str)
        self.sig_connect_to.connect(self.connect_to)
        #self.sig_update_add_pri = QtCore.pyqtSignal(str)
        self.sig_update_add_pri.connect(self.update_add_pri)
        #self.sig_update_add_pub = QtCore.pyqtSignal(str)
        self.sig_update_add_pub.connect(self.update_add_pub)
        #self.sig_update_rm_pri = QtCore.pyqtSignal(str)
        self.sig_update_rm_pri.connect(self.update_rm_pri)
        #self.sig_update_rm_pub = QtCore.pyqtSignal(str)
        self.sig_update_rm_pub.connect(self.update_rm_pub)



    def init_para(self):
        self.ui_login.server_ip.setText("127.0.0.1")
        self.ui_login.server_port.setText("20000")
        self.ui_login.user_name.setText("sustc")


    def init_chat(self):
        #init_users = ["public", "zt", "sustc", "su"]
        init_users = self.online_users.keys()
        self.ui_chat.pri_users.addItem(QListWidgetItem("public"))
        for user in init_users:
            self.ui_chat.pub_users.addItem(QListWidgetItem(user))
            self.users_record[user] = []

        #self.users_record["public"] = [chat_record("public","hello"), chat_record("public","world")]
        #self.users_record["zt"] = [chat_record("zt","hey"), chat_record("zt","zt")]

    def init_media(self):
        qDebug("init media resources")
        media_root="./music"
        self.play_list = QtMultimedia.QMediaPlaylist()
        self.play_list.setPlaybackMode(QtMultimedia.QMediaPlaylist.Random)
        qDebug("????")
        self.player = QtMultimedia.QMediaPlayer()
        qDebug("???")
        self.player.setPlaylist(self.play_list)
        self.play_names = []
        file_list = do_dir(media_root, "mp3")
        qDebug(json.dumps(file_list))
        for fpath in file_list:
            qDebug(fpath)
            media_content = QtMultimedia.QMediaContent(QUrl.fromLocalFile(fpath))
            self.play_list.addMedia(media_content)
            fname = fpath.split("/").pop()
            self.play_names.append(fname)

        play_num = self.play_list.mediaCount()
        rand_index = random.randint(0,play_num-1)
        self.play_list.setCurrentIndex(rand_index)

        #self.player.play()
    def switch_play(self):
        self.player.stop()
        play_num = self.play_list.mediaCount()
        rand_index = random.randint(0,play_num-1)
        self.play_list.setCurrentIndex(rand_index)
        self.player.play()

    def set_connect(self):
        self.ui_login.login_btu.clicked.connect(self.clicked_login)
        self.ui_chat.logout_btu.clicked.connect(self.clicked_logout)
        self.ui_chat.add_pri_user.clicked.connect(self.clicked_add_pri)
        self.ui_chat.rm_pri_user.clicked.connect(self.clicked_rm_pri)
        self.ui_chat.pri_users.clicked.connect(self.clicked_reciever)
        self.ui_chat.send_btu.clicked.connect(self.clicked_send)
        self.ui_chat.msg_input.returnPressed.connect(self.ui_chat.send_btu.clicked.emit)
        self.ui_chat.switch_btu.clicked.connect(self.switch_play)
    '''
    def cliecked_login(self):
        #self.init_chat()
        if self.login():
            qDebug("Login successful")
            self.wl.hide()
            self.center(0)
            self.wc.show()
        else:
            qDebug("Login failure")
    '''

    def clicked_login(self):
        try:
            #_translate = QtCore.QCoreApplication.translate
            self.server_ip = self.ui_login.server_ip.text()
            self.server_port = int(self.ui_login.server_port.text())
            self.username = self.ui_login.user_name.text()
            if self.username == 'public':
                #raise(Exception e)
                qDebug("Login failure")
                qDebug("Can't be public")
                return False

            #初始化和服务器连接
            self.init_conn()
            #初始化聊天界面
            self.ui_chat.menuStatus.setTitle(translate("MainWindow", "Hey, "+self.username))
            self.ui_chat.welcome_label.setText(translate("MainWindow", "Hey " + self.username +", Welcome to  chat!"))
            self.ui_chat.welcome_label.adjustSize()
            qDebug(self.server_ip + ":" + str(self.server_port) + "  " + self.username)
            #self.myclient = client.Client((self.server_ip, self.server_port), self.username)
            #打开登录线程并最多阻塞三秒
            t = threading.Thread(target=self.back_login, args=())
            t.setDaemon(True)
            t.start()
            '''
            t = 3
            dt = t/50
            for i in range(50):
                time.sleep(dt)
                if self.status and len(self.online_users.keys())>0:
                    self.cur_user = "public"
                    self.init_chat()
                    self.refresh_msg_show(self.cur_user)
                    return True
            '''
            t.join(3)
            #根据status以及获取online_users列表来判断是否登录成功
            if self.status and len(self.online_users.keys())>0:
                self.cur_user = "public"
                self.init_chat()
                qDebug("Login successful")
                self.wl.hide()
                self.center(0)
                self.wc.show()
                #self.init_media()
                self.player.play()
                self.refresh_msg_show(self.cur_user)
                qDebug(self.cur_user)
                #t = threading.Thread(target=self.init_media,args=())
                #t.setDaemon(True)
                #t.start()
                #self.sig_refresh_msg_show.emit(self.cur_user)
                return True

            qDebug("status " + str(self.status))
            qDebug("Login failure")
            #self.myclient.run()
            return False

        except Exception as e:
            qDebug(str(e))
            qDebug("Please input all info")
            return False

    def clicked_logout(self):
        '''
        logout按钮触发事件
        '''
        #打开注销线程并最多阻塞两秒
        t = threading.Thread(target=self.back_logout, args=())
        t.setDaemon(True)
        t.start()
        t.join(2)
        qDebug("Logout successful")
        #清空用户相关参数
        self.users_record = {}
        self.ui_chat.pri_users.clear()
        self.ui_chat.pub_users.clear()

        #隐藏聊天窗口，显示登录窗口
        self.wc.hide()
        self.player.stop()
        self.center(1)
        self.wl.show()

    def clicked_send(self):
        '''
        消息发送按钮触发事件
        获取输入框内容并生存记录以及消息，将消息msg发送给当前聊天用户
        '''
        input_msg = self.ui_chat.msg_input.text()
        #gen_msg = "msg:"+self.cur_user + ":"+input_msg
        #self.myclient.deal_input(gen_msg)
        new_record = chat_record("me", input_msg)
        self.users_record[self.cur_user].append(new_record)
        #if self.cur_user == "public":
        #    self.ui_chat.msg_show.append("me(pub): " + input_msg)
        #else:
        self.ui_chat.msg_show.append("me: " + input_msg)
        self.ui_chat.msg_input.clear()

        msg = Message(("msg", self.username, input_msg.encode(encoding='utf_8')))
        qDebug(self.username +  "->" + self.cur_user + ": " + msg.body.decode(encoding='utf_8'))
        self.send(self.cur_user, msg)
        #count+=1
        #qDebug(str(count))
        return

    @pyqtSlot()
    def refresh_msg_show(self, who="public"):
        '''
        根据传入用户名刷新msg_show窗口为和该用户的聊天记录
        '''
        qDebug("1")
        #self.msg_show_lock.acquire()
        self.ui_chat.msg_show.clear()
        qDebug("2")
        if who in self.users_record.keys():
            qDebug("3")
            for record in self.users_record[who]:
                qDebug("4")
                self.ui_chat.msg_show.append(record.__str__())
        #else:
            #self.users_record[who] = []
        #self.msg_show_lock.release()
        qDebug("5")

    def refresh_tip(self):
        '''
        刷新提示栏为提示栈的栈顶提示
        '''
        if self.msg_stack.len >0 :
            top_tip = self.msg_stack.pop()
            self.ui_chat.label_tip.setText(translate("MainWindow", top_tip))
        else:
            self.ui_chat.label_tip.setText(translate("MainWindow", ""))

    def add_record(self, new_record, isPublic=False):
        '''
        添加一条消息记录，如果消息记录来源为自己或者当前聊天用户则同时添加到msg_show窗口中
        '''
        qDebug("add record")
        if isPublic:
            self.users_record["public"].append(new_record)
            if "public" == self.cur_user:
                self.ui_chat.msg_show.append(new_record.__str__())
            else:
                tip = "recieved (pub)msg from " + new_record.who
                self.msg_stack.push(tip)
                self.refresh_tip()
        else:
            self.users_record[new_record.who].append(new_record)
            if new_record.who == self.cur_user:
                self.ui_chat.msg_show.append(new_record.__str__())
            else:
                tip = "recieved msg from " + new_record.who
                #self.ui_chat.label_tip.setText(translate("MainWindow", tip))
                self.msg_stack.push(tip)
                self.refresh_tip()

    def contain_item(self, user_list, name):
        '''
        用于判断在一个QListWidgets里面时候包含文本值为name的Item,包含的话返回索引，否则-1
        '''
        users_N = user_list.count()
        qDebug(str(users_N))
        for i in range(users_N):
            item = user_list.item(i)
            if name == item.text():
                return i
        return -1

    @pyqtSlot()
    def update_add_pub(self, new_user):
        '''
        往在线客户端列表中新加一个客户端，在有客户端登录时接受到服务器的更新列表消息后会调用本函数
        '''
        qDebug("add_pub_user")
        #try:
        if self.contain_item(self.ui_chat.pub_users, new_user)<0:
            self.ui_chat.pub_users.addItem(new_user)
            tip = new_user + " is online now!"
            self.msg_stack.push(tip)
            self.refresh_tip()

        else:
            qDebug("Already added")

    @pyqtSlot()
    def update_rm_pub(self, rm_user):
        '''
        从在线客户端列表中删除一个客户端，在有客户端注销是收到服务器的更新列表消息后会调用本函数
        '''
        qDebug("rm_pub_user")
        #try:
        '''
        if (not rm_user in ("public", self.username)) and (self.contain_item(self.ui_chat.pub_users, rm_user)>=0):
            pub_users_N = self.ui_chat.pub_users.count()
            for i in range(pub_users_N):
                item = self.ui_chat.pub_users.item(i)
                if rm_user == item.text():
                    self.ui_chat.pub_users.takeItem(i)
                    self.msg_stack.remove_by_name(rm_user)
                    tip = rm_user + " logout!"
                    self.msg_stack.push(tip)
                    self.refresh_tip()
                    return
        '''
        #判断删除客户端不是public或者自己，并且在当前的在线客户端列表中
        index = self.contain_item(self.ui_chat.pub_users, rm_user)
        not_in = (not rm_user in ("public", self.username))
        if not_in and index >=0:
            item = self.ui_chat.pub_users.item(index)
            #qDebug(rm_user + " =? " + item.text())
            if rm_user == item.text():
                self.ui_chat.pub_users.takeItem(index)
                #qDebug("befor remove")
                self.msg_stack.remove_by_name(rm_user)
                tip = rm_user + " logout!"
                self.msg_stack.push(tip)
                #qDebug("add tip")
                self.refresh_tip()
                #qDebug("refreshed logout tip")
                return
        else:
            qDebug("Can't find pub_user "+rm_user)

    @pyqtSlot()
    def update_rm_pri(self, rm_user, need_send=False):
        '''
        从私密客户端列表中删除一个客户端，在收到客户端的断开连接消息或服务器发来的删除已注销客户端消息时会调用。
        '''
        qDebug("rm_pri_user")
        '''
        判断删除客户端不是public并且与自己建立了私密连接
        '''
        qDebug("1")
        if rm_user == self.cur_user:
            qDebug("a")
            self.cur_user = "public"
            self.reset_who()
            qDebug("b")
            #self.refresh_msg_show(self.cur_user)
            self.sig_refresh_msg_show.emit(self.cur_user)

        qDebug("2")
        if rm_user in self.Sessions.keys():
            self.delete_session(rm_user, need_send)

        if rm_user in self.users_record.keys():
            del self.users_record[rm_user]

        qDebug("3")
        index = self.contain_item(self.ui_chat.pri_users, rm_user)
        not_pub = rm_user != "public"
        qDebug(str(index))
        qDebug(str(not_pub))
        if not_pub and index >=0:
            item = self.ui_chat.pri_users.item(index)
            qDebug(rm_user + " =? " + item.text())
            if rm_user == item.text():
                self.ui_chat.pri_users.takeItem(index)
                qDebug("4")
                self.msg_stack.remove_by_name(rm_user)
                qDebug("5")
                tip = "disconnected to " + rm_user
                self.msg_stack.push(tip)
                qDebug("6")
                self.refresh_tip()
                qDebug("7")
                return
        else:
            qDebug("Can't find pri_user " + rm_user)

    @pyqtSlot()
    def update_add_pri(self, new_pri, send_request=True):
        '''
        新建一个与其他客户端的私密会话并加到私密客户端列表中，在发起或收到连接请求时会调用本函数。
        '''
        if (self.contain_item(self.ui_chat.pri_users, new_pri)==-1) and new_pri != self.username:
                    qDebug("send conn request to " + new_pri)
                    #self.connect_to(new_pri)
                    if send_request:

                        t = threading.Thread(target=self.connect_to, args=([new_pri]))
                        t.setDaemon(True)
                        t.start()
                        t.join(3)
                        '''
                        self.sig_connect_to.emit(new_pri)
                        '''
                    i = 0
                    while i<30:
                        sleep(0.01)
                        if new_pri in self.Sessions.keys() and self.Sessions[new_pri].client_addr != self.server_addr:
                            break
                        i+=1

                    if new_pri in self.Sessions.keys() and self.Sessions[new_pri].client_addr != self.server_addr:
                        self.ui_chat.pri_users.addItem(new_pri)
                        if not (new_pri in self.users_record.keys()):
                            self.users_record[new_pri] = []
                        tip = "connected to " + new_pri + " successful!"
                        self.msg_stack.push(tip)
                        self.refresh_tip()
                        return
                    else:
                        tip = "connected to " + new_pri + " failed!"
                        self.msg_stack.push(tip)
                        self.refresh_tip()
                        return
        else:
            qDebug("Already added")

    def clicked_add_pri(self):
        '''
        新建私密连接按钮触发事件，向在线客户端列表中被选择的用户发起连接请求
        '''
        qDebug("hahahah")
        #try:
        items = self.ui_chat.pub_users.selectedItems()
        if len(items) > 0:
            for item in items:
                #qDebug(item.text())
                #qDebug(str(self.contain_item(self.ui_chat.pri_users, item.text())))
                threading.Thread(target=self.update_add_pri, args=([item.text()])).start()
                #self.sig_update_add_pri.emit(item.text())
        #except Exception as e:
        #    qDebug("Nothing selected")

    def clicked_rm_pri(self):
        '''
        删除私密连接按钮触发事件，向私密客户端列表中被选择的用户发起断开连接请求
        '''
        qDebug("hahahah")
        indexs = self.ui_chat.pri_users.selectedIndexes()
        if len(indexs) > 0:
            for index in indexs:
                qDebug(str(index.row()))
                item = self.ui_chat.pri_users.item(index.row())
                if item.text() != "public":
                    #self.delete_session(item.text(), True)
                    '''
                    self.ui_chat.pri_users.takeItem(index.row())
                    #self.send(item.text(), Message(("disconnect",self.username, b'')))
                    tip = "disconnected to " + item.text()
                    self.msg_stack.push(tip)
                    self.refresh_tip()
                    if item.text() == self.cur_user:
                        self.cur_user = "public"
                        self.reset_who()
                        self.refresh_msg_show(self.cur_user)
                    '''
                    self.update_rm_pri(item.text(), True)
                    return
                else:
                    qDebug("Can't remove public")

    def reset_who(self):
        self.ui_chat.label_user.setText(translate("MainWindow", self.cur_user + ":"))

    def clicked_reciever(self):
        '''
        私密客户端列表被点击时获取被选中项，将消息窗口切换成与该客户端的聊天记录
        '''
        items = self.ui_chat.pri_users.selectedItems()
        if len(items) > 0:
            to_who = items[0].text()
            #self.ui_chat.label_user.setText(translate("MainWindow", to_who + ":"))
            self.cur_user = to_who
            self.reset_who()
            qDebug(to_who)
            self.refresh_msg_show(self.cur_user)
            #self.sig_refresh_msg_show.emit(self.cur_user)
            tip = "chat with " + self.cur_user + " now"
            self.msg_stack.push(tip)
            self.refresh_tip()
            return


    def center(self, i):
        '''
        将窗口移动到屏幕中央
        '''
        #qDebug("????")
        #qr = self.ui_login.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        #self.ui_login.move(cp.x(),cp.y())
        if i==1:
            qr = self.ui_login.frameGeometry()
            qr.moveCenter(cp)
            self.wl.move(qr.topLeft())

        else:
            qr = self.ui_login.frameGeometry()
            qr.moveCenter(cp)
            self.wc.move(qr.topLeft())

    def back_login(self):
        '''
        back_login:
            客户端登陆，先从客户端获取公钥，用公钥加密与服务端的会话密钥并放入msg.body中，
            服务器返回一个数组[status all_users_name],登陆成功后打开和服务器会话线程
        '''
        msg = Message(("get_pub", self.username, b"public"))
        qDebug((msg.body.decode()))
        self.send("public", msg)
        qDebug("want key")
        qDebug(str(self.server_addr))
        pub_msg = self.Sessions["public"].recieve()
        qDebug("No pub key")
        server_pub_key = rsa.PublicKey.load_pkcs1(pub_msg.body)
        '''
        qDebug(server_pub_key)
        qDebug(self.Sessions["public"].get_key())
        '''
        qDebug("***********")

        #[session_key pub_key] -> dump -> rsa
        rsa_session_key = rsa_encode(server_pub_key, self.Sessions["public"].get_key())

        body =  self.public_key.save_pkcs1() + rsa_session_key

        self.Sessions["public"].send(Message(("login", self.username, body)))
        qDebug("***********")
        msg = self.Sessions["public"].recieve()
        qDebug("***********")
        info = json.loads(msg.body.decode(encoding='utf_8'))
        status = info[0]
        if status == 1:
            qDebug("login in sucessful")
            self.online_users["public"] = server_pub_key
            for cn in info[1:]:
                self.online_users[cn] = ""
                qDebug(cn)
            #self.locks["public"] = threading.Lock()
            self.threads["public"] = threading.Thread(target=self.handle_msg, args=(["public"]))
            self.threads["public"].start()
            #self.threads["public"].join()
            #self.sig_handle_msg.emit("public")
            self.lock.acquire()
            self.status = True
            self.lock.release()
            return True
        else:
            qDebug("login failure!")
            return False

    def get_status(self):
        return self.status

    def back_logout(self):
        '''
        logout:
            注销登陆，断开所有连接并清空
        '''
        #msg = Message(("logout",self.username, ""))
        ##self.locks[client_username].acquire()
        #self.Sessions["public"].send(msg.__bytes__())
        ##self.locks[client_username].release()
        #ts = []
        #for client_username in list(self.Sessions.keys()):
        t = threading.Thread(target=self.delete_session,args=(["public", True]))
        t.start()
        t.join(3)
        #    ts.append(t)

        #for t in ts:
        #    t.join()

        self.Sessions = {}
        self.clientSocket.close()
        self.online_users = {}
        return 0

    @pyqtSlot()
    def connect_to(self, client_username):
        '''
        connect_to:
            连接到另一个客户端，先生成会话密钥， 检测已连接，然后检测时候有该客户端公钥，
            没有的话先向服务器查询，接着建立会话， 构建消息包:
            msg:
                type: connect
                username: current_username
                body: json.dumps([to rsa_encode(to_pub_key,session_key)])
            发送出去后等待目标客户端响应，得到目标客户端会话地址，更新会话地址
        '''
        #input()
        session_key = get_random_bytes(16)
        qDebug(session_key)
        if client_username in self.Sessions.keys():
            qDebug("Already connected!")
            return
        #input()
        if self.online_users[client_username] == "":
            self.Sessions["public"].send(Message(('get_pub',self.username, client_username.encode(encoding='utf_8'))))
        #input()
            #pub_key = rsa_decode(self.private_key, encry_pub_key)

        while self.online_users[client_username] == "":
            sleep(0.01)

        #input()
        qDebug("get pub key")
        self.Sessions[client_username] = Session(self.server_addr_a, session_key)
        #input()
        #self.locks[client_username] = threading.Lock()
        #将client_username补齐20位
        qDebug("padding msg head")
        body = client_username.encode(encoding='utf_8')
        lb = len(body)
        l = 20 - len(body)
        for i in range(l):
            body+= bytes([l])

        #print("origin body " + body[:lb].decode(encoding='utf_8'))
        msg = Message(('connect',self.username, body+rsa_encode(self.online_users[client_username], session_key)))
        #input()
        self.send(client_username, msg)
        #input()
        qDebug("send connect request")
        msg, client_addr = self.Sessions[client_username].recieve(True)
        #input()
        qDebug("aim IP: " + str(client_addr))
        qDebug("connected successful")
        self.Sessions[client_username].update_client(client_addr)
        self.threads[client_username] = threading.Thread(target=self.handle_msg, args=([client_username]))
        self.threads[client_username].start()
        #self.sig_handle_msg.emit(client_username)
        #self.threads[client_username].join()


    def add_connect(self, msg):
        '''
        add_connect:
            响应其他客户端的连接请求
            msg:
                type: connect
                username: from_name
                body: bytes[from_addr rsa_encode(self_pub_key,session_key)])
            新建会话，并返回一个数据包告诉对方自己的会话地址
        '''
        #json_msg = bytes_msg.decode(encoding='utf_8')
        #msg = loads_msg(bytes_msg)
        qDebug("recieve connect request")
        client_username = msg.username
        #body中前30字节为目标客户端名字
        #print(msg.body)
        bytes_addr = msg.body[:(30-msg.body[29])]
        client_addr = tuple(json.loads(bytes_addr.decode(encoding='utf_8')))
        session_key = rsa_decode(self.private_key, msg.body[30:])
        #self.locks[client_username] = threading.Lock()
        self.Sessions[client_username] = Session(client_addr, session_key)
        self.threads[client_username] = threading.Thread(target=self.handle_msg, args=([client_username]))
        self.threads[client_username].start()
        #self.sig_handle_msg.emit(client_username)

        self.send(client_username, Message(("msg", self.username, b"")))
        qDebug("connected by " + msg.username)
        self.update_add_pri(msg.username, False)
        #self.threads[client_username].join()


    def delete_session(self, client_username, need_send=False):
        '''
        delete_session:
            删除一个会话，先告诉对方自己即将断开连接
            并把对应的线程，锁清除
            不复杂UI列表刷新
        '''
        #lock = threading.Lock()
        #lock.acquire()
        qDebug("disconnected to "+client_username)
        qDebug(json.dumps(list(self.Sessions.keys())))
        if client_username in self.Sessions.keys():
            #self.locks[client_username].acquire()
            if need_send:
                if client_username == "public":
                    msg = Message(("logout", self.username, b""))
                    self.send(client_username, msg)
                else:
                    msg = Message(("disconnect", self.username, b""))
                    self.send(client_username, msg)

            #self.locks[client_username].release()
            #time.sleep(0.01)
            self.Sessions[client_username].close()
            #if self.threads[client_username].isAlive():
            #    self.threads[client_username].cancel()
            lock = threading.Lock()
            lock.acquire()
            del self.threads[client_username]
            del self.Sessions[client_username]
            lock.release()
            #del self.locks[client_username]
        #lock.release()

    def send(self, to_who, msg):
        '''
        send:
            封装发送过程，客户端发送消息
        参数:
            client_username: 接收机名字
            msg: Message对象
        '''
        if to_who in list(self.Sessions.keys()):
            #msg = Message(("msg", self.username, ))
            #self.locks[to_who].acquire()
            rs = self.Sessions[to_who].send(msg)
            #self.locks[to_who].release()
            qDebug("send msg to " + to_who + ": " + msg.__str__())

            '''
            if msg.type == "msg":
                qDebug(msg.body)
                qDebug("to " + to_who + " : " + msg.body.decode(encoding='utf_8'))
            '''

    @pyqtSlot()
    def handle_msg(self, client_username):
        '''
        handle_msg:
            接收和client_username的会话中的返回内容
        '''
        while 1:
            ##self.locks[client_username].acquire()
            #接收到的Message对象除了msg和broadmsg类型的消息外，其他类型消息的body都保持了bytes可是，msg类型的body已用会话密钥解密
            msg = self.Sessions[client_username].recieve()
            qDebug("From " + client_username + " recieved " + msg.__str__())
            ##self.locks[client_username].release()
            if msg.type == "msg":

                if client_username == "public":
                    qDebug(("from (pub)" + msg.username + " : " + msg.body.decode(encoding='utf_8')))
                    #self.add_record(chat_record(msg.username, msg.body.decode(encoding='utf_8')))
                    new_record = chat_record(msg.username, msg.body.decode(encoding='utf_8'))
                    self.add_record(new_record, True)

                else:
                    qDebug((" " + client_username + " : " + msg.body.decode(encoding='utf_8')))
                    new_record = chat_record(msg.username, msg.body.decode(encoding='utf_8'))
                    #self.users_record[client_username].append(new_record)
                    #if client_username == self.cur_user:
                    #    self.ui_chat.msg_show.append(new_record.__str__())
                    self.add_record(new_record)
                    #self.add_record(chat_record(client_username, msg.body.decode(encoding='utf_8')))

                #qDebug(("from " + client_username + " : " + msg.body.decode(encoding='utf_8')))
                #self.add_record(chat_record(client_username, msg.body.decode(encoding='utf_8')))
                continue
            '''
            if msg.type == "broadmsg":
                msg.body = aes_decode(msg.body, self.Sessions["public"].get_key())
                qDebug("(pub) from ")
            '''
            if msg.type == "connect":
                self.add_connect(msg)
                continue

            if msg.type == "get_pub":
                pub_key = rsa.PublicKey.load_pkcs1(msg.body)
                self.online_users[msg.username] = pub_key
                continue

            if msg.type == "disconnect":
                '''
                self.delete_session(msg.username)
                index = self.contain_item(self.ui_chat.pri_users, client_username)
                if index != -1:
                    self.ui_chat.pri_users.takeItem(index)
                    tip = "disconnected from " + msg.username + "!"
                    self.msg_stack.push(tip)
                    self.refresh_tip()
                '''
                self.update_rm_pri(msg.username)
                #self.sig_update_rm_pri.emit(msg.user_name)
                break

            if msg.type == "update":
                self.update_online_users(msg)
                continue

    def update_online_users(self, msg):
        '''
        处理服务器发来的更新用户消息，新用户登录以及用户注销
        '''
        client_name = msg.username
        op = msg.body.decode(encoding='utf_8')
        if op == "add":
            self.online_users[client_name] = b''
            #self.ui_chat.pub_users.addItem(client_name)
            self.update_add_pub(client_name)
            #self.sig_update_add_pub.emit(client_name)
            qDebug("Update online users")
            qDebug(json.dumps(list(self.online_users.keys())))
            return

        if op == "rm":
            #self.delete_session(client_name)
            self.update_rm_pri(client_name)
            #self.sig_update_rm_pri.emit(client_name)
            self.update_rm_pub(client_name)
            #self.sig_update_rm_pub.emit(client_name)
            #print(json.dumps(list(self.online_users.keys())))
            #print(json.dumps(list(self.Sessions.keys())))
            return

    '''
    def deal_input(self, input_msg):

        （在非GUI版本中用于处理命令行输入)
        deal_input:
            处理输入内容，一般为: 类型:接收者：消息内容(默认为空)
        构建Message对象并发送

        #global count
        #input_msg = line[0]
        inputs = input_msg.split(":", -1)
        if len(inputs) == 2:
            inputs.append("")

        msg_type = inputs[0]
        username = inputs[1]
        body = inputs[2]

        if msg_type == "logout":
            self.logout()
            return
        if msg_type == "login":
            self.username = username
            self.login()
            return

        if msg_type == "connect":
            self.connect_to(username)
            return

        if msg_type == "disconnect":
            index = self.contain_item(self.ui_chat.pri_users, username)
            if index != -1:
                self.ui_chat.pri_users.takeItem(index)

            self.delete_session(username)
            return
        if inputs[0] == "show":
            if inputs[1]=="pub_users":
                qDebug(json.dumps(list(self.online_users.keys())))
                return
            if inputs[1]=="pri_users":
                qDebug(json.dumps(list(self.Sessions.keys())))
                return
            if inputs[1] == "pub_key":
                qDebug(self.Sessions["public"].get_key())
                return
            return

        inputs[2] = inputs[2].encode(encoding='utf_8')
        #print("input->>" + inputs[2].decode('utf_8'))
        msg = Message(inputs)
        msg.username = self.username

        if msg.type == "msg":
            qDebug(self.username +  "->" + username + ": " + msg.body.decode(encoding='utf_8'))
            self.send(username, msg)
            #+=1
            #qDebug(str(count))
            return

        qDebug("invalied msg format:\n type:who:body\n")
    '''
