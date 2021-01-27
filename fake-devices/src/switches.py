import json
import paho.mqtt.client as mqtt
import random
import time

from typing import Dict

from mqtt import FakeMQTTDevice


class FakeSwitch(FakeMQTTDevice):
    """Defines a fake switch.

    command_topic is the MQTT topic to which this switch subscribes to and listens to "ON" and "OFF" commands.
    state_topic is the MQTT topic to which this switch publishes its state: "ON" or "OFF". This is the source of truth for this device's state.

    Names for available icons are in https://pictogrammers.github.io/@mdi/font/5.3.45/
    """

    def __init__(
        self, id: str, name: str, icon: str, state_topic: str, command_topic: str
    ):
        super(FakeSwitch, self).__init__()
        self.id = id
        self.name = name
        self.icon = icon
        self.state_topic = state_topic
        self.command_topic = command_topic

    def run(self):
        self.mqtt_client.loop_forever()

    def on_message(self, message: str):
        print(f'Switch {self.id} received message: {message} -> {self.state_topic}')
        if message == "ON":
            self.mqtt_client.publish(self.state_topic, "ON")
        else:
            self.mqtt_client.publish(self.state_topic, "OFF")

    def on_connect(self):
        print(f"Switch {self.id} connected.")

        # Subscribe to commands.
        self.mqtt_client.subscribe(self.command_topic, qos=2)

        # Publish an auto-discovery message so home-assistant automatically learns about
        # this switch. How cool is that?
        # Docs: https://www.home-assistant.io/docs/mqtt/discovery/
        self.mqtt_client.publish(
            f"homeassistant/switch/fake-switches/{self.id}/config",
            json.dumps(
                {
                    "name": self.name,
                    "icon": f"mdi:{self.icon}",
                    "unique_id": self.id,
                    "state_topic": self.state_topic,
                    "command_topic": self.command_topic,
                    "platform": "mqtt",
                    "device": {
                        "identifiers": self.id,
                        "name": self.name,
                        "model": "fake_switch-v1",
                        "manufacturer": "hacker-club.io",
                    },
                }
            ),
            qos=2,
            retain=True,
        )