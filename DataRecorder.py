import serial as sr
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import threading
import time
import csv
import serial.tools.list_ports

#MQTT Credintial
broker = 'broker.emqx.io'
port = 1883
topic = "EM/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
#username = 'emqx'
#password = 'public'


DEVICE_ID=1                                                    #Deivce ID Unieque to Device
attempts=1                                                     #attempt of collecting data

data_set=np.array([])
time_set=np.array([])

time = 0

heartbeat_flag=False;                                           #flag for heart beat                                                                                           

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print (p)

collect_data=True;


def collectData():
    global data
    global ind
    global time

    file_name=DEVICE_ID+"Data_set "+attempts+".csv"
    attempts+=1

    s=sr.Serial('COM6',115200)    
    temp_index=0;  
    while(collect_data):
        try:
            line=s.readline()
            line_str=line.decode()
            vals=line_str.split(",")
            time=time+int(vals[0])
            amplitude=int(vals[1])

            with open(file_name, 'a+') as f:
                writer = csv.writer(f,delimiter=",",lineterminator="\r")
                writer.writerow([time,amplitude])
                index+=1
                
                #if 10000 data points are collected make the heartbeat true
                if(temp_index>=10000):
                    heartbeat_flag=True
                    temp_index=0
                

        except Exception as e:
            print(e)

    s.close()
    f.close()     
 

def heartBeat():
    while True:
        if(heartbeat_flag==True):
            #Send MQTT beat
            heartbeat_flag=False
        time.sleep(5)   


collect = threading.Thread(target=collectData)
hbeat=threading.Thread(target=heartBeat)

collect.start()
hbeat.start()


collect_data=False;
print("Application ended");

    



