from rich.table import Table
from rich.console import Console
from time import sleep

from src.schemas import ShipsManager


class ShowShipCargoStatus:
    name = "Show ship cargo status"
    description = (
        "Gathers all the ships available to us and show the cargo contents for each one"
    )

    def sleep(self):
        pass

    def process(self):
        ships = ShipsManager.all()
        console = Console()
        for ship in ships.ships:
            # Info table
            cargo_info_table = Table(title="Capacity")
            cargo_info_table.add_column("capacity")
            cargo_info_table.add_column("units")
            cargo_info_table.add_row(
                str(ship.cargo["capacity"]), str(ship.cargo["units"])
            )
            # Contents table
            contents_table = Table(title="Contents")
            contents_table.add_column("symbol")
            contents_table.add_column("units")
            cargo = ship.cargo_status()
            for row in cargo.inventory:
                contents_table.add_row(row["symbol"], row["units"])
            console.rule(f"[bold red]Cargo - {ship.symbol}")
            console.print(cargo_info_table, justify="left", end="")
            console.print(contents_table, justify="center")
            sleep(2)
