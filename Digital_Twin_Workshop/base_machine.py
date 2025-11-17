"""
Base class for all machines in the digital twin system.
Contains common attributes and methods shared by all machine types.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MachineState(Enum):
    """Enumeration of possible machine states"""
    IDLE = "IDLE"
    RUNNING = "RUNNING"


class BaseMachine(Base, ABC):
    """
    Base class for all machines in the digital twin system.
    Uses SQLAlchemy for ORM functionality.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_name = Column(String, nullable=False)
    state = Column(SQLEnum(MachineState), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    def __init__(self, machine_name=None, state=MachineState.IDLE, timestamp=None):
        """
        Initialize a new machine instance.
        
        Args:
            machine_name: Name identifier for the machine
            state: Initial state (defaults to IDLE)
            timestamp: Creation timestamp (defaults to current time)
        """
        self.machine_name = machine_name
        self.state = state
        self.timestamp = timestamp or datetime.now()
        self._is_dirty = False
    
    @property
    def is_dirty(self):
        """Check if machine state has been modified"""
        return self._is_dirty
    
    @is_dirty.setter
    def is_dirty(self, value):
        """Set the dirty flag"""
        self._is_dirty = value
    
    def update_timestamp(self):
        """Update the timestamp to current time"""
        self.timestamp = datetime.now()
    
    @abstractmethod
    def process_mqtt(self, attribute_name, string_value):
        """
        Process incoming MQTT messages to update machine attributes.
        Each subclass must implement this method to handle its specific attributes.
        
        Args:
            attribute_name: Name of the attribute to update
            string_value: String representation of the new value
        """
        pass
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.machine_name}, state={self.state.value})>"
