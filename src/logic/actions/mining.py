import attrs
from time import sleep
from rich.console import Console

from src.schemas import Ship, Nav, Extraction, Cargo, Transaction
from src.schemas.errors import Error
from src.support.tables import report_result


@attrs.define
class MiningLoop:
    symbol: str
    destination: str
    console: Console = Console()
    fuel_cost: int = 0
    sell_total: int = 0

    @property
    def name(self) -> str:
        return f"Ship {self.symbol} mining @ {self.destination}"

    def sleep(self):
        pass

    def navigate_to(self, ship: Ship) -> Ship:
        """
        Navigate to the destination, returns the ship when it has arrived.
        """
        if ship.nav.waypointSymbol == self.destination and ship.nav.status in [
            "IN_ORBIT",
            "DOCKED",
        ]:
            self.console.print("Ship at destination, not navigating...")
            return ship
        self.console.print("Going to orbit...")
        result = ship.orbit()
        report_result(result=result, HappyClass=Nav)

        self.console.print(f"Going to destination {self.destination}")
        result = ship.navigate(waypoint=self.destination)
        report_result(result=result, HappyClass=Nav)

        arrived = False
        while arrived is False:
            result = ship.navigation_status()
            if (
                result.waypointSymbol == self.destination
                and result.status == "IN_ORBIT"
            ):
                self.console.print(f"Ship arrived at {self.destination}")
                report_result(result=result, HappyClass=Nav)
                arrived = True
            else:
                self.console.print("Ship in transit")
                # This will display seconds to arrival
                result = ship.navigate(waypoint=self.destination)
                report_result(result=result, HappyClass=Nav)
                sleep(20)

        result = ship.dock()
        report_result(result, Nav)
        result = ship.refuel()
        self.console.print(result)
        self.fuel_cost = result["transaction"].totalPrice
        return ship

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
        while cargo_status.units <= cargo_status.capacity:
            result = ship.extract()
            if isinstance(result, Error):
                report_result(result, Extraction)
                cooldown = result.data["cooldown"]
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
        items_units = [
            (x['symbol'], x['units']) for x in cargo.inventory
        ]
        self.console.print(f"Total cargo to sell: {items_units}")
        for symbol, units in items_units:
            self.console.log(f"Selling {symbol}...")
            result = ship.sell(symbol=symbol, amount=units)
            if isinstance(result, Error):
                report_result(result, Ship)
            else:
                transaction = result['transaction']
                report_result(transaction, Transaction)
                self.sell_total +=  transaction.totalPrice
        return ship


    def process(self):
        ship = Ship.get(symbol=self.symbol)
        ship = self.navigate_to(ship)
        ship = self.mine_until_cargo_full(ship)
        ship = self.sell_cargo(ship)

        self.console.print(
            f"Total earned from mining run = {self.sell_total - self.fuel_cost}"
        )
