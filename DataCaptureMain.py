from CommUtil import CommUtil
import pandas as pd
import datetime
import serial as sr
import threading
from Config import Config
import paho.mqtt.client as mqtt
import time as t


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("Message published with mid: "+str(mid))

def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(Config.BROKER, Config.PORT)
    return client

def publish_heatbeat(client):
    client.on_publish = on_publish
    client.publish(Config.TOPIC, "HB")

if __name__ == "__main__":
    lgr = CommUtil.set_loggger('Data Capture Main')
    lgr.info('---' * 20)
    lgr.info('Data Capture Main')
    start_time = datetime.datetime.now()
    lgr.info('Start time {0}'.format(start_time))

    df = pd.DataFrame()

    i=0
    time_stamp=0

    #list for store the data
    df_list = []

    #Mqtt Start
    client = connect_mqtt()
    # Start the loop to process network traffic and dispatch callbacks
    client.loop_start()

    try:
        lgr.info('Data Capture Start')
        s = sr.Serial(Config.COM, 115200)
        reading_index = 0
        while (Config.COLLECT_DATA):

            line = bytearray()
            byte = s.read()
            while byte != b'\n':
                line += byte
                byte = s.read()
            line = s.readline()
            line_str = line.decode('utf-8', 'ignore')
            vals = line_str.split(",")
            time_stamp = time_stamp + int(vals[0])
            amplitude = int(vals[1])
            reading_index = reading_index + 1

            current_time = "{0:%Y%m%d%H%M%S}".format(datetime.datetime.now())
            
            #----Dummy data 
            #amplitude = 100
            #time_stamp=current_time
            #amplitude=amplitude+1

            new_row = {'id':reading_index,'s_id': len(df_list) + 1,'stamp':current_time,'time': time_stamp, 'amplitude': amplitude}
            df_list.append(new_row)



            if (len(df_list) % 10000) == 0:
                lgr.info('enable heartbeat at '+ str(len(df_list)))
                
                df = pd.DataFrame(df_list)
                df.to_csv(r'output/data_{0:%Y%m%d%H%M%S}.csv'.format(datetime.datetime.now()),index=False)
                thread = threading.Thread(target=publish_heatbeat, args=(client,), daemon=True)
                thread.start()

                # clear the dataframe
                df.drop(index=df.index, columns=None, inplace=True)
                #clear the list
                df_list=[]
    except Exception as e:
        lgr.error(str(e))

    except KeyboardInterrupt:
        lgr.info("Manual interruption")

    df.to_csv(r'output/data_{0:%Y%m%d%H%M%S}.csv'.format(datetime.datetime.now()), index=False)
    lgr.info('---' * 20)
    lgr.info('Completed at {1}. Time taken {0}'.format(datetime.datetime.now() - start_time, lgr.info('---' * 20)))
