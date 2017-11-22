#from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json
from socket import *
import string
import random
#Crypto 来自 PyCryptodome、
import rsa

def do_dir(d, file):
    all_file = []
    for f in os.listdir(d):   #列出目录下的所以文件及目录
        f = os.path.join(d, f)  #通过os.path.join()函数，把两个路径合成一个时
        if os.path.isfile(f):    #判断是否是文件
            if os.path.splitext(f)[1] == '.' + file: #判断是否是需要的文件类型
                all_file.append(os.path.abspath(f)) #打印出绝对路径
        else:  #如果是目录，递归进行
            all_file += do_dir(f, file)

    return all_file

encty_types = ("connect", "msg")
g_code = "sustcech"
key_root = "./keys/"
def get_random_bytes(n):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return bytes(salt, 'utf_8')

def cb(data):
    if str(type(data)) != "<class 'bytes'>":
        return str(data).encode()
    return data

def generate_rsa_key(pre=""):
    '''
    generate_rsa_key: 产生rsa密钥对
    '''
    (pubkey, privkey) = rsa.newkeys(2048)

    pub = pubkey.save_pkcs1()
    pubfile = open(key_root + pre + '_public.pem','w+')
    pubfile.write(pub.decode(encoding='utf_8'))
    pubfile.close()

    pri = privkey.save_pkcs1()
    prifile = open(key_root + pre + '_private.pem','w+')
    prifile.write(pri.decode(encoding='utf_8'))
    prifile.close()

#RSA加密解密操作对象为bytes
import os
def load_keys(name):
    pub_path = key_root + name+"_public.pem"
    pri_path = key_root + name+"_private.pem"
    if not (os.path.exists(pub_path) and os.path.exists(pri_path)):
        generate_rsa_key(name)

    with open(pub_path) as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)

    with open(pri_path) as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)

    return (privkey, pubkey)

def rsa_encode(pub_key, data):
    '''
    rsa_encode: 使用公钥加密字符串
    '''
    print(len(data))
    encry_data = rsa.encrypt(data, pub_key)
    return encry_data

def rsa_decode(private_key, encry_data):
    '''
    rsa_decode: 使用私钥解密字符串
    '''
    print(type(encry_data))
    data = rsa.decrypt(encry_data, private_key)
    return data

def aes_encode(body, session_key):
    '''
    aes_encode: 使用会话密钥加密消息内容
    '''
    print('Begin')
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    print("init")
    print(cipher_aes.encrypt_and_digest(body))
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(body)
    encry_body = json.dumps([ciphertext, tag])
    return encry_body
    
def aes_decode(encry_body, session_key):
    '''
    aes_decode: 使用会话密钥解密消息内容
    '''
    ciphertext, tag = json.loads(encry_body)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    body = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return body

from binascii import b2a_hex, a2b_hex  
import threading
class Session:
    #只有当消息类型为msg时会用会话密钥加密解密
    def __init__(self, client_addr=["",""], session_key=b""):
        #self.client_ip = client_addr[0]
        #self.client_port = client_addr[1]
        #self.key = key  
        self.mode = AES.MODE_CBC 
        self.client_addr = client_addr
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.session_key = session_key
        self.lock = threading.Lock()

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数  
    def encrypt(self, text):  
        cryptor = AES.new(self.session_key, self.mode, self.session_key)  
        #text = text.encode("utf-8")  
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用  
        length = 16  
        count = len(text)  
        add = length - (count % length)  
        text = text + (b'\0' * add)  
        self.ciphertext = cryptor.encrypt(text)  
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题  
        #所以这里统一把加密后的字符串转化为16进制字符串  
        #return b2a_hex(self.ciphertext).decode("ASCII")
        return b2a_hex(self.ciphertext)
       
    #解密后，去掉补足的空格用strip() 去掉  
    def decrypt(self, text):  
        cryptor = AES.new(self.session_key, self.mode, self.session_key)  
        plain_text = cryptor.decrypt(a2b_hex(text))  
        #return plain_text.rstrip(b'\0').decode("utf-8")  
        return plain_text.rstrip(b'\0')

    def update_client(self, client_addr):
        '''
        update_client: 更新会话中对方地址
        client_addr: 对方的地址(ip, port)
        '''
        #self.client_ip = client_addr[0]
        #self.client_port = client_addr[1]
        self.client_addr = client_addr

    def get_key(self):
        '''
        get_key:
            返回当前会话的会话密钥
        '''
        self.lock.acquire()
        k = self.session_key
        self.lock.release()
        return k

    def set_key(self, key):
        self.lock.acquire()
        self.session_key = key
        self.lock.release()

    #msg 不用编码
    def send(self, msg):
        '''
        send: 发送信息，会根据消息在会话内加密

        msg: Message 对象
        '''
        print("在Session中发送消息")
        if msg.type == "msg":
            print("消息内容为: ", msg.body.decode(encoding='utf_8'))
            print(self.session_key)
            msg.body = self.encrypt(msg.body)
            print("加密后:")
            print(msg.body)

        self.lock.acquire()
        res = self.clientSocket.sendto(msg.__bytes__(), self.client_addr)
        self.lock.release()
        print("发送字节数: ", res)

    
    def recieve(self, need_addr=False):
        '''
            返回Message对象
        '''
        print("在Session中接收消息")
        msg, new_address = self.clientSocket.recvfrom(2048)
        if new_address[1] == self.client_addr[1]:
            self.update_client(new_address)
        msg = loads_msg(msg)
        
        if msg.type == "msg":
            msg.body = self.decrypt(msg.body)
            print("解密后消息内容为: " + msg.type+" "+msg.username + " " + msg.body.decode(encoding='utf_8'))

        if need_addr:
            return msg, new_address
        return msg
    
    def encode(self, body):
        return self.encrypt(body)

    def decode(self, body):
        return self.decrypt(body)

        
    def close(self):
        self.clientSocket.close()


