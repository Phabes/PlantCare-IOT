# PlantCare-IOT

PlantCare is a prototype of a smart plant irrigation system based on the Node-RED environment. The garden irrigation control is based on the weather forecast. 

## System virtual devices

System contains two virtual devices:

* soil-sensor: checks the level of soil hydration and reacts to the low level case. Additionally, it has set a trigger for every morning and evening at fixed hours . Depending on the weather forecast for the day, irrigates the soil accordingly.
* sprinkler: thanks to mqtt broker, it listens for information about the need to water the soil and performs the task accordingly.

## Run application

All the components needed to run the system are stored in Docker containers. For easy running multi-container Docker applications, the ***docker-compose.yaml*** was created.

To run all necesary components:

```
docker compose up
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

<img width="1440" alt="Zrzut ekranu 2022-12-30 o 20 10 41" src="https://user-images.githubusercontent.com/61901509/210109152-6c384cac-4d97-4d4f-a111-4e799908c06e.png">

### Eclipse Mosquitto

To enable communication between virtual devices, the system use Eclipse Mosquitto - an open source (EPL/EDL licensed) message broker that implements the MQTT protocol. 

Functions used to manage the transmission:

* *Connect* – to establishes a connection with the broker,
* *Subscribe* – to subscribes (listens) to a given topic on the broker,
* *Publish* – to publishes (sends) information on a given topic, through a broker, to all clients subscribing to a given topic.

The system has two topics: soil-sensor and sprinkler.

### Weather

To get the information about the daily weather forecast we use the openweathermap API. 

### Redis

The level of the soil hydration is stored in the Redis database. Thanks to this approach, all the virtual devices have the access to this information. 

Default port: `"6379:6379"`

## Diagrams
