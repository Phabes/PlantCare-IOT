import time

import paho.mqtt.client as mqtt

humidity = 30


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

client.connect("localhost", 1883, 60)

# client.subscribe("garden", 0)
while (True):
    client.publish("garden", humidity, 0, False)
    time.sleep(1)
    humidity -= 1
    if humidity == 22:
        humidity = 83
# client.loop_forever()
