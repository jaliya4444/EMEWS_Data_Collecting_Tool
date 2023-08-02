import paho.mqtt.client as mqtt

# Define callback functions for different events
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    print("Message published")

# Connect to the MQTT broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("broker.hivemq.com", 1883)

# Publish a message
topic = "J412/1"
message = "Hello, MQTT!"
client.publish(topic, message)

# Start the loop to process network traffic and dispatch callbacks
client.loop_forever()