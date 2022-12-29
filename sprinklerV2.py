import datetime
import time
import paho.mqtt.client as mqtt
import json

''' JSON Message to sprinkler:
{
    "turn": true/false [bool]
    "time": float      [number_of_minutes]
}
'''
humidity = 0


def on_message(client, userdata, msg):
    global humidity
    payload = json.loads(msg.payload)

    if payload['turn']:
        print("turning on watering for " + str(payload['time']) + " min")

        end_time = datetime.datetime.now() + datetime.timedelta(minutes=payload['time'])
        while True:
            if datetime.datetime.now() >= end_time:
                break
            else:
                print("watering")
                humidity += 1
                time.sleep(0.15)

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
