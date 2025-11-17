"""
Complete workshop example - putting it all together.
"""
import logging
from machine_registry import MachineRegistry
from mqtt_receiver import MqttReceiver
from conveyor_belt import ConveyorBelt
from sorting_line import SortingLine
from vacuum_gripper import VacuumGripper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the workshop demo"""
    
    # 1. Create the machine registry
    logger.info("Setting up machine registry...")
    registry = MachineRegistry()
    
    # 2. Create and register machines
    registry.register_machine("ConveyorBelt01", ConveyorBelt("ConveyorBelt01"))
    registry.register_machine("SortingLine01", SortingLine("SortingLine01"))
    registry.register_machine("VacuumGripper02", VacuumGripper("VacuumGripper02"))
    
    logger.info(f"Registered machines: {list(registry.machines.keys())}")
    
    # 3. Set up MQTT receiver
    logger.info("Connecting to MQTT broker...")
    receiver = MqttReceiver(
        broker_url="localhost",  # Change to your MQTT broker address
        topics=["factory/#"],     # Subscribe to all factory topics
        machine_registry=registry,
        port=1883
    )
    
    # 4. Start receiving messages
    receiver.start()
    
    logger.info("Workshop system running! Press Ctrl+C to stop")
    
    # 5. Keep the program running
    try:
        import time
        while True:
            time.sleep(1)
            
            # Optional: Print machine states every 10 seconds
            # Uncomment to see periodic updates
            # if int(time.time()) % 10 == 0:
            #     for machine in registry.get_all_machines():
            #         print(f"  {machine}")
            
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        receiver.stop()
        logger.info("Stopped successfully")


if __name__ == "__main__":
    main()
