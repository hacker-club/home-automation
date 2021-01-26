# docker-compose
```
# Start all containers
$ docker-compose up

# Remove all containers
$ docker-compose rm
```

# mosquitto
The following volumes are mounted from `host` => `container` (check in `docker-compose.yml`):
- `conf/mosquitto` => `/mosquitto/config`
- `data/mosquitto` => `/var/lib/mosquitto`
## Create username/password
The following command will create a username password credentials. In this repository, I assume the username is `mqttuser` and the password `mqttpassword` for demonstration purposes.
```
docker exec -it homeautodockercompose_mosquitto_1 mosquitto_passwd -c /mosquitto/config/password_file mqttuser
```

# home-assistant
You can access the home-assistant UI at [localhost:8123](http://localhost:8123).
## Credentials
You will be asked to set up your credentials upon first access. In this demonstration, we will use username `home-assistant` and password `home-assistant`.
## mqtt
You can install MQTT as an addon from within home-assistant, but in this demonstratino I set up a separate mqtt broker in the `docker-compose.yml` file (`mosquitto`). This option is described in home-assistant docs under [mqtt - run your own](https://www.home-assistant.io/docs/mqtt/broker#run-your-own).