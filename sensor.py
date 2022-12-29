import time

import paho.mqtt.client as mqtt

humidity = 100

def on_publish(mqttc, obj, mid):
    print(humidity)


client = mqtt.Client()
client.on_publish = on_publish

client.connect("localhost", 1883, 60)

while True:
    client.publish("soil-sensor", humidity, 0, False)
    time.sleep(1)

    if not humidity == 0:
        humidity -= 1
