import attrs
from time import sleep
from rich.console import Console

from src.schemas.ships import Ship, ShipsManager, Nav, Cargo

from src.support.tables import attrs_to_rich_table, report_result


@attrs.define
class AbstractShipNavigate:
    """
    The best navigation functions to use.
    """

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
            self.console.print("Ship at destination, not navigating...")
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
