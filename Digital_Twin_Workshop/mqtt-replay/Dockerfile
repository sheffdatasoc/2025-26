FROM python:3.10-slim

WORKDIR /app

# Copy your CSV in
COPY simple_process.csv .

# Install mqtt-recorder
RUN pip install --no-cache-dir mqtt-recorder

# Allow overriding via ENV
ENV MQTT_HOST=mqtt-broker
ENV MQTT_PORT=1883
ENV MODE=replay
ENV FILE=simple_process.csv
ENV LOOP=999999999

CMD ["sh", "-c", "mqtt-recorder --host $MQTT_HOST --port $MQTT_PORT --mode $MODE --file $FILE --loop $LOOP"]
