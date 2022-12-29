import datetime
import time
import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient

mongo_client = MongoClient("mongodb+srv://qwerty:qwerty123@plantcare-iot.q0i3fmr.mongodb.net")
db = mongo_client.PlantCare
collection = db.Soil


''' JSON Message to sprinkler:
{
    "turn": true/false [bool]
    "time": float      [number_of_minutes]
}
'''


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    if payload['turn']:
        print("turning on watering for " + str(payload['time']) + " min")

        end_time = datetime.datetime.now() + datetime.timedelta(minutes=payload['time'])
        while True:
            if datetime.datetime.now() >= end_time:
                break
            else:
                data = list(collection.find({}))
                humidity = data[0]["humidity"]
                print(humidity)
                if humidity == 100:
                    continue

                updateResult = collection.update_one({'humidity': humidity}, {'$set': {'humidity': humidity + 1}})

                time.sleep(0.2)
        print("watering finished")
        return

    if not payload['turn']:
        print("turning off watering")

        return


client = mqtt.Client()
client.on_message = on_message
client.max_inflight_messages_set(1)
client.connect("localhost", 1883, 60)
client.subscribe("sprinkler", 0)
client.loop_forever()
