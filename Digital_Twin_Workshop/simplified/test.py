from rich.live import Live
from rich.table import Table
import time, random

def make_table(values):
    table = Table(title="DTO State")
    table.add_column("Field")
    table.add_column("Value")
    table.add_column("Bar")

    for name, val in values.items():
        bar = "█" * val
        table.add_row(name, str(val), bar)
    return table

values = {"temperature": 3, "pressure": 5, "humidity": 2}

with Live(make_table(values), refresh_per_second=5) as live:
    for _ in range(30):
        values = {k: random.randint(0, 20) for k in values}
        live.update(make_table(values))
        time.sleep(0.2)
