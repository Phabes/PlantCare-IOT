import time

while True:
    if humidity == 0:
        continue

    humidity -= 1

    time.sleep(1)
