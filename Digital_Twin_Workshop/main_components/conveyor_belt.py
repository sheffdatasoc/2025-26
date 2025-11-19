"""
ConveyorBelt machine for workshop.
"""
from base_machine import BaseMachine
import logging

logger = logging.getLogger(__name__)


class ConveyorBelt(BaseMachine):
    """Conveyor belt machine"""
    # todos: implement the following:
    # - init method
    # - process_mqtt
    # - repr and todict (change attribute names)
    
    def __init__(self, machine_name=None):
        super().__init__(machine_name)
        self.attr1 = 0
        pass
    
    def process_mqtt(self, attribute_name, value):
        """Process MQTT messages"""
        pass

    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            "attr1": self.attr1,
        })
        return data
    
    def __repr__(self):
        return (f"ConveyorBelt({self.machine_name}, attr1={self.attr1},)")
