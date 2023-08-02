class Config:
    #MQTT Credintial
    BROKER = 'broker.hivemq.com'
    PORT = 1883
    TOPIC = "J412/1"
    CLIENT_ID = 'clientId-TOIS6zzrrm'
    USERNAME = 'emqx'
    PASSWORD = 'public'
    DEVICE_ID=1
    KEEPALIVE_INTERVAL=60

    COLLECT_DATA = True

    COM='COM7'