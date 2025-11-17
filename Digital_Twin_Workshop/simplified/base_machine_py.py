"""
Simple base class for machines in the digital twin system.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class MachineState(Enum):
    """Machine states"""
    IDLE = "IDLE"
    RUNNING = "RUNNING"


class BaseMachine(ABC):
    """Base class for all machines"""
    
    def __init__(self, machine_name=None):
        self.machine_name = machine_name
        self.state = MachineState.IDLE
        self.timestamp = datetime.now()
    
    @abstractmethod
    def process_mqtt(self, attribute_name, value):
        """Process MQTT updates - implement in subclasses"""
        pass
    
    def to_dict(self):
        """Convert to dictionary for easy JSON serialization"""
        return {
            "machineName": self.machine_name,
            "state": self.state.value,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.machine_name}, {self.state.value})"
