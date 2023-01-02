import datetime
import time
import paho.mqtt.client as mqtt
import json
import redis as redis
from threading import Thread

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def watering(redis):
    while True:
        time.sleep(0.2)
        watering = str(redis.get("watering"))
        if watering == "True":
            humidity = int(r.get("humidity"))
            if humidity == 100:
                continue
            humidity += 1
            redis.set("humidity", humidity)
            print("watering")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print("Got msg: " + str(payload))
    if payload['turn']:
        if str(r.get("watering")) != "True":
            print("turning on watering for " + str(payload['time']) + " min")
            r.setex("watering", datetime.timedelta(minutes=payload['time']), value="True")
        else:
            print("Watering is turned on")
    else:
        print("turning off watering")
        r.set("watering", "False")

# Sprinkler is separate thread that checks if "watering" key is set in redis
# if yes it changes humidity value

try:
   t = Thread(target=watering, args=[r])
   t.start()
except:
   print("Error: unable to start watering thread")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sprinkler", 0)
client.loop_forever()


