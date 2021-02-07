# Simulated Smart Devices
This directory holds the initial implementation of simulated smart devices.

As a test, we use [Eclipse's public](https://test.mosquitto.org/). It runs on `test.mosquitto.org` on port `1883`. This config is editable in `src/config.py`.

To run it, first set up a `virtualenv` with Python 3:
```bash
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python src/main.py
FakeSensor office_motion_detector connected.
FakeSensor garage_door connected.
FakeSensor kitchen_smoke_detector connected.
Switch office_light connected.
Switch alarm_light connected.
```