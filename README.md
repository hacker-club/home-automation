# A gentle guide to home automation with docker-compose
This repository holds code for a series of blog posts called "A gentle guide to home automation with docker-compose", published on [hackerclub.io](https://hackerclub.io).

The posts and code are organized in _parts_. Each part builds on top of the previous ones, so we incrementally build a more feature rich home automation system with more moving parts. Using our `docker-compose` files in each part, you should be able to bring up a working environment with all the described components with a single command.

## Part 1
We introduce some of the main components in our setup: MQTT and smart devices such as sensors and switches. We build code to "simulate" sensors and switches, which we will use to get a better understanding of MQTT. Check it out at [part1/](./part1).

## Part 2
We take a closer look at Docker, Docker Compose and how they can help us. We use Docker to run our very own MQTT broker and take a look at how we can containerize the simulated devices we built in part 1.

## Part 3
We get fancier by introducing Home Assistant as a central directory of smart devices and Node-RED for automation. We will be able to say: "if the office motion detector senses somebody's presence, turn on the office light" or "turn on the AC if the bedroom temperature is over X degrees".

## Part 4
It's all about data persistence and visualization. We will introduce the [InfluxDB](https://www.influxdata.com/) as a time-series database for storing our data over time and [Grafana](https://grafana.com/) for visually querying our data. These two new additions to our `docker-compose` file will play along nicely with the ones from step 2.

## Part 5
Making it secure. We will remedy some of the security concessions we made in the name of simplicity. We will secure usernames and passwords, and make a case for denying all access through the public internet. We also briefly touch on VPNs and how they can help us.

# Security considerations
This goal of the repository is to provide a gentle introduction and educational material for using `docker-compose` in home automation. We build up progressively complex `docker-compose` files that spin up different services with default credentials. This makes it easy for us to learn and try different things out. In part 4, we introduce better approaches for handling credentials and making our installation safer. This is closer to what we would use in the real-world.

# Simulated smart devices
Unfortunally cannot ship real hardware sensors and smart switches to all of our readers. We instead introduce a collection of "simulated" smart devices so we can play around with our home automation system. They are defined in [part1/fake-devices/](https://github.com/hacker-club/homeauto-docker-compose/tree/main/part1/fake-devices):
- A [`FakeSensor`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/part1/fake-devices/src/sensors.py) periodically draws a random number and publishes its value like a real sensor would;
- A [`FakeBinarySensor`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/part1/fake-devices/src/binary_sensors.py) simulates a device that has only two states. For example:
  * a lock sensor can be either open or close
  * a motion can be either be triggered or inactive
- A [`FakeSwitch`](https://github.com/hacker-club/homeauto-docker-compose/blob/main/part1/fake-devices/src/switches.py) listens to commands (like turn on, turn off) and report their state (on or off) as a real smart switch would;
-
We discuss these simulated devices in part 1.