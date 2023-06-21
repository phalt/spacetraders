import asyncio
from abc import ABC
from collections import defaultdict
from typing import List, Optional

import attrs
from rich.console import Console
from rich.table import Table

from src.schemas.errors import Error
from src.schemas.mining import Extraction, Survey
from src.schemas.ships import Cargo, Nav, Ship
from src.schemas.transactions import Transaction
from src.schemas.waypoint import Waypoint
from src.support.datetime import local_now
from src.support.tables import blue, pink, report_result, yellow


class AbstractMining(ABC):
    with_surveys: bool

    async def mine_until_cargo_full(self, ship: Ship, destination: str) -> Ship:
        await ship.orbit()
        cargo_status = await ship.cargo_status()
        match cargo_status:
            case Error():
                report_result(cargo_status, Cargo)
            case Cargo():
                if cargo_status.units == cargo_status.capacity:
                    self.console.print(f"{blue(ship.symbol)} cargo is full")
                    report_result(cargo_status, Cargo)
                    return ship

                self.console.print(
                    f"{blue(ship.symbol)} mining @ {yellow(destination)}"
                )
                mining_results = defaultdict(int)
                mining_table = Table(title=f"{blue(ship.symbol)} mining results")
                mining_table.add_column("symbol")
                mining_table.add_column("yield")
                while cargo_status.units < cargo_status.capacity:
                    valid_survey = None
                    if self.with_surveys:
                        surveys = Survey.filter(symbol=destination)
                        for s in surveys:
                            if s.expiration.local_time > local_now():
                                valid_survey = s
                        if valid_survey:
                            self.console.print(
                                f"Using Survey {valid_survey.signature} to mine"
                            )
                    result = await ship.extract(survey=valid_survey)
                    match result:
                        case Error():
                            self.console.print(result)
                            cooldown = result.data.get("cooldown")
                            if cooldown:
                                await asyncio.sleep(cooldown["remainingSeconds"])
                        case dict():
                            extraction: Extraction = result["extraction"]
                            mining_results[
                                extraction.yield_["symbol"]
                            ] += extraction.yield_["units"]
                            cooldown = result["cooldown"].remainingSeconds
                            await asyncio.sleep(cooldown)
                    cargo_status = await ship.cargo_status()
                for symbol, units in mining_results.items():
                    mining_table.add_row(symbol, str(units))
        self.console.print(f"{blue(ship.symbol)} finished mining")
        self.console.print(mining_table)
        return ship


class AbstractSellCargo(ABC):
    async def sell_cargo(
        self, ship: Ship, do_not_sell_symbols: Optional[List[str]] = []
    ) -> Ship:
        """
        Sell all the contents of the cargo except trade good.
        """
        await ship.dock()
        cargo = await ship.cargo_status()

        match cargo:
            case Error():
                report_result(cargo, Cargo)
            case Cargo():
                self.console.print(f"{blue(ship.symbol)} selling cargo")
                this_cargo_sale = 0
                cargo_table = Table(title=f"{blue(ship.symbol)} cargo sold")
                cargo_table.add_column("symbol")
                cargo_table.add_column("units")
                cargo_table.add_column("price per unit")
                cargo_table.add_column("total price")
                items_units = [
                    (x.symbol, x.units)
                    for x in cargo.inventory
                    if x.symbol not in do_not_sell_symbols
                ]
                self.console.print(items_units)
                for symbol, units in items_units:
                    result = await ship.sell(symbol=symbol, amount=units)
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
                self.console.print(
                    f"{blue(ship.symbol)} earned from sales: {pink(this_cargo_sale)}"
                )
        return ship


class AbstractShipNavigate(ABC):
    console: Console
    expenses: int
    navigate_waypoint: Waypoint

    async def navigate_to(
        self,
        ship: Ship,
        destination: str,
        dock: Optional[bool] = True,
        refuel: Optional[bool] = True,
    ) -> Ship:
        """
        Navigate to the destination, returns the ship when it has arrived.
        If dock is true, will attempt to dock when arrived.
        If refuel is true, will refuel if the destination waypoint has a marketplace and is selling fuel.
        """
        self.navigate_waypoint = await Waypoint.get(symbol=destination)
        if ship.nav.waypointSymbol == destination and ship.nav.status in [
            "IN_ORBIT",
            "DOCKED",
        ]:
            # Ship is already at this location
            self.console.print(f"{blue(ship.symbol)} arrrived @ {yellow(destination)}")
            return ship
        result = await ship.orbit()
        self.console.print(
            f"{blue(ship.symbol)} navigating to destination {yellow(destination)}"
        )
        arrived = False
        while arrived is False:
            result = await ship.navigation_status()
            if result.waypointSymbol == destination and result.status == "IN_ORBIT":
                arrived = True
            else:
                # This will display seconds to arrival
                result = await ship.navigate(waypoint=destination)
                report_result(result=result, HappyClass=Nav)
                cooldown = result.data["secondsToArrival"]
                await asyncio.sleep(cooldown)

        self.console.print(
            f"{blue(ship.symbol)} arrived at {yellow(destination)}",
        )
        if dock:
            self.console.print(f"{blue(ship.symbol)} docking")
            await ship.dock()
        if refuel and await self.navigate_waypoint.can_refuel():
            self.console.print(f"{blue(ship.symbol)} refueling")
            result = await ship.refuel()
            match result:
                case Error():
                    report_result(result, Nav)
                case dict():
                    report_result(result["transaction"], Transaction)
                    self.expenses += result["transaction"].totalPrice
        self.console.print(f"{blue(ship.symbol)} arrrived @ {yellow(destination)}")
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

    @property
    def name(self) -> str:
        return f"{self.ship_symbol} navigating to {self.destination}"

    async def process(self):
        self.console.rule(self.name)
        ship = await Ship.get(self.ship_symbol)
        ship = await self.navigate_to(ship, self.destination)
