import time
from pymongo import MongoClient

mongo_client = MongoClient("mongodb+srv://qwerty:qwerty123@plantcare-iot.q0i3fmr.mongodb.net")
db = mongo_client.PlantCare
collection = db.Soil

while True:
    data = list(collection.find({}))
    humidity = data[0]["humidity"]
    if humidity == 0:
        continue
    updateResult = collection.update_one({'humidity': humidity}, {'$set': {'humidity': humidity - 1}})
    time.sleep(1)
