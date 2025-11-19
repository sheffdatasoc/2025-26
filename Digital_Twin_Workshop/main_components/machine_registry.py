"""
Simple machine registry for workshop demo.
"""
import json
import logging
from base_machine import MachineState, BaseMachine

logger = logging.getLogger(__name__)


class MachineRegistry:
    """Manages all machines"""
    
    def __init__(self):
        self.machines = {}
    
    def register_machine(self, name, machine):
        """Add a machine to the registry"""
        self.machines[name] = machine
        logger.info(f"Registered machine: {name}")
    
    def publish_update(self, machine_name, attribute_name, value):
        """Update a machine based on MQTT message"""
        
        machine = self.machines.get(machine_name)
        if not machine:
            #logger.error(f"Machine '{machine_name}' with {attribute_name} and {value} not found. Available: {list(self.machines.keys())}")
            return
        
        # Handle state changes
        # if just the execution state is changed, the registry handles it directly
        # otherwise the machine DTOs handle the processing
        if attribute_name == "isExecuting":
            if value == "true":
                if machine.state != MachineState.RUNNING:
                    logger.info(f"{machine_name} is now RUNNING")
                    machine.state = MachineState.RUNNING
            else:
                if machine.state != MachineState.IDLE:
                    logger.info(f"{machine_name} is now IDLE")
                    machine.state = MachineState.IDLE
            # Let the machine handle other attributes
        machine.process_mqtt(attribute_name, value)
    
    def get_machine(self, name):
        """Get a machine object by name"""
        return self.machines.get(name)
    
    def get_all_machines(self):
        """Get all machines as a list"""
        return list(self.machines.values())
    
    def get_machine_json(self, name):
        """Get machine as JSON string"""
        machine = self.machines.get(name)
        if not machine:
            return "{}"
        return json.dumps(machine.to_dict())
