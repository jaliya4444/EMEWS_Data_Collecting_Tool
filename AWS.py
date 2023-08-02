from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


class AWS:
    def __init__(self,TOPIC):
        # Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
        ENDPOINT = "a1c8l7kio0mxsk-ats.iot.ap-northeast-1.amazonaws.com"
        CLIENT_ID = "basicPubSub"
        PATH_TO_CERTIFICATE = "certificates/test_thing.cert.pem"
        PATH_TO_PRIVATE_KEY = "certificates/test_thing.private.key"
        PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root-CA.crt"
        MESSAGE = "Hello World"
        self.TOPIC = "device_{0}".format(TOPIC)
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6)
        print("Connecting to {} with client ID '{}'...".format(
            ENDPOINT, CLIENT_ID))
        # Make the connect() call
        connect_future = self.mqtt_connection.connect()
        # Future.result() waits until a result is available
        connect_future.result()
        print("Connected!")
        # Publish message to server desired number of times.

    def push_details(self, data):
        print('Begin Publish')
        message = {"message":str(data)}
        self.mqtt_connection.publish(topic=self.TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")

    # def __del__(self):
    #     disconnect_future = self.mqtt_connection.disconnect()
    #     disconnect_future.result()
