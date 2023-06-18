from typing import List, Optional
import attrs
from time import sleep
from rich.console import Console
from rich.table import Table

from collections import defaultdict

from src.schemas.ships import Ship, ShipsManager, Nav, Cargo
from src.schemas.errors import Error
from src.schemas.mining import Extraction
from src.schemas.transactions import Transaction
from src.support.tables import attrs_to_rich_table, report_result


@attrs.define
class AbstractMining:
    def mine_until_cargo_full(self, ship: Ship) -> Ship:
        ship.orbit()
        cargo_status = ship.cargo_status()
        match cargo_status:
            case Error():
                report_result(cargo_status, Cargo)
            case Cargo():
                if cargo_status.units == cargo_status.capacity:
                    self.console.print("Cargo is full")
                    report_result(cargo_status, Cargo)
                    return ship

                with self.console.status("mining until cargo full..."):
                    mining_results = defaultdict(int)
                    mining_table = Table(title="Mining results")
                    mining_table.add_column("symbol")
                    mining_table.add_column("yield")
                    while cargo_status.units < cargo_status.capacity:
                        result = ship.extract()
                        match result:
                            case Error():
                                report_result(result, Extraction)
                                cooldown = result.data.get("cooldown")
                                if cooldown:
                                    sleep(cooldown["remainingSeconds"])
                            case dict():
                                extraction: Extraction = result["extraction"]
                                mining_results[
                                    extraction.yield_["symbol"]
                                ] += extraction.yield_["units"]
                                cooldown = result["cooldown"].remainingSeconds
                                sleep(cooldown)
                        cargo_status = ship.cargo_status()
                    for symbol, units in mining_results.items():
                        mining_table.add_row(symbol, str(units))

        self.console.print(mining_table)
        return ship


@attrs.define
class AbstractSellCargo:
    def sell_cargo(
        self, ship: Ship, do_not_sell_symbols: Optional[List[str]] = []
    ) -> Ship:
        """
        Sell all the contents of the cargo except trade good.
        """
        ship.dock()
        cargo = ship.cargo_status()

        match cargo:
            case Error():
                report_result(cargo, Cargo)
            case Cargo():
                with self.console.status("Selling cargo..."):
                    this_cargo_sale = 0
                    cargo_table = Table(title="Cargo sold")
                    cargo_table.add_column("symbol")
                    cargo_table.add_column("units")
                    cargo_table.add_column("price per unit")
                    cargo_table.add_column("total price")
                    items_units = [
                        (x["symbol"], x["units"])
                        for x in cargo.inventory
                        if x["symbol"] not in do_not_sell_symbols
                    ]
                    for symbol, units in items_units:
                        result = ship.sell(symbol=symbol, amount=units)
                        match result:
                            case Error():
                                report_result(result, Ship)
                            case dict():
                                transaction: Transaction = result["transaction"]
                                cargo_table.add_row(
                                    symbol,
                                    str(units),
                                    str(transaction.pricePerUnit),
                                    str(transaction.totalPrice),
                                )
                                self.cargo_sales += transaction.totalPrice
                                this_cargo_sale += transaction.totalPrice
                self.console.print(cargo_table)
                self.console.print(f"Total credits earned: {this_cargo_sale}")
        return ship


@attrs.define
class AbstractShipNavigate:
    ship_symbol: str
    console: Console = Console()

    def navigate_to(self, ship: Ship, destination: str) -> Ship:
        """
        Navigate to the destination, returns the ship when it has arrived.
        """
        if ship.nav.waypointSymbol == destination and ship.nav.status in [
            "IN_ORBIT",
            "DOCKED",
        ]:
            return ship
        self.console.print("Going to orbit...")
        result = ship.orbit()
        report_result(result=result, HappyClass=Nav)

        self.console.print(f"Going to destination {destination}")
        result = ship.navigate(waypoint=destination)
        report_result(result=result, HappyClass=Nav)

        arrived = False
        while arrived is False:
            result = ship.navigation_status()
            if result.waypointSymbol == destination and result.status == "IN_ORBIT":
                self.console.print(f"Ship arrived at {destination}")
                report_result(result=result, HappyClass=Nav)
                arrived = True
            else:
                self.console.print("Ship in transit")
                # This will display seconds to arrival and will always be an error class
                result = ship.navigate(waypoint=destination)
                report_result(result=result, HappyClass=Nav)
                cooldown = result.data["secondsToArrival"]
                sleep(cooldown)

        result = ship.dock()
        report_result(result, Nav)
        result = ship.refuel()
        self.console.print(result)
        self.expenses += result["transaction"].totalPrice
        return ship


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
