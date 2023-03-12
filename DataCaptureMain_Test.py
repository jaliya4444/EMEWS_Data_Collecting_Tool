from CommUtil import CommUtil
import pandas as pd
import datetime
import serial as sr
import threading

from Config import Config
from paho.mqtt import client as mqtt_client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(Config.CLIENT_ID)
    client.username_pw_set(Config.USERNAME, Config.PASSWORD)
    client.on_connect = on_connect
    client.connect(Config.BROKER, Config.PORT)
    return client

def send_MQTT():
    lgr.info('sending')
    client = connect_mqtt()
    topic = "EMEWS/mqtt/heartbeat"
    msg = f"messages: ok"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0 :
        lgr.info(f"Send `{msg}` to topic `{topic}`")
    else :
        lgr.error(f"Failed to send message to topic {topic}")

    lgr.info('send done')

if __name__ == "__main__":
    lgr = CommUtil.set_loggger('Data Capture Main')
    lgr.info('---' * 20)
    lgr.info('Data Capture Main')
    start_time =datetime.datetime.now()
    lgr.info('Start time {0}'.format(start_time))


    df=pd.DataFrame()
    try:
        lgr.info('Data Capture Start')
        s = sr.Serial(Config.COM, 115200)
        while (Config.COLLECT_DATA) :
            line = s.readline()
            line_str = line.decode()
            vals = line_str.split(",")
            time = time + int(vals[0])
            amplitude = int(vals[1])

            if (len(df) %1000)==0:
                lgr.info('enable heartbeat')
                new_row = {'id' : len(df) + 1, 'time' : time, 'amplitude' :amplitude,'heartbeat':True}
                df = df.append(new_row, ignore_index=True)
                lgr.info(new_row)
                # thread = threading.Thread(target=send_MQTT(), daemon=True)
                # thread.start()
                df.to_csv(r'output/data_{0:%Y%m%d%H%M%S}.csv'.format(datetime.datetime.now()))
            else:
                new_row = {'id' : len(df) + 1, 'time' : time, 'amplitude' : amplitude,'heartbeat':False}
                df = df.append(new_row, ignore_index=True)
                lgr.info(new_row)
    except Exception as e:
        lgr.error(str(e))

    lgr.info('---' * 20)
    lgr.info('Completed at {1}. Time taken {0}'.format(datetime.datetime.now() - start_time, lgr.info('---' * 20)))
