import threading

from mqtt import FakeMQTTDevice

from binary_sensors import FakeBinarySensor
from sensors import FakeSensor
from switches import FakeSwitch


def run_on_thread(fake_device: FakeMQTTDevice):
    thread = threading.Thread(target=fake_device.run)
    thread.start()
    return thread


def main():
    all_devices = [
        FakeBinarySensor(
            id="office_motion_detector",
            name="Office motion detector",
            device_class="motion",
            state_topic="fake-sensors/office/motion",
            probability_of_changing_state=0.1,
            transmission_interval_seconds=1,
            initial_state=True,
        ),
        FakeBinarySensor(
            id="garage_door",
            name="Garage door",
            device_class="garage_door",
            state_topic="fake-sensors/garage/door",
            probability_of_changing_state=0.1,
            transmission_interval_seconds=5,
            initial_state=False,
        ),
        FakeBinarySensor(
            id="kitchen_smoke_detector",
            name="Kitchen smoke detector",
            device_class="smoke",
            state_topic="fake-sensors/kitchen/smoke",
            probability_of_changing_state=0.05,
            transmission_interval_seconds=2,
            initial_state=False,
        ),
        FakeSensor(
            id="bedroom_temperature",
            name="Bedroom Temperature",
            icon="thermometer",
            state_topic="fake-sensors/bedroom/temperature",
            value_mean=20.2,
            value_stddev=2.0,
            unit="°C",
            transmission_interval_seconds=1.0,
        ),
        FakeSensor(
            id="kitchen_humidity",
            name="Kitchen Humidity",
            icon="water-percent",
            state_topic="fake-sensors/kitchen/humidity",
            value_mean=62.4,
            value_stddev=2.8,
            unit="%",
            transmission_interval_seconds=2.5,
        ),
        FakeSensor(
            id="living_room_co2",
            name="Living Room CO2",
            icon="molecule-co2",
            state_topic="fake-sensors/living-room/co2",
            value_mean=720.7,
            value_stddev=5,
            unit="ppm",
            transmission_interval_seconds=5.0,
        ),
        FakeSensor(
            id="living_room_co2_battery_level",
            name="Living Room CO2 battery level",
            icon="battery",
            state_topic="fake-sensors/living-room/co2-battery",
            value_mean=85,
            value_stddev=2.5,
            unit="%",
            transmission_interval_seconds=10.0,
        ),
        FakeSwitch(
            id="office_light",
            name="Office light",
            icon="ceiling-light",
            state_topic="fake-switches/office/light/state",
            command_topic="fake-switches/office/light/command",
        ),
        FakeSwitch(
            id="alarm_light",
            name="Alarm light",
            icon="alarm-light",
            state_topic="fake-switches/office/alarm-light/state",
            command_topic="fake-switches/office/alarm-light/command",
        ),
    ]

    threads = [run_on_thread(device) for device in all_devices]
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()