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