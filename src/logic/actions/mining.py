import attrs
from rich.console import Console

from src.schemas.ships import Ship

from .ships import AbstractMining, AbstractSellCargo, AbstractShipNavigate


@attrs.define
class MiningLoop(AbstractShipNavigate, AbstractSellCargo, AbstractMining):
    ship_symbol: str
    destination: str
    console: Console = Console()
    cargo_sales: int = 0
    expenses: int = 0
    with_surveys: bool = False

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} mining @ {self.destination}"

    def process(self):
        ship = Ship.get(symbol=self.ship_symbol)
        ship = self.navigate_to(ship, self.destination)
        ship = self.mine_until_cargo_full(ship, self.destination)
        ship = self.sell_cargo(ship)

        self.console.print(
            f"Total earned from mining run = {self.cargo_sales - self.expenses}"
        )
