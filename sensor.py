import time
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("localhost", 1883, 60)

while True:
    client.publish("soil-sensor", humidity, 0, False)
    time.sleep(5)
