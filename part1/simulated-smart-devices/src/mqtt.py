import paho.mqtt.client as mqtt

from typing import Dict

from config import MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT


class FakeMQTTDevice:
    def __init__(self):
        self.mqtt_client = mqtt.Client(userdata=self)
        self.mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT)

    def run(self):
        raise NotImplementedError("Implement me!")

    def on_connect(self):
        pass

    def on_message(self, message: str):
        pass


def on_connect(client: mqtt.Client, fake_device: FakeMQTTDevice, flags: Dict, rc: int):
    fake_device.on_connect()


def on_message(
    client: mqtt.Client, fake_device: FakeMQTTDevice, message: mqtt.MQTTMessage
):
    fake_device.on_message(message.payload.decode('utf-8'))