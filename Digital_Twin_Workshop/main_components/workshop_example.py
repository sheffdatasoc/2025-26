
import logging
from machine_registry import MachineRegistry
from mqtt_receiver import MqttReceiver
from conveyor_belt import ConveyorBelt
from sorting_line import SortingLine
from vacuum_gripper import VacuumGripper
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


# Create rich console for pretty output
console = Console()


def create_machine_panel(machine):
    """Create a pretty panel for a machine's status"""
    # Create a table for the machine details
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column(style="cyan", width=15)
    table.add_column(style="yellow")
    
    # Add machine type and name
    machine_type = machine.__class__.__name__
    
    # Add common attributes
    table.add_row("Type", machine_type)
    table.add_row("State", str(machine.state.value))
    
    # Add machine-specific attributes
    if hasattr(machine, 'forward') and hasattr(machine, 'conveyor_running'):
        # ConveyorBelt
        table.add_row("Forward", "✓" if machine.forward else "✗")
        table.add_row("Running", "✓" if machine.conveyor_running else "✗")
        color = "green" if machine.conveyor_running else "blue"
    
    elif hasattr(machine, 'color_present'):
        # SortingLine
        table.add_row("Color", str(machine.color_present) if machine.color_present else "None")
        table.add_row("Running", "✓" if machine.conveyor_running else "✗")
        if machine.ejected_to_branch:
            table.add_row("Last Ejected", machine.ejected_to_branch)
        color = "magenta" if machine.color_present else "blue"
    
    elif hasattr(machine, 'rotation'):
        # VacuumGripper
        table.add_row("Rotation", f"{machine.rotation:.1f}°")
        table.add_row("Height", f"{machine.height}mm")
        table.add_row("Forward", f"{machine.forward}mm")
        color = "cyan"
    else:
        color = "white"
    
    # Create panel with the table
    return Panel(
        table,
        title=f"[bold]{machine.machine_name}[/bold]",
        border_style=color,
        padding=(1, 2)
    )



def main():
    
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
        broker_url="localhost",  
        topics=["PLC/Island 1/#"],     # Subscribe to all factory topics
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
            
            if int(time.time()) % 5 == 0:
                console.clear()
                console.print("\n[bold cyan]🏭 Factory Digital Twin Status[/bold cyan]\n")
                
                panels = [create_machine_panel(machine) for machine in registry.get_all_machines()]
                
                console.print(Columns(panels, equal=True, expand=True))
                
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        receiver.stop()
        logger.info("Stopped successfully")


if __name__ == "__main__":
    main()
