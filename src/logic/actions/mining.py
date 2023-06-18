import attrs
from time import sleep
from rich.console import Console

from src.schemas.ships import Ship, Cargo
from src.schemas.mining import Extraction
from src.schemas.transactions import Transaction
from src.schemas.errors import Error
from src.support.tables import report_result
from .ships import AbstractShipNavigate


@attrs.define
class MiningLoop(AbstractShipNavigate):
    ship_symbol: str
    destination: str
    console: Console = Console()
    sell_total: int = 0
    expenses: int = 0

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} mining @ {self.destination}"

    def sleep(self):
        pass

    def mine_until_cargo_full(self, ship: Ship) -> Ship:
        """
        Mine until the cargo is full, then report the contents of the cargo.
        """
        ship.orbit()
        cargo_status = ship.cargo_status()
        if cargo_status.units == cargo_status.capacity:
            self.console.print("Cargo is full")
            report_result(cargo_status, Cargo)
            return ship

        self.console.print("Mining...")
        while cargo_status.units < cargo_status.capacity:
            result = ship.extract()
            if isinstance(result, Error):
                report_result(result, Extraction)
                cooldown = result.data.get("cooldown")
                if cooldown:
                    sleep(cooldown["remainingSeconds"])
            else:
                report_result(result["extraction"], Extraction)
                cooldown = result["cooldown"].remainingSeconds
                self.console.print(f"Cooldown for {cooldown} seconds")
                sleep(cooldown)
            cargo_status = ship.cargo_status()

        self.console.print("Cargo is full")
        report_result(cargo_status, Cargo)
        return ship

    def sell_cargo(self, ship: Ship) -> Ship:
        """
        Sell all the contents of the cargo
        """
        ship.dock()
        cargo = ship.cargo_status()
        items_units = [(x["symbol"], x["units"]) for x in cargo.inventory]
        self.console.print(f"Total cargo to sell: {items_units}")
        for symbol, units in items_units:
            self.console.log(f"Selling {symbol}...")
            result = ship.sell(symbol=symbol, amount=units)
            if isinstance(result, Error):
                report_result(result, Ship)
            else:
                transaction = result["transaction"]
                report_result(transaction, Transaction)
                self.sell_total += transaction.totalPrice
        return ship

    def process(self):
        ship = Ship.get(symbol=self.ship_symbol)
        ship = self.navigate_to(ship, self.destination)
        ship = self.mine_until_cargo_full(ship)
        ship = self.sell_cargo(ship)

        self.console.print(
            f"Total earned from mining run = {self.sell_total - self.expenses}"
        )
