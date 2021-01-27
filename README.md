# A gentle guide to home automation with docker-compose
This repository holds code for the blog post [Home automation with docker-compose: a gentle guide](https://hackerclub.io).

The code is organized in _parts_. Each step builds on top of the previous, so we incrementally build a more feature rich home automation system with more moving parts:

## Part 1
In this step, we introduce the main concepts (such as MQTT, Home Assistant, sensors, switches and Docker). We put together a minimal `docker-compose` file that orchestrates an MQTT broker, Home Assistant and some emulated/faked smart devices.

To get started, simply clone this repo and run `docker-compose up`:
```bash
$ git clone git@github.com:hacker-club/homeauto-docker-compose.git
$ cd homeauto-docker-compose
$ docker-compose up
```
When docker compose boots up, visit [localhost:8132](http://localhost:8123/) and log in with username `homeassistant` and password `homeassistant`. You will see the Home Assistant dashboard with some simulated sensors.

## Part 2
We start getting fancier by introducing _automation_. We will be able to say "if the office motion detector senses somebody's presence, turn on the light" or "turn on the AC if the bedroom temperature is over X degrees". To this end, we include the amazing [Node-RED](https://nodered.org/) container to our `docker-compose` file.

## Part 3
It's all about data persistence and visualization. We will introduce the [InfluxDB](https://www.influxdata.com/) as a time-series database for storing our data over time and [Grafana](https://grafana.com/) for visually querying our data.

## Part 4
Making it secure. We will remedy some of the security bad practices we introduced in the name of making the introduction easier to follow along. These include securing usernames and passwords, and making a case for denying all access through the public internet. We also briefly touch on VPNs.

# Security considerations
This goal of the repository is to provide a gentle introduction and educational material. This means that, specially in the first steps, we have some default credentials pre-setup so you can get your feet wet with a pre-configured system with fake emulated smart devices: we can simply run `docker-compose` and open your browser instead of having to set up everything from scratch.
In part 4, we introduce better approaches for handling credentials and making our installation safer. This is closer to what we would use in the real-world.

# Emulated/faked smart devices
Unfortunally cannot ship real hardware sensors and smart switches to all of our readers. We instead introduce a collection of "simulated" smart devices so we can play around with our home automation system. They are defined in [fake-devices/](https://github.com/hacker-club/homeauto-docker-compose/tree/main/fake-devices):
- A [`FakeSensor`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/fake-devices/src/sensors.py) periodically draws a random number and publishes its value like a real sensor would;
- A [`FakeBinarySensor`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/fake-devices/src/binary_sensors.py) simulates a device that has only two states. For example:
  * a lock sensor can be either open or close
  * a motion can be either be triggered or inactive
- A [`FakeSwitch`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/fake-devices/src/switches.py) listens to commands (like turn on, turn off) and report their state (on or off) as a real smart switch would;
We discuss these emulated devices in part 1.

# docker-compose
## Some useful commands
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
# mosquitto
The following volumes are mounted from `host` => `container` (check in `docker-compose.yml`):
- `conf/mosquitto` => `/mosquitto/config`
- `data/mosquitto` => `/var/lib/mosquitto`

## Executing MQTT commands inside the `mosquitto` container
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

### Try it
Using `mosquitto_pub` and `mosquito_sub` as above, try subscribing to a topic and publishing to it from a different terminal window. The subscriber should be notified when the publisher writes its message.

# home-assistant
You can access the home-assistant UI at [localhost:8123](http://localhost:8123).

## Credentials
Usually, you would be asked to set up your credentials upon first access. In this demonstration, we have pre-setup the username `homeassistant` and password `homeassistant`.

## MQTT
You can install MQTT as an addon from within home-assistant, but in this demonstratino I set up a separate mqtt broker in the `docker-compose.yml` file (`mosquitto`). This option is described in home-assistant docs under [mqtt - run your own](https://www.home-assistant.io/docs/mqtt/broker#run-your-own).

## Auto discovery
home-assistant can automatically discover smart devices in your network. One way is via MQTT (see [MQTT discovery docs](https://www.home-assistant.io/docs/mqtt/discovery/)).
MQTT discovery works by having smart devices "announce" themselves by writing their configurations to an agreed topic in mqtt. In this repository, I use the default discovery topic, `homeassistant/`.

### Fake devices discovery
You can see the MQTT discovery in action with the fake devices in this repo. [Here's how fake sensors register themselves](./fake-devices/src/sensors.py).