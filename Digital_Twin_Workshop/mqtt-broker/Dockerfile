# Dockerfile
FROM eclipse-mosquitto:2.0

# Copy your custom config into the container
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf

# Expose MQTT and WebSocket ports
EXPOSE 1883
EXPOSE 9001

# Start Mosquitto with our config
CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
