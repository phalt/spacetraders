from abc import ABC
from collections import defaultdict
from time import sleep
from typing import List, Optional

import attrs
from rich.console import Console
from rich.table import Table

from src.schemas.errors import Error
from src.schemas.mining import Extraction
from src.schemas.ships import Cargo, Nav, Ship
from src.schemas.transactions import Transaction
from src.support.tables import report_result


class AbstractMining(ABC):
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


class AbstractSellCargo(ABC):
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


class AbstractShipNavigate(ABC):
    console: Console
    expenses: int

    def navigate_to(self, ship: Ship, destination: str) -> Ship:
        """
        Navigate to the destination, returns the ship when it has arrived.
        """
        if ship.nav.waypointSymbol == destination and ship.nav.status in [
            "IN_ORBIT",
            "DOCKED",
        ]:
            return ship
        result = ship.orbit()
        result = ship.navigate(waypoint=destination)
        report_result(result=result, HappyClass=Nav)
        with self.console.status(f"Going to destination {destination}..."):
            arrived = False
            while arrived is False:
                result = ship.navigation_status()
                if result.waypointSymbol == destination and result.status == "IN_ORBIT":
                    arrived = True
                else:
                    # This will display seconds to arrival
                    result = ship.navigate(waypoint=destination)
                    report_result(result=result, HappyClass=Nav)
                    cooldown = result.data["secondsToArrival"]
                    sleep(cooldown)

        self.console.print(
            f"Ship arrived at {destination}, docking and refuelling",
        )

        result = ship.dock()
        result = ship.refuel()
        match result:
            case Error():
                report_result(result, Nav)
            case dict():
                report_result(result["transaction"], Transaction)
                self.expenses += result["transaction"].totalPrice
        return ship


@attrs.define
class SimpleShipNavigateAction(AbstractShipNavigate):
    """
    Simple action for navigating a ship to a destination.
    """

    destination: str
    ship_symbol: str
    console: Console = Console()
    expenses: int = 0

    def process(self):
        ship = Ship.get(self.ship_symbol)
        self.navigate_to(ship, self.destination)
