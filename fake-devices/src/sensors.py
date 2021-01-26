import paho.mqtt.client as mqtt
import random
import time
import threading

from dataclasses import dataclass
from typing import Dict

from config import MQTT_USER, MQTT_PASS, MQTT_HOST, MQTT_PORT


@dataclass
class FakeSensor:
    value_topic: str
    value_mean: float
    value_stddev: float
    value_unity: str
    transmission_interval_seconds: float
    mqtt_client: mqtt.Client = None

    def __post_init__(self):
        self.mqtt_client = mqtt.Client(userdata=self)
        self.mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.connect(MQTT_HOST, MQTT_PORT)

    def run(self):
        thread = threading.Thread(target=run_on_thread, args=(self,))
        thread.start()
        return thread


def run_on_thread(sensor: FakeSensor):
    sensor.mqtt_client.loop_start()
    while True:
        value = random.gauss(sensor.value_mean, sensor.value_stddev)
        sensor.mqtt_client.publish(sensor.value_topic, value)
        # Sleep for some time.
        time.sleep(sensor.transmission_interval_seconds + (random.random() - 0.5))


def on_connect(client: mqtt.Client, userdata: FakeSensor, flags: Dict, rc: int):
    print(f"Connected with result code {rc}, {userdata.value_topic}")
    # TODO: publish auto discovery info.
