from extra import stack
import threading
from time import sleep
q = stack()

def add_ele(dt, p=False):
    global q
    for i in range(5):
        q.push(str(i+i*int(p)))
        sleep(dt)
    
if __name__ == "__main__":
    t = threading.Thread(target=add_ele, args=([0.5]))
    t.start()
    t1 = threading.Thread(target=add_ele, args=([0.5, True]))
    t1.start()
    i=0
    while i<15:
        sleep(0.2)
        print(q.arr)
        i+=1

    print("*********")
    for i in range(3):
        q.remove_by_name(str(i))
    
    print(q.arr[:q.len])
    