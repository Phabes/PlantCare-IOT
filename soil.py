import time

import redis as redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set("humidity", 100)

while True:
    humidity = int(r.get("humidity"))
    if humidity == 0:
        continue

    r.set("humidity", humidity - 1)

    time.sleep(1)
