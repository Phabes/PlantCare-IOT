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

## Docker

There are 3 images used:

- **MQTT**
  For the MQTT server we used the Eclipse Mosquitto image (https://hub.docker.com/_/eclipse-mosquitto)

  ![Dockercompose-mosquitto](./images/Dockercompose-mosquitto.png)

- **Node-RED**
  Image is built using Dockerfile. Based on nodered/node-red image (https://hub.docker.com/r/nodered/node-red)

  ![Dockerfile](./images/Dockerfile.png)

  _package.json_ file contains all required dependencies for node-red and scripts to run it:

  ![Packagejson](./images/packagejson.png)

  _soil_data_9_ file stores data for charts. \
  _settings.js_ file stores settings that are loaded into the runtime as a Node.js module that exports a JavaScript object of key/value pairs. \
  _flows_cred.js_ is credentials file. It is encrypted by default to ensure its contents cannot be easily read. We provides the key for the encryption in the settings.js file. If another instance of Node-RED doesn't have the same encryption key, it won't be able to decrypt the file. \
  _flows.js_ file stores the node-red flow which is loaded and then run when application starts.

  Dockerfile is used to build the image inside docker-compose file:

  ![Nodered](./images/Dockercompose-nodered.png)

- **Redis**
  For the Redis we used the Redis image (https://hub.docker.com/_/redis)

  ![Redis](./images/Dockercompose-redis.png)

All 3 images are put inside one container using docker-compose which lets us set up and run all images using one docker command.
All images are connected with the same network: _iot-planet-net_.

![Dockercompose](./images/Dockercompose.png)

## Python scripts

All scripts use redis to share one soil which is represented by an integer value called _humidity_. 0 is the minimum value and 100 is the maximum value.

- **soil**
  It is a script to simulate soil's behaviour. Every 1 second humidity value is decrement by 1.

  ![Soil](./images/soil.png)

  _humidity_ value cannot be smaller than 0 (it is the minimum value).

- **sensor**
  It is a script to simulate sensor's behaviour. Every five seconds it reads humidity value and publishs it to the MQTT server to the _soil-sensor_ topic.

  ![Sensor](./images/sensor.png)

- **sprinkler**
  It is a script to simulate sprinkler's behaviour. It listens to the _sprinkler_ topic messages from the MQTT server. Messages processed by the sprinkler must be of the given JSON format:

  ```
    {
        "turn": bool       [turn spinkler on / turn spinkler off],
        "time": float      [number of minutes that watering should last]
    }
  ```

  When a message comes in with the turn value set to _true_ it starts watering which lasts the time value number of seconds . _humidity_ value is incremented by 1 every 200 miliseconds.

  ![Watering](./images/watering.png)
