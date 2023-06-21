import attrs
from rich.console import Console

from src.schemas.ships import Ship
from src.support.tables import blue, pink

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
        return f"Ship {self.ship_symbol} mining loop @ {self.destination}"

    async def process(self):
        ship = await Ship.get(symbol=self.ship_symbol)
        ship = await self.navigate_to(ship, self.destination)
        ship = await self.mine_until_cargo_full(ship, self.destination)
        ship = await self.sell_cargo(ship)

        self.console.print(
            f"{blue(ship.symbol)} total earned from mining = {pink(self.cargo_sales - self.expenses)}"
        )
