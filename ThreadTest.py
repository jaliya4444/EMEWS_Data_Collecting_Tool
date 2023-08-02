import threading
from time import sleep

def tesetInstruct():
    print ("start")
    sleep(1)
    print ("end")


for x in range(1,2000):
    print(x)
    if(x%500==0):
        t=threading.Thread(target=tesetInstruct)
        t.start()
