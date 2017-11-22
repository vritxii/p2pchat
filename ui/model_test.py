import time
import threading

class Test():
    def __init__(self):
        self.status = -1
        self.lock = threading.Lock()

    def login(self):
        self.lock.acquire()
        self.status = 1
        self.lock.release()
        self.hehe = 12

    def get_status(self):
        s = self.status
        return s

class Ha():

    def __init__(self):
        self.t = Test()

    def login(self):
        self.t.login()

    def get_status(self):
        return self.t.get_status()

if __name__ == "__main__":
    ha = Ha()
    t = threading.Thread(target=ha.login, args=())
    t.start()
    time.sleep(0.5)
    print(ha.get_status())
    print(ha.t.hehe)