import attrs
from rich.console import Console

from src.db.models.systems import SystemMappingStatusModel
from src.db.models.waypoints import MappedEnum
from src.logic.actions.ships import (
    AbstractShipChart,
    AbstractShipJump,
    AbstractShipNavigate,
)
from src.schemas.ships import Ship
from src.schemas.systems import System
from src.schemas.waypoint import Waypoint
from src.support.tables import blue, yellow


@attrs.define
class ShipExplore(AbstractShipNavigate, AbstractShipJump, AbstractShipChart):
    """
    Randomly explore the galaxy, reording where it has been and
    what interesting things it finds at waypoints.
    It will only go to waypoints that haven't been explored yet,
    so it is possible to send out many probes on this action at once.
    """

    ship_symbol: str
    mapping_this_system: bool = False
    console: Console = Console()
    expenses: int = 0

    @property
    def name(self) -> str:
        return f"{self.ship_symbol} going exploring..."

    async def map_system(self, ship: Ship, current_system: System) -> None:
        """
        Map all the way points in this system.
        """
        for w in current_system.waypoints:
            waypoint = await Waypoint.get(w.symbol)
            if waypoint.mapped != MappedEnum.MAPPED:
                await self.navigate_to(ship, destination=waypoint.symbol)
                await self.chart_waypoint(ship)
                # If it is a market place
                # record each trade good buy / sell value in the db.
                # If it is a shipyard
                # Record what ships are for sale and what price.
                # Record that we have visited it, what it is, what the traits are, etc.
                waypoint.set_mapped()
                self.console.print(
                    f"{blue(ship.symbol)} mapped waypoint {yellow(waypoint.symbol)}"
                )
        current_system.mapping_complete(ship_symbol=ship.symbol)
        self.console.print(
            f"{blue(ship.symbol)} mapped system {yellow(current_system.symbol)}"
        )

    async def process(self):
        self.console.rule(self.name)
        ship = await Ship.get(self.ship_symbol)
        current_system = await System.get(symbol=ship.nav.systemSymbol)
        self.console.print(f"{blue(ship.symbol)} @ {yellow(current_system.symbol)}")
        if current_system.mapped == MappedEnum.UN_MAPPED:
            # Claim it!
            current_system.mapping_in_progress(ship.symbol)
            self.console.print(
                f"{blue(ship.symbol)} mapping {yellow(current_system.symbol)}"
            )
            self.mapping_this_system = True
        if current_system.mapped == MappedEnum.INCOMPLETE:
            # Are we the one working on it?
            ship_mapping_this = (
                SystemMappingStatusModel.in_progress_for_ship(ship.symbol)
                .filter(SystemMappingStatusModel.symbol == current_system.symbol)
                .count()
                == 1
            )
            if ship_mapping_this:
                self.console.print(
                    f"{blue(ship.symbol)} was mapping {yellow(current_system.symbol)}, resuming..."
                )
                self.mapping_this_system = True
        if current_system.mapped == MappedEnum.MAPPED:
            # Go to another system
            self.mapping_this_system = False

        if self.mapping_this_system:
            await self.map_system(ship, current_system)
            self.mapping_this_system = False
        else:
            pass
            # Go to jump gate
            # Jump
            # Restart this loop
        # Check to see which waypoints we have not visited yet.
        # If no waypoints remaining:
        # Otherwise randomly pick an unexplored waypoint.
        # Navigate to it
        # Chart it

        # Restart this loop
