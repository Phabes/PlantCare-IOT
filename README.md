# PlantCare-IOT

PlantCare is a prototype of a smart plant irrigation system based on the Node-RED environment. The garden irrigation control is based on the weather forecast.

## System virtual devices

System contains two virtual devices:

- soil-sensor: checks the level of soil hydration and reacts to the low level case. Additionally, it has set a trigger for every morning and evening at fixed hours . Depending on the weather forecast for the day, irrigates the soil accordingly.
- sprinkler: thanks to mqtt broker, it listens for information about the need to water the soil and performs the task accordingly.

## Run application

All the components needed to run the system are stored in Docker containers. For easy running multi-container Docker applications, the **_docker-compose.yaml_** was created.

To run all necesary components:

```
docker compose up -d
docker build -t node-red .
docker run -p 1880:1880 --network iot_iot-plant-net -d node-red
```

To run Python files:

```
python sensor.py
python soil.py
python sprinkler.py
```

## Tools

### NodeRed

Default server is `http://127.0.0.1:1880/`

System layout:

![321652927_441119368099957_4397307115607273046_n](https://user-images.githubusercontent.com/61901509/210244740-181e4a5e-9623-4f61-846a-8e8b3ed9e008.png)

### Eclipse Mosquitto

To enable communication between virtual devices, the system use Eclipse Mosquitto - an open source (EPL/EDL licensed) message broker that implements the MQTT protocol.

Functions used to manage the transmission:

- *Connect* – to establishes a connection with the broker,
- *Subscribe* – to subscribes (listens) to a given topic on the broker,
- *Publish* – to publishes (sends) information on a given topic, through a broker, to all clients subscribing to a given topic.

The system has two topics: soil-sensor and sprinkler.

### Weather

To get the information about the daily weather forecast we use the openweathermap API.

### Redis

The level of the soil hydration is stored in the Redis database. Thanks to this approach, all the virtual devices have the access to this information.

Default port: `"6379:6379"`

## Diagrams

![321906699_470752491919449_5381184498221539571_n](https://user-images.githubusercontent.com/61901509/210244601-e0b977d2-851e-48e0-8282-bc53b10b3100.png)

![321237787_887107109398009_5403797075088989886_n](https://user-images.githubusercontent.com/61901509/210244605-76a32d88-c0c4-4a60-9130-3b0775472291.png)

![321922610_723402209343127_850382364625469373_n](https://user-images.githubusercontent.com/61901509/210244975-95924b3b-1957-4304-9ce4-1b7c726c2f38.png)


