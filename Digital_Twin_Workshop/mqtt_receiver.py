"""
MQTT Receiver - Handles incoming MQTT messages and routes them to the machine registry.
"""
import logging
from typing import List
import paho.mqtt.client as mqtt

from machine_registry import MachineRegistry
from mqtt_utils import get_machine_name, get_attribute_name, get_value

logger = logging.getLogger(__name__)


class MqttReceiverConfig:
    """
    Configuration and handler for MQTT message reception.
    Subscribes to MQTT topics and processes incoming messages.
    """
    
    def __init__(
        self,
        broker_url: str,
        client_id: str,
        topics: List[str],
        machine_registry: MachineRegistry,
        username: str = "",
        password: str = "",
        port: int = 1883
    ):
        """
        Initialize MQTT receiver configuration.
        
        Args:
            broker_url: MQTT broker URL/hostname
            client_id: Unique client identifier
            topics: List of topics to subscribe to
            machine_registry: MachineRegistry instance for routing updates
            username: MQTT username (optional)
            password: MQTT password (optional)
            port: MQTT broker port (default: 1883)
        """
        self.broker_url = broker_url
        self.client_id = client_id
        self.topics = topics
        self.machine_registry = machine_registry
        self.username = username
        self.password = password
        self.port = port
        self.client = None
    
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for when the client connects to the broker.
        
        Args:
            client: MQTT client instance
            userdata: User data passed to callbacks
            flags: Response flags from the broker
            rc: Connection result code
        """
        if rc == 0:
            logger.info(f"Connected to MQTT broker at {self.broker_url}")
            # Subscribe to all configured topics
            for topic in self.topics:
                client.subscribe(topic, qos=1)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker, return code: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """
        Callback for when the client disconnects from the broker.
        
        Args:
            client: MQTT client instance
            userdata: User data passed to callbacks
            rc: Disconnection result code
        """
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker, return code: {rc}")
        else:
            logger.info("Disconnected from MQTT broker")
    
    def on_message(self, client, userdata, msg):
        """
        Callback for when a message is received from the broker.
        
        Args:
            client: MQTT client instance
            userdata: User data passed to callbacks
            msg: MQTT message object
        """
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # Parse MQTT message
            machine_name = get_machine_name(topic)
            attribute_name = get_attribute_name(topic)
            value = get_value(payload)
            
            # Log for debugging
            logger.debug(f"Received MQTT message - Topic: {topic}, "
                        f"Machine: {machine_name}, "
                        f"Attribute: {attribute_name}, "
                        f"Value: {value}")
            
            # Route to machine registry
            self.machine_registry.publish_update(machine_name, attribute_name, value)
            
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}", exc_info=True)
    
    def start(self):
        """
        Start the MQTT client and begin receiving messages.
        """
        try:
            # Create MQTT client
            self.client = mqtt.Client(client_id=self.client_id)
            
            # Set up authentication if provided
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            # Set callbacks
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            # Connect to broker
            logger.info(f"Connecting to MQTT broker at {self.broker_url}:{self.port}")
            self.client.connect(self.broker_url, self.port, keepalive=60)
            
            # Start network loop in background thread
            self.client.loop_start()
            
            logger.info("MQTT receiver started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start MQTT receiver: {e}", exc_info=True)
            raise
    
    def stop(self):
        """
        Stop the MQTT client and disconnect from the broker.
        """
        if self.client:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                logger.info("MQTT receiver stopped")
            except Exception as e:
                logger.error(f"Error stopping MQTT receiver: {e}")


# Example usage
if __name__ == "__main__":
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Database setup (example)
    engine = create_engine('sqlite:///machines.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create machine registry
    registry = MachineRegistry(session)
    
    # Initialize with your machine classes
    # registry.init({
    #     "SortingLine01": SortingLine,
    #     "HighBay01": Highbay,
    #     # ... other machines
    # })
    
    # Create MQTT receiver
    receiver = MqttReceiverConfig(
        broker_url=os.getenv("MQTT_BROKER_URL", "localhost"),
        client_id=os.getenv("MQTT_CLIENT_ID", "digital_twin_client"),
        topics=os.getenv("MQTT_TOPICS", "factory/#").split(","),
        machine_registry=registry
    )
    
    try:
        # Start receiving messages
        receiver.start()
        
        # Keep running
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        receiver.stop()
        registry.shutdown()
