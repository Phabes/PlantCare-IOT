import time
import paho.mqtt.client as mqtt
import redis as redis

r = redis.Redis(host='localhost', port=6379, db=0)

client = mqtt.Client()

client.connect("localhost", 1883, 60)

while True:
    client.publish("soil-sensor", int(r.get("humidity")), 0, False)
    time.sleep(5)
