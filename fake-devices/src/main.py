from sensors import FakeSensor

all_sensors = [
    FakeSensor(
        value_topic="fake-sensors/bedroom/temperature",
        value_mean=20.2,
        value_stddev=5.0,
        value_unity="°C",
        transmission_interval_seconds=1.0,
    ),
    FakeSensor(
        value_topic="fake-sensors/kitchen/humidity",
        value_mean=62.4,
        value_stddev=20.8,
        value_unity="%",
        transmission_interval_seconds=2.5,
    ),
    FakeSensor(
        value_topic="fake-sensors/living-room/co2",
        value_mean=720.7,
        value_stddev=200,
        value_unity="ppm",
        transmission_interval_seconds=5.0,
    ),
]

threads = [s.run() for s in all_sensors]

# Wait until all threads are finished. Hint: they never are.
for thread in threads:
    thread.join()