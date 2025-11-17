"""
VacuumGripper machine for workshop.
"""
from base_machine import BaseMachine
import logging

logger = logging.getLogger(__name__)


class VacuumGripper(BaseMachine):
    """Vacuum gripper machine with rotation, height, and forward movement"""
    
    def __init__(self, machine_name=None):
        super().__init__(machine_name)
        self.rotation = 0.0
        self.height = 0
        self.forward = 0
    
    def delta_rotation(self, rotation_count):
        """Calculate rotation angle from encoder count"""
        set_angle = (rotation_count / 61.2) * 360
        self.rotation = set_angle % 360
    
    def delta_height(self, height_count):
        """Calculate height in mm from encoder count"""
        # Distance (mm) = PulseCount × 5/75
        self.height = round(height_count * 5.0 / 75.0)
    
    def delta_forward(self, forward_count):
        """Calculate forward distance in mm from encoder count"""
        # Distance (mm) = PulseCount × 5/75
        self.forward = round(forward_count * 5.0 / 75.0)
    
    def process_mqtt(self, attribute_name, value):
        """Process MQTT messages"""
        try:
            if attribute_name == "vacuumSensRotEncoderCounter":
                rotation_count = int(value)
                self.delta_rotation(rotation_count)
                logger.info(f"{self.machine_name}: rotation = {self.rotation:.1f}°")
            
            elif attribute_name == "vacuumSensVerticalEncoderCounter":
                height_count = int(value)
                self.delta_height(height_count)
                logger.info(f"{self.machine_name}: height = {self.height}mm")
            
            elif attribute_name == "vacuumSensArmEncoderCounter":
                forward_count = int(value)
                self.delta_forward(forward_count)
                logger.info(f"{self.machine_name}: forward = {self.forward}mm")
        
        except ValueError:
            logger.warning(f"Invalid number for {attribute_name}: {value}")
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            "rotation": self.rotation,
            "height": self.height,
            "forward": self.forward
        })
        return data
    
    def __repr__(self):
        return (f"VacuumGripper({self.machine_name}, rot={self.rotation:.1f}°, "
                f"h={self.height}mm, f={self.forward}mm)")
