
import attrs
from rich.console import Console

from src.logic.actions.ships import (
    AbstractShipChart,
    AbstractShipJump,
    AbstractShipNavigate,
)
from src.schemas.ships import Ship


@attrs.define
class ShipExplore(AbstractShipNavigate, AbstractShipJump, AbstractShipChart):
    """
    Randomly explore the galaxy, reording where it has been and
    what interesting things it finds at waypoints.
    It will only go to waypoints that haven't been explored yet,
    so it is possible to send out many probes on this action at once.
    """

    destination: str
    ship_symbol: str
    console: Console = Console()
    expenses: int = 0

    @property
    def name(self) -> str:
        return f"{self.ship_symbol} going exploring..."

    async def process(self):
        self.console.rule(self.name)
        await Ship.get(self.ship_symbol)
        # Get the current system information.
        # Check to see which waypoints we have not visited yet.
        # If no waypoints remaining:
            # Go to jump gate
            # Jump
            # Restart this loop
        # Otherwise randomly pick an unexplored waypoint.
        # Navigate to it
        # Chart it
        # If it is a market place
            # record each trade good buy / sell value in the db.
        # If it is a shipyard
            # Record what ships are for sale and what price.
        # Record that we have visited it, what it is, what the traits are, etc.
        # Restart this loop
