import json
import paho.mqtt.client as mqtt
import random
import time
import threading

from dataclasses import dataclass
from typing import Dict

from mqtt import FakeMQTTDevice


class FakeSensor(FakeMQTTDevice):
    """Defines a fake sensor that periodically sends data to a MQTT topic.
    Names for available icons are in https://pictogrammers.github.io/@mdi/font/5.3.45/"""

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

    def on_connect(self):
        print(f"FakeSensor {self.id} connected.")
        self.mqtt_client.publish(
            f"homeassistant/sensor/fake-sensors/{self.id}/config",
            payload=json.dumps(
                {
                    "unique_id": self.id,
                    "name": self.name,
                    "icon": f"mdi:{self.icon}",
                    "unit_of_measurement": self.unit,
                    "state_topic": self.state_topic,
                    "platform": "mqtt",
                    "device": {
                        "identifiers": self.id,
                        "name": self.name,
                        "model": "fake-sensor-v1",
                        "manufacturer": "hacker-club.io",
                    },
                },
            ),
            qos=2,
            retain=True,
        )