class Message:
    '''
    Message: 
        统一消息结构体
    成员变量:
        type(str): 消息类型(disconnect, connect, msg, broadmsg, login, logout, get_pub, update)
        username(str): 发送这个消息的用户名，服务端默认public
        body(bytes): 消息内容
    '''
    def __init__(self, msg):
        self.type = msg[0]
        self.username = msg[1]
        self.body = msg[2]
        print("body类型为" + str(type(self.body)))
    
    
    def __str__(self):
        print("返回Message对象的操作类型以及发送人")
        print(type(self.body))
        json_msg = json.dumps([self.type, self.username])
        print(type(json_msg))
        return json_msg

    def __bytes__(self):
        #return json.dumps([self.type, self.username, self.body]).encode(encoding='utf_8')
        print("将Message对象转bytes")
        data = self.type.encode()
        l = 20 - len(self.type.encode())
        for i in range(l):
            data+= bytes([l])
        data += self.username.encode()
        l = 30 - len(self.username.encode())
        for i in range(l):
            data+= bytes([l])
        
        if str(type(self.body)) == "<class 'str'>":
            data += self.body.encode()
        else:
            data += self.body

        return data
        
        

def loads_msg(bytes_msg):
    '''
    loads_msg:
        将序列化的Message对象的json字符串还原成Message对象并返回
    '''
    print("将bytes转为Message对象，body保留bytes")
    msg_type = bytes_msg[0:(20-bytes_msg[19])].decode(encoding='utf_8')
    msg_username = bytes_msg[20:(50-bytes_msg[49])].decode(encoding='utf_8')
    if len(bytes_msg) > 50:
        msg_body = bytes_msg[50:]
    else:
        msg_body = b''

    return Message((msg_type, msg_username, msg_body))
    #return Message(tuple(json.loads(json_msg)))

class chat_record():
    '''
    chat_record:
        聊天消息类，用于存储消息是谁发的，以及消息内容，如果是自己的话用"me"代替自己的用户名
    
    func:
        __init__:
            who: 消息来源
            msg: 消息内容
        
        __str__:
            返回格式化的消息-> who:msg

    '''
    def __init__(self, who, msg):
        self.who = who
        self.msg = msg

    def __str__(self):
        return self.who + ": " + self.msg

class stack():
    '''
    stack:
        线程安全的栈，为了拿来存储ui的提示信息

    arr:
        str数组用于存储tips
    len:
        当前未读的有效消息数
    lock:
        锁，防止线程同时读写变量
    '''

    def __init__(self, max_len=20):
        self.arr = []
        self.lock = threading.Lock()
        self.len = 0
    
    def remove_by_name(self, name):
        '''
        删除所有包含name的提示
        '''
        self.lock.acquire()
        tmp_arr = self.arr
        i = 0
        while i<self.len:
            if name in self.arr[i]:
                if i == (self.len-1):
                    self.len -= 1
                else:
                    self.arr[i:(self.len-1)] = tmp_arr[(i+1):self.len]
                    self.len -= 1
                i -= 1
            i+=1
            
        self.lock.release()
        
    def pop(self):
        '''
        弹出最新的tip并返回
        '''
        self.lock.acquire()
        tmp = self.arr[self.len-1]
        self.len -= 1
        self.lock.release()
        return tmp

    def peak(self):
        '''
        返回最新的tip
        '''
        self.lock.acquire()
        p = self.arr[self.len-1]
        self.lock.release()
        return p

    def push(self, ele):
        '''
        加入一条最新的tip到栈顶
        '''
        self.lock.acquire()
        if self.len < len(self.arr):
            self.arr[self.len] = ele
        else:
            self.arr.append(ele)
        
        self.len += 1
        self.lock.release()

    def get_len(self):
        '''
        获取提示栈中未读且有效的消息数
        '''
        self.lock.acquire()
        l = self.len
        self.release()
        return l