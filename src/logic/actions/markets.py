import attrs
from rich.console import Console

from src.schemas.ships import Ship

from .ships import AbstractSellCargo, AbstractShipNavigate


@attrs.define
class MarketSell(AbstractShipNavigate, AbstractSellCargo):
    ship_symbol: str
    destination: str
    console: Console = Console()
    cargo_sales: int = 0
    expenses: int = 0

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} selling @ {self.destination}"

    def process(self):
        ship = Ship.get(symbol=self.ship_symbol)
        ship = self.navigate_to(ship, self.destination)
        ship = self.sell_cargo(ship)
