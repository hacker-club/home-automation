# Example MQTT clients
These are small Python 3 MQTT clients based on the paho-mqtt library.

These example uses the public [Eclipse MQTT broker](https://test.mosquitto.org/).

## Install dependencies
It's easier to use a virtual environment and install the dependencies from `requirements.txt`:
```bash
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Publisher
```bash
$ python publisher.py
```

## Subscriber
```bash
$ python subscriber.py
```