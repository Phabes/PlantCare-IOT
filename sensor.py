import time
import paho.mqtt.client as mqtt
from pymongo import MongoClient

mongo_client = MongoClient("mongodb+srv://qwerty:qwerty123@plantcare-iot.q0i3fmr.mongodb.net")
db = mongo_client.PlantCare
collection = db.Soil

client = mqtt.Client()

client.connect("localhost", 1883, 60)

while True:
    data = list(collection.find({}))
    humidity = data[0]["humidity"]
    client.publish("soil-sensor", humidity, 0, False)
    time.sleep(5)
