"""
SortingLine machine for workshop.
"""
from base_machine import BaseMachine
import logging
import re

logger = logging.getLogger(__name__)


class SortingLine(BaseMachine):
    """Sorting line machine that sorts items by color"""
    
    def __init__(self, machine_name=None):
        super().__init__(machine_name)
        self.color_present = None
        self.conveyor_running = False
        self.ejected_to_branch = None
    
    def process_mqtt(self, attribute_name, value):
        """Process MQTT messages"""
        
        # Check if it's an ejector attribute
        if re.match(r"^sortingLineAct(Red|White|Blue)Ejector$", attribute_name):
            attribute_name = "ejectedToBranch"
        
        if attribute_name == "ejectedToBranch":
            ejector_active = value.lower() == "true"
            if ejector_active and self.color_present:
                # Map colors to branches
                color_to_branch = {
                    "BLUE": "LEFT",
                    "RED": "MIDDLE",
                    "WHITE": "RIGHT"
                }
                self.ejected_to_branch = color_to_branch.get(self.color_present)
                #logger.info(f"{self.machine_name}: ejected {self.color_present} to {self.ejected_to_branch}")
        
        elif attribute_name == "command":
            # Extract color from command string like "<Color.RED:"
            match = re.search(r"<Color\.(RED|BLUE|WHITE):", value)
            if match:
                self.color_present = match.group(1)
                #logger.info(f"{self.machine_name}: color_present = {self.color_present}")
        
        elif attribute_name == "colorPresent":
            self.color_present = value.upper()
            #logger.info(f"{self.machine_name}: color_present = {self.color_present}")
        
        elif attribute_name == "sortingLineActMotorConveyor":
            self.conveyor_running = value.lower() == "true"
            #logger.info(f"{self.machine_name}: conveyor_running = {self.conveyor_running}")
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            "colorPresent": self.color_present,
            "conveyorRunning": self.conveyor_running,
            "ejectedToBranch": self.ejected_to_branch
        })
        return data
    
    def __repr__(self):
        return (f"SortingLine({self.machine_name}, color={self.color_present}, "
                f"branch={self.ejected_to_branch})")
