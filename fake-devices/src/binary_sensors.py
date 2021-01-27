import json
import paho.mqtt.client as mqtt
import random
import time
import threading

from dataclasses import dataclass
from typing import Dict

from mqtt import FakeMQTTDevice


class FakeBinarySensor(FakeMQTTDevice):
    """Defines a fake sensor that periodically sends data to a MQTT topic.
    Names for available classes are in https://www.home-assistant.io/integrations/binary_sensor/#device-class."""

    def __init__(
        self,
        id: str,
        name: str,
        device_class: str,
        state_topic: str,
        probability_of_changing_state: float,
        transmission_interval_seconds: float,
        initial_state: bool,
    ):
        super(FakeBinarySensor, self).__init__()
        self.id = id
        self.name = name
        self.device_class = device_class
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
        # MQTT auto-discovery. For available values for binary sensors, see
        # https://www.home-assistant.io/integrations/binary_sensor.mqtt/
        self.mqtt_client.publish(
            f"homeassistant/binary_sensor/fake-sensors/{self.id}/config",
            payload=json.dumps(
                {
                    "unique_id": self.id,
                    "name": self.name,
                    "device_class": self.device_class,
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
