"""
Simple MQTT receiver for workshop demo.
"""
import logging
import paho.mqtt.client as mqtt
from mqtt_utils import get_machine_name, get_attribute_name, get_value

logger = logging.getLogger(__name__)


class MqttReceiver:
    """Simple MQTT message receiver"""
    
    def __init__(self, broker_url, topics, machine_registry, port=1883):
        """
        Args:
            broker_url: MQTT broker address (e.g., "localhost")
            topics: List of topics to subscribe (e.g., ["factory/#"])
            machine_registry: MachineRegistry instance
            port: MQTT port (default: 1883)
        """
        self.broker_url = broker_url
        self.port = port
        self.topics = topics
        self.registry = machine_registry
        self.client = mqtt.Client()
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, rc):
        """Called when connected to broker"""
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.broker_url}")
            for topic in self.topics:
                client.subscribe(topic)
                logger.info(f"Subscribed to: {topic}")
        else:
            logger.error(f"Connection failed with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Called when a message is received from the broker"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # Parse the message
            machine_name = get_machine_name(topic)
            attribute_name = get_attribute_name(topic)
            value = get_value(payload)
            
            logger.debug(f"Message: {machine_name}.{attribute_name} = {value}")
            
            # Update the machine
            # the registry handles passing the attribute and value to the correct machine
            self.registry.publish_update(machine_name, attribute_name, value)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def start(self):
        """Connect and start listening"""
        logger.info(f"Connecting to {self.broker_url}:{self.port}...")
        self.client.connect(self.broker_url, self.port)
        self.client.loop_start()
        logger.info("MQTT receiver started")
    
    def stop(self):
        """Stop and disconnect"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT receiver stopped")
