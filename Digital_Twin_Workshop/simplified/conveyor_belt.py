"""
ConveyorBelt machine for workshop.
"""
from base_machine import BaseMachine
import logging

logger = logging.getLogger(__name__)


class ConveyorBelt(BaseMachine):
    """Conveyor belt machine"""
    
    def __init__(self, machine_name=None):
        super().__init__(machine_name)
        self.forward = False
        self.conveyor_running = False
    
    def process_mqtt(self, attribute_name, value):
        """Process MQTT messages"""
        if attribute_name == "conveyorActForward":
            self.forward = value.lower() == "true"
            logger.info(f"{self.machine_name}: forward = {self.forward}")
        
        elif attribute_name == "isExecuting":
            self.conveyor_running = value.lower() == "true"
            logger.info(f"{self.machine_name}: conveyor_running = {self.conveyor_running}")
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            "forward": self.forward,
            "conveyorRunning": self.conveyor_running
        })
        return data
    
    def __repr__(self):
        return (f"ConveyorBelt({self.machine_name}, forward={self.forward}, "
                f"running={self.conveyor_running})")
