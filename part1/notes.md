# Erasing all retained mqtt messages
```
$ docker-compose exec mosquitto mosquitto_sub -t '#' -u mqttuser -P mqttpassword --remove-retained --retained-only
```