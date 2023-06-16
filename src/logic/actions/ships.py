import attrs
from time import sleep
from rich.console import Console

from src.schemas import Ship, ShipsManager, Nav, Cargo

from src.support.tables import attrs_to_rich_table, report_result


@attrs.define
class ShipNavigate:
    symbol: str
    destination: str

    @property
    def name(self) -> str:
        return f"Ship {self.symbol} navigate to {self.destination}"

    def sleep(self):
        sleep(20)

    def process(self):
        console = Console()
        ship = Ship.get(symbol=self.symbol)
        if (
            ship.nav.waypointSymbol == self.destination
            and ship.nav.status != "IN_TRANSIT"
        ):
            console.print(f"Ship {ship.symbol} has arrived at {self.destination}")
            if ship.nav.status == "IN_ORBIT":
                console.print("Ship is in orbit, docking...")
                result = ship.dock()
                report_result(result=result, HappyClass=Nav)
        if ship.nav.status == "DOCKED":
            console.print("Ship is docked, going to orbit...")
            result = ship.orbit()
            report_result(result=result, HappyClass=Nav)
        console.print(
            f"Ship is at {ship.nav.waypointSymbol}, navigating to {self.destination}..."
        )
        result = ship.navigate(waypoint=self.destination)
        report_result(result=result, HappyClass=Nav)


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
            console.print(f":package: Cargo for {ship.symbol}", emoji=True)
            console.print(attrs_to_rich_table(Cargo, [ship.cargo]))
