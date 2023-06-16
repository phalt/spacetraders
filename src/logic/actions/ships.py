import attrs
from rich.table import Table
from rich.console import Console
from time import sleep

from src.schemas import Ship, ShipsManager, Nav, Cargo
from src.schemas.errors import Error

from src.support.tables import attrs_to_rich_table


@attrs.define
class ShipNavigate:
    symbol: str
    destination: str

    @property
    def name(self) -> str:
        return f"Ship {self.symbol} navigate to {self.destination}"

    def sleep(self):
        pass

    def process(self):
        ship = Ship.get(symbol=self.symbol)
        result = ship.navigate(waypoint=self.destination)
        match result:
            case Error():
                print(Error)
            case Nav():
                Table()


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
