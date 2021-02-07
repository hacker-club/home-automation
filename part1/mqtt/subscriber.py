import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "hacker-club/example/random"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with status: {rc}")
    client.subscribe(TOPIC)


def on_message(client, user_data, message):
    print(f"Got message: {float(message.payload)}")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()