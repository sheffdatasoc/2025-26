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
        """Called when a message is received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # Parse the message
            machine_name = get_machine_name(topic)
            attribute_name = get_attribute_name(topic)
            value = get_value(payload)
            
            logger.debug(f"Message: {machine_name}.{attribute_name} = {value}")
            
            # Update the machine
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


# Example usage
if __name__ == "__main__":
    from machine_registry import MachineRegistry
    from base_machine import BaseMachine
    
    logging.basicConfig(level=logging.INFO)
    
    # Example machine class
    class WorkshopMachine(BaseMachine):
        def process_mqtt(self, attribute_name, value):
            logger.info(f"  -> {self.machine_name}: {attribute_name} = {value}")
    
    # Set up registry
    registry = MachineRegistry()
    registry.register_machine("Machine01", WorkshopMachine("Machine01"))
    registry.register_machine("Machine02", WorkshopMachine("Machine02"))
    
    # Set up MQTT receiver
    receiver = MqttReceiver(
        broker_url="localhost",
        topics=["factory/#"],
        machine_registry=registry
    )
    
    # Start receiving
    receiver.start()
    
    print("Listening for MQTT messages... Press Ctrl+C to stop")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        receiver.stop()
        print("\nStopped")
