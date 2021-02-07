# A gentle guide to home automation with docker-compose - Part 1
This is the first part of posts about using `docker-compose` for home automation published on [hackerclub.io](https://hackerclub.io). You can read it [here](https://hackerclub.io/).

In this part, we introduce some of the main components in our setup: Docker, MQTT, Home Assistant, and smart devices as sensors and switches. We build code to "simulate" sensors and switches, so we can quickly set up a playground with `docker-compose`.

# Simulated smart devices
We use Python code to simulate some smart devices such as sensors and switches. The code for these simulated devices is in [fake-devices/](./fake-devices).

# Run it!
To get started, clone this repo and run `docker-compose up`:
```bash
$ git clone git@github.com:hacker-club/homeauto-docker-compose.git
$ cd homeauto-docker-compose/part1/
$ docker-compose up
```
You should be able to access Home Assistant at [localhost:8132](http://localhost:8123/) using username `homeassistant` and password `homeassistant`.

# Some useful commands
## docker-compose
1. Bring `docker-compose` up and start all containers:
```
$ docker-compose up
```
2. Bring `docker-compose` down and stop all containers:
```
$ docker-compose up
```
3. Remove all containers
Once stopped (with `docker-compose down`), the containers are not running anymore, but data associated with them is still persisted. To wipe it, run:
```
$ docker-compose rm
```
## mosquitto
Mosquitto is our MQTT broker. We run it as a container via `docker-compose`.
The following volumes are mounted from `host` => `container` (check in `docker-compose.yml`):
- `conf/mosquitto` => `/mosquitto/config`
- `data/mosquitto` => `/var/lib/mosquitto`

### Executing MQTT commands inside the `mosquitto` container
Once `docker-compose up` has been run, our `mosquitto` container is up and ready. We can execute commands from inside of it by using `docker-compose exec mosquitto <command>`. Some useful commands are:

1. `mosquitto_pub` publishes a message to a MQTT topic:
```
$ docker-compose exec mosquitto mosquitto_pub -t some/topic -u mqttuser -P mqttpassword -m "hello, mosquitto!"
```
2. `mosquito_sub` subscribes to a MQTT topic:
```
$ docker-compose exec mosquitto mosquitto_sub -t some/topic -u mqttuser -P mqttpassword
```

3. Username/password management
In this repo, we already set up a username and password to get things going (`mqttuser:mqttpassword` - for demonstration purposes only). This password was set up using the `mosquitto_passwd` command from inside the `mosquitto` container. The generated password file (`/mosquitto/config/password_file`) contains the username and a hash of the password ([docs](https://mosquitto.org/man/mosquitto-conf-5.html)):
```
$ docker-compose exec -it mosquitto mosquitto_passwd -c /mosquitto/config/password_file mqttuser
```

#### Try it
Using `mosquitto_pub` and `mosquito_sub` as above, try subscribing to a topic and publishing to it from a different terminal window. The subscriber should be notified when the publisher writes its message.

## home-assistant
You can access the home-assistant UI at [localhost:8123](http://localhost:8123).

### Credentials
Usually, you would be asked to set up your credentials upon first access. In this demonstration, we have pre-setup the username `homeassistant` and password `homeassistant`.

### MQTT
You can install MQTT as an addon from within home-assistant, but in this demonstratino I set up a separate mqtt broker in the `docker-compose.yml` file (`mosquitto`). This option is described in home-assistant docs under [mqtt - run your own](https://www.home-assistant.io/docs/mqtt/broker#run-your-own).

# Auto discovery
home-assistant can automatically discover smart devices in your network. One way is via MQTT (see [MQTT discovery docs](https://www.home-assistant.io/docs/mqtt/discovery/)).
MQTT discovery works by having smart devices "announce" themselves by writing their configurations to an agreed topic in mqtt. In this repository, I use the default discovery topic, `homeassistant/`.

# Simulated devices discovery
You can see the MQTT discovery in action with the fake devices in this repo. [Here's how fake sensors register themselves](./fake-devices/src/sensors.py).