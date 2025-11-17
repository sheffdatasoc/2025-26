"""
Machine Registry - Central registry for managing digital twin machines.
"""
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Type
from threading import Lock

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from apscheduler.schedulers.background import BackgroundScheduler

from base_machine import BaseMachine, MachineState

logger = logging.getLogger(__name__)


class MachineRegistry:
    """
    Central registry for managing all machines in the digital twin system.
    Handles machine initialization, state updates, and persistence.
    """
    
    def __init__(self, session: Session):
        """
        Initialize the machine registry.
        
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.machines: Dict[str, BaseMachine] = {}
        self._lock = Lock()
        self._scheduler = None
        
    def publish_update(self, machine_name: str, attribute_name: str, value: str):
        """
        Process an update for a machine attribute from MQTT.
        
        Args:
            machine_name: Name of the machine to update
            attribute_name: Name of the attribute to update
            value: New value for the attribute
        """
        # Ignore specific machines
        if machine_name in ["PunchingMachine01", "received"]:
            return
        
        with self._lock:
            machine = self.machines.get(machine_name)
            
            if machine is None:
                logger.error(f"Machine not found: '{machine_name}'. "
                           f"Available machines: {list(self.machines.keys())}")
                return
            
            # Handle state changes
            if attribute_name == "isExecuting":
                if value == "true":
                    if machine.state == MachineState.RUNNING:
                        return
                    logger.info(f"Machine {machine_name} is now running.")
                    machine.state = MachineState.RUNNING
                else:
                    if machine.state == MachineState.IDLE:
                        return
                    logger.info(f"Machine {machine_name} is now idle.")
                    machine.state = MachineState.IDLE
            else:
                machine.process_mqtt(attribute_name, value)
            
            machine.is_dirty = True
    
    def init(self, machine_classes: Dict[str, Type[BaseMachine]]):
        """
        Initialize the machine registry with machine instances.
        
        Args:
            machine_classes: Dictionary mapping machine names to their classes
                Example: {"SortingLine01": SortingLine, "HighBay01": Highbay}
        """
        logger.info("MachineRegistry initializing...")
        
        for machine_name, machine_class in machine_classes.items():
            machine = self._load_last_or_create(machine_class, machine_name)
            self.machines[machine_name] = machine
        
        logger.info(f"Machine registry initialized with machines: {list(self.machines.keys())}")
        
        # Start the scheduler for periodic persistence
        self._start_scheduler()
    
    def _load_last(self, machine_class: Type[BaseMachine], machine_name: str) -> Optional[BaseMachine]:
        """
        Load the most recent instance of a machine from the database.
        
        Args:
            machine_class: Class of the machine to load
            machine_name: Name of the machine
            
        Returns:
            Most recent machine instance or None if not found
        """
        try:
            return self.session.query(machine_class)\
                .filter(machine_class.machine_name == machine_name)\
                .order_by(machine_class.id.desc())\
                .limit(1)\
                .one()
        except NoResultException:
            return None
    
    def _load_last_or_create(self, machine_class: Type[BaseMachine], machine_name: str) -> BaseMachine:
        """
        Load the most recent machine instance or create a new one.
        
        Args:
            machine_class: Class of the machine
            machine_name: Name of the machine
            
        Returns:
            Machine instance (loaded or newly created)
        """
        machine = self._load_last(machine_class, machine_name)
        
        if machine is None:
            logger.info(f"Creating new instance of {machine_name}")
            machine = machine_class()
            machine.machine_name = machine_name
            machine.is_dirty = True
        else:
            logger.info(f"Loaded existing {machine_name}: {machine}")
            if machine.machine_name is None:
                machine.machine_name = machine_name
                machine.is_dirty = True
        
        return machine
    
    def tick(self):
        """
        Periodic task to persist dirty machines to the database.
        Runs every 300ms as scheduled.
        """
        with self._lock:
            for machine in self.machines.values():
                if machine.is_dirty:
                    try:
                        # Detach from session and create new entry
                        self.session.expunge(machine)
                        machine.id = None
                        self.session.add(machine)
                        self.session.commit()
                        machine.is_dirty = False
                    except Exception as e:
                        logger.error(f"Error persisting machine {machine.machine_name}: {e}")
                        self.session.rollback()
    
    def _start_scheduler(self):
        """Start the background scheduler for periodic tasks"""
        self._scheduler = BackgroundScheduler()
        # Run tick every 300ms (0.3 seconds)
        self._scheduler.add_job(self.tick, 'interval', seconds=0.3)
        self._scheduler.start()
        logger.info("Scheduler started for machine persistence")
    
    def shutdown(self):
        """Shutdown the registry and stop the scheduler"""
        if self._scheduler:
            self._scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def get_all_machines(self) -> List[BaseMachine]:
        """
        Get a list of all registered machines.
        
        Returns:
            List of all machine instances
        """
        with self._lock:
            return list(self.machines.values())
    
    def get_machine_json(self, machine_name: str) -> str:
        """
        Get JSON representation of a machine.
        
        Args:
            machine_name: Name of the machine
            
        Returns:
            JSON string of the machine or empty object if not found
        """
        with self._lock:
            machine = self.machines.get(machine_name)
            if machine is None:
                return "{}"
            
            try:
                # Convert machine to dict (you may need to customize this)
                machine_dict = {
                    "id": machine.id,
                    "machineName": machine.machine_name,
                    "state": machine.state.value,
                    "timestamp": machine.timestamp.isoformat()
                }
                return json.dumps(machine_dict)
            except Exception as e:
                logger.error(f"Error serializing machine {machine_name}: {e}")
                return "{}"
    
    def get_machines(self) -> Dict[str, BaseMachine]:
        """
        Get a copy of the machines dictionary.
        
        Returns:
            Dictionary mapping machine names to machine instances
        """
        with self._lock:
            return self.machines.copy()
    
    def get_machine_by_name(self, machine_name: str) -> Optional[BaseMachine]:
        """
        Get a machine by its name.
        
        Args:
            machine_name: Name of the machine
            
        Returns:
            Machine instance or None if not found
        """
        with self._lock:
            return self.machines.get(machine_name)
