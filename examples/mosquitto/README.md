# Example Mosquitto configuration
To run the `eclipse-mosquitto` Docker image with this configuration:

```bash
$ docker run -p 1883:1883 -v $(pwd)/conf:/mosquitto/config -v $(pwd)/data:/var/lib/mosquitto eclipse-mosquitto
```

# Create users
The `password_file` in this directory comes pre-populated with the `mqttuser:mqttpassword` credentials. To add/remove new users, use the [`mosquitto_passwd`](https://mosquitto.org/man/mosquitto_passwd-1.html) command:
```bash
$ docker exec -it <container_id> mosquitto_passwd /mosquitto/config/password_file mqttuser
```