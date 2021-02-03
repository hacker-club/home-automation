import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "hacker-club/example/random"
SLEEP_FOR_SECS = 5


def on_connect(client, userdata, flags, rc):
    print(f"Connected with status: {rc}")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER_HOST, BROKER_PORT, 5)
    client.loop_start()
    print("ok!")
    while True:
        value = random.uniform(0, 1)
        client.publish(TOPIC, value)
        time.sleep(SLEEP_FOR_SECS)


if __name__ == "__main__":
    main()