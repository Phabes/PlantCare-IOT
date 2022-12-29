import datetime
import time
import paho.mqtt.client as mqtt
import json
import redis as redis

''' JSON Message to sprinkler:
{
    "turn": true/false [bool]
    "time": float      [number_of_minutes]
}
'''

r = redis.Redis(host='localhost', port=6379, db=0)


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    print("Got msg: " + str(payload))

    if payload['turn']:
        print("turning on watering for " + str(payload['time']) + " min")

        end_time = datetime.datetime.now() + datetime.timedelta(minutes=payload['time'])
        while True:
            if datetime.datetime.now() >= end_time:
                break
            else:
                humidity = int(r.get("humidity"))

                if humidity == 100:
                    continue

                humidity += 1

                r.set("humidity", humidity)

                time.sleep(0.2)
        print("watering finished")
        return

    if not payload['turn']:
        print("turning off watering")

        return


client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sprinkler", 0)
client.loop_forever()
