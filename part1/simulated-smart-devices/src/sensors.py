import json
import paho.mqtt.client as mqtt
import random
import time
import threading

from dataclasses import dataclass
from typing import Dict

from mqtt import FakeMQTTDevice


class FakeSensor(FakeMQTTDevice):
    """Defines a fake sensor.

    Objects of this class have periodically publish a random value to the MQTT topic `state_topic`.
    To add some real-world feeling to it, random values are drawn from a normal distribution with mean
    `value_mean` and standard deviation `value_stddev`.

    Moreover, objects of this class make themselves "discoverable" by other devices by
    publishing their configuration to the MQTT topic homeassistant/switch/fake-switches/<id>/config.
    This allows for home-assistant to automatically find them (https://www.home-assistant.io/docs/mqtt/discovery/).

    The `icon` argument defines how this device is represented in home-assistant. Possible values are in
    https://pictogrammers.github.io/@mdi/font/5.3.45/.
    """

    def __init__(
        self,
        id: str,
        name: str,
        icon: str,
        state_topic: str,
        value_mean: float,
        value_stddev: float,
        unit: str,
        transmission_interval_seconds: float,
    ):
        super(FakeSensor, self).__init__()
        self.id = id
        self.name = name
        self.icon = icon
        self.state_topic = state_topic
        self.value_mean = value_mean
        self.value_stddev = value_stddev
        self.unit = unit
        self.transmission_interval_seconds = transmission_interval_seconds

    def run(self):
        self.mqtt_client.loop_start()
        while True:
            # Pick a random value.
            value = random.gauss(self.value_mean, self.value_stddev)
            # Publish to its MQTT topic.
            self.mqtt_client.publish(self.state_topic, f"{value:.2f}")
            # Sleep.
            time.sleep(self.transmission_interval_seconds)