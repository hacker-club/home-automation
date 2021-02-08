import json
import paho.mqtt.client as mqtt
import random
import time
import threading

from dataclasses import dataclass
from typing import Dict

from mqtt import FakeMQTTDevice


class FakeBinarySensor(FakeMQTTDevice):
    """Defines a fake binary sensor.

    A binary sensor is one that has only two possible states: "ON" or "OFF".
    Some examples are:
    - Motion detector sensors (either detection or no detection)
    - Lock sensors (either locked or unlocked)
    - Window sensors (either open or close)

    To add some excitement to this simulation, at every `transmission_interval_seconds`,
    this sensor has a `probability_of_changing_state`. This means that there is a configurable
    chance that the state will flip from "ON" to "OFF" once in a while.
    """

    def __init__(
        self,
        id: str,
        name: str,
        state_topic: str,
        probability_of_changing_state: float,
        transmission_interval_seconds: float,
        initial_state: bool,
    ):
        super(FakeBinarySensor, self).__init__()
        self.id = id
        self.name = name
        self.state_topic = state_topic
        self.probability_of_changing_state = probability_of_changing_state
        self.transmission_interval_seconds = transmission_interval_seconds
        self.state = initial_state

    def run(self):
        self.mqtt_client.loop_start()
        while True:
            # Maybe flip the current state with some probability.
            self.state = (
                not self.state
                if random.random() < self.probability_of_changing_state
                else self.state
            )
            # Publish "ON" or "OFF" to its MQTT topic based on its current state.
            self.mqtt_client.publish(self.state_topic, "ON" if self.state else "OFF")
            # Sleep.
            time.sleep(self.transmission_interval_seconds)

    def on_connect(self):
        print(f"FakeSensor {self.id} connected.")