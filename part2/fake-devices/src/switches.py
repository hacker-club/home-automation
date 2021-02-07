import json
import paho.mqtt.client as mqtt
import random
import time

from typing import Dict

from mqtt import FakeMQTTDevice


class FakeSwitch(FakeMQTTDevice):
    """Defines a fake switch.

    Objects of this class have two responsibilities:
    1. Subscribe to `command_topic` and listens to "ON" or "OFF" messages
    2. Publish their state ("ON" or "OFF") to `state_topic`

    Moreover, objects of this class make themselves "discoverable" by other devices by
    publishing their configuration to the MQTT topic homeassistant/switch/fake-switches/<id>/config.
    This allows for home-assistant to automatically find them (https://www.home-assistant.io/docs/mqtt/discovery/).


    The `icon` argument defines how this device is represented in home-assistant. Possible values are in
    https://pictogrammers.github.io/@mdi/font/5.3.45/.
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

        # Publish self config for auto discovery.
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
                        "manufacturer": "hackerclub.io",
                    },
                }
            ),
            qos=2,
            retain=True,
        )