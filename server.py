from socket import *
from time import ctime, sleep
import threading
from extra import *
import sys
import rsa
class Server:
    '''
    成员变量:
        private_key:服务器公钥 
        public_key: 服务器私钥
        ip: 服务器ip
        port: 服务器监听端口
        server_socket: 服务器使用套接字
        Sessions: 服务器与客户机建立的辅助连接{client_name:Sessiom}
        public_keys： 客户端对应的公钥{client_name: client_pub_key}
        locks: 客户端连接对应锁
        status: 服务器在线状态
    '''
    def __init__(self,server_addr):
        self.name = "public"
        key_pair = load_keys(self.name)
        print(len(key_pair))
        self.private_key = key_pair[0]
        self.public_key = key_pair[1]
        self.ip = server_addr[0]
        self.port = server_addr[1]
        #self.port_a = server_addr[2]
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket_a = socket(AF_INET, SOCK_DGRAM)
        self.server_socket_a.bind((self.ip, self.port+1))
        #self.server_socket_a = socket(AF_INET, SOCK_STREAM)
        #self.server_socket_a.bind((self.ip, self.port_a))
        self.Sessions = {}
        #self.Sessions_a = {}
        self.public_keys = {"public":self.public_key}
        #self.locks = {}
        #self.lock = threading.Lock()
        self.status = True
        self.threads = {}

    def handle_msg(self):
        '''
        handle_msg: 
            当status等于True(服务器在线)时不断从server_socket中读取数据，恢复出Message对象后
            根据消息类别选择对应的操作
        '''

        while self.status:
            #print("status", self.status)
            msg, new_address = self.server_socket.recvfrom(2048)
            msg = loads_msg(msg)
            print("收到类型: " + msg.type)

            if msg.type == "msg":
                t = threading.Thread(target=self.broadcast, args=([msg]))
                t.start()
                continue

            if msg.type == "login":
                print("收到登陆请求")
                t = threading.Thread(target=self.login, args=([msg]))
                t.start()
                continue
            '''
            if msg.type == "connect":
                
                msg:
                    type:str
                    username:str
                    body: my_addr(30) content()
                
                #msg, new_address = which_socket.recvfrom(2048)
                #msg = loads_msg(msg.decode(encoding='utf_8'))
                #body = json.loads(msg.body)
                #body.append(new_address)
                #body = [to encry(session_key) from_addr]
                #msg.body = json.dumps(body)
                print("收到"+msg.username + "的连接请求")
                print("与消息来源会话密钥: "+self.Sessions[msg.username].get_key())
                bytes_addr = json.dumps(new_address).encode(encoding='utf_8')
                ll = len(bytes_addr)
                l = 30-len(bytes_addr)
                for i in range(l):
                    bytes_addr += bytes([l])
                print("消息来源地址: " + bytes_addr[:ll].decode(encoding='utf_8'))
                to_who = msg.body[:(20-msg.body[19])].decode(encoding='utf_8')
                msg.body = bytes_addr + msg.body[20:]

                t = threading.Thread(target=self.forward, args=([to_who, msg]))
                t.start()
                continue
            '''
            if msg.type in ["logout", "disconnect"]:
                print("收到注销请求")
                t = threading.Thread(target=self.logout, args=([Message(("update", msg.username, b'rm'))]))
                t.start()
                continue
                
            if msg.type == "get_pub":
                print("收到查询公钥的请求")
                #self.locks[msg.username] = threading.Lock()
                if not (msg.username in self.Sessions.keys()):
                    self.Sessions[msg.username] = Session(new_address, "")
                t = threading.Thread(target=self.get_pub, args=([msg]))
                t.start()
                continue

    def handle_connect(self):
        while 1:
            msg, new_address = self.server_socket_a.recvfrom(2048)
            msg = loads_msg(msg)
            print("收到类型: " + msg.type)
            if msg.type == "connect":
                '''
                msg:
                    type:str
                    username:str
                    body: my_addr(30) content()
                '''
                #msg, new_address = which_socket.recvfrom(2048)
                #msg = loads_msg(msg.decode(encoding='utf_8'))
                #body = json.loads(msg.body)
                #body.append(new_address)
                #body = [to encry(session_key) from_addr]
                #msg.body = json.dumps(body)
                print("收到"+msg.username + "的连接请求")
                print("与消息来源会话密钥: ")
                print(self.Sessions[msg.username].get_key())
                bytes_addr = json.dumps(new_address).encode(encoding='utf_8')
                ll = len(bytes_addr)
                l = 30-len(bytes_addr)
                for i in range(l):
                    bytes_addr += bytes([l])
                print("消息来源地址: " + bytes_addr[:ll].decode(encoding='utf_8'))
                to_who = msg.body[:(20-msg.body[19])].decode(encoding='utf_8')
                msg.body = bytes_addr + msg.body[20:]
                self.forward(to_who, msg)
                #t = threading.Thread(target=self.forward, args=([to_who, msg]))
                #t.start()
                continue

    def broadcast(self, msg, ne=True):
        '''
        broadcast:
            将msg转发给连接到服务器的所有除消息来源外的客户端，
            发送时发送端用和服务器的会话密钥加密msg.body，服务器收到后解密，在
            转发时分别用和各个客户端的会话密钥加密
        msg
        '''
        print("广播消息: " + msg.type + " " + msg.username)
        #msg.body = rsa_decode(self.private_key, msg.body)
        if msg.type == "msg":
            #print(type(msg.body))
            msg.body = self.Sessions[msg.username].decode(msg.body)
            print("消息内容:" + msg.body.decode(encoding='utf_8'))

        #msg传了指针!,需要匿名对象防止内容篡改
        for client_name in list(self.Sessions.keys()):
            if client_name != msg.username:
                #self.locks[client_name].acquire()
                self.Sessions[client_name].send(Message((msg.type, msg.username, msg.body)))
                #self.locks[client_name].release()

                
    def login(self, msg):
        '''
        login:
            将用户注册到当前网络中,msg类型为login, username为注册用户的用户名
            body为用服务端公钥加密的json.dumps([session_key, public_key]),
            并返回登陆状态默认为1以及已连接所有用户名
        length(pub_key) = 426
        '''
        client_name = msg.username
        print("login: " + msg.username)
        #rsa -> loads -> [session_key, public_key]
        public_key = msg.body[:426]
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        #self.locks[client_name] = threading.Lock()

        session_key = rsa_decode(self.private_key, msg.body[426:])
        print("session_key类型: ", str(type(session_key)))
        self.public_keys[client_name] = public_key
        #self.Sessions[client_name] = Session(new_address, session_key)
        
        self.Sessions[client_name].set_key(session_key)
        print(self.Sessions[client_name].get_key())
        
        #body = json.dumps(list(self.Sessions.keys))
        body = [1]
        body.append("public")
        for k in list(self.Sessions.keys()):
            body.append(k)
        body = json.dumps(body)
        #self.locks[client_name].acquire()
        self.Sessions[client_name].send(Message(("login", "public", body.encode(encoding='utf_8'))))
        #self.locks[client_name].release()

        update_msg = Message(("update", client_name,  b"add"))
        self.broadcast(update_msg, False)

    def forward(self, to_who, msg):
        '''
        forwrd:
            转发客户端建立点对点连接的请求
            msg：
                type: connect
                username: msg_from_client_name
                body: json.dumps([to session_key from_addr]) session用接收客户端公钥加密
        '''
        print("辅助转发来自" + msg.username + "的连接请求")
        print("与"+ to_who + "的会话密钥: ")
        print(self.Sessions[to_who].get_key())
        
        #to_who = msg.body[30:(50-msg.body[50])].decode(encoding='utf_8')
        #self.locks[to_who].acquire()
        self.Sessions[to_who].send(msg)
        #self.locks[to_who].release()

    def logout(self, msg):
        '''
        logout:
            客户端注销, 关闭并删除对应会话，删除对应公钥
        '''
        print("注销 "+ msg.username)
        print(self.Sessions.keys())
        self.Sessions[msg.username].close()
        #self.Sessions_a[msg.username].close()
        del self.Sessions[msg.username]
        #del self.Sessions_a[msg.username]
        del self.public_keys[msg.username]
        
        t = threading.Thread(target=self.broadcast, args=([msg]))
        t.start()
        t.join()

    def get_pub(self, msg):
        '''
        get_pub:
            获取公钥
        msg:
            type: get_pub
            username: msg_from_client_name
            body: whose public_key the client want 
        '''
        print("请求 "+ msg.body.decode(encoding='utf_8') + "的公钥")
        #self.locks[msg.username].acquire()
        self.Sessions[msg.username].send(Message(("get_pub", msg.body.decode(encoding='utf_8') , self.public_keys[msg.body.decode(encoding='utf_8')].save_pkcs1())))
        #self.locks[msg.username].release()

    def run(self):
        '''
        run:
            开始监听
        '''
        #self.server_socket.listen()
        t = threading.Thread(target=self.handle_msg, args=())
        t.setDaemon(True)
        t.start()
        self.threads["main"] = t
        
        t1 = threading.Thread(target=self.handle_connect, args=())
        t1.setDaemon(True)
        t1.start()
        self.threads["assist"] = t1

    def cancel(self):
        '''
        cancel:
            服务器退出，断开会话
        '''
        self.status = False
        sleep(1)
        for c in list(self.Sessions.keys()):
            self.Sessions[c].close()
            del self.Sessions[c]

        self.Sessions = {}
        self.public_keys = {}

    def show(self):
        '''
        调试函数，用于解析命令行输入，打印出指定变量当时的值
        '''
        while 1:
            ops = input()
            ops = ops.split(":", -1)
            #print(ops)
            if ops[0] == "session_key":
                print("与" + ops[1] + "会话密钥: ")
                print(self.Sessions[ops[1]].get_key())
                continue
            
if __name__ == "__main__":
    server_ip = "127.0.0.1"
    #server_ip = ""
    server_port = 20000
    s = Server((server_ip, server_port))
    t = threading.Thread(target=s.run, args=())
    t.setDaemon(True)
    t.start()
    #t.join()
    t1 = threading.Thread(target=s.show, args=())
    t1.setDaemon(True)
    t1.start()
    print("press any key to exit...")
    while 1:
        sleep(1)
    s.cancel()
