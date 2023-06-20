import click
from rich import print

print(":rocket: Paul's SpaceTraders.io client :moon:")


@click.group()
def cli_group():
    """
    CLI commands for Paul's SpaceTraders.io client
    """


@click.command()
@click.argument("symbol")
@click.argument("faction", default="COSMIC")
@click.argument("email", default="")
def register(symbol, faction, email):
    """
    Register a new agent
    """
    from rich.pretty import pprint
    from structlog import get_logger

    from src.schemas.agent import AgentManager
    from src.schemas.errors import Error

    log = get_logger(__name__)

    result = AgentManager.register_new(symbol=symbol, faction=faction, email=email)
    if isinstance(result, Error):
        pprint(result)
    else:
        content = f"""
Agent created!
Copy and paste this into a file called `env.ini` in the project root to get started:

[api]
key = {result.token}

After you saved that run `make query q='me'` to test it all worked
"""

        log.info(content)


@click.command()
def me():
    """
    Details about yourself
    """
    from src.schemas.agent import Agent
    from src.support.tables import report_result

    result = Agent.me()
    report_result(result, Agent)


@click.command()
@click.option("-d", "--depth", help="Expand fields", default=1)
def contracts(depth):
    """
    Contracts available to you
    """
    from rich.pretty import pprint

    from src.schemas.contracts import ContractManager

    result = ContractManager.all()
    for contract in result.contracts:
        pprint(contract, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.option("-d", "--depth", help="Expand fields", default=1)
def waypoint(symbol, depth):
    """
    Waypoint information
    """
    from rich.pretty import pprint

    from src.schemas.waypoint import Waypoint

    result = Waypoint.get(symbol=symbol)
    pprint(result, max_depth=depth)


@click.command()
@click.argument("symbol")
@click.option("-d", "--depth", help="Expand fields", default=1)
def shipyard(symbol, depth):
    """
    Shipyard information
    """
    from rich.pretty import pprint

    from src.schemas.waypoint import Shipyard

    result = Shipyard.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.option("-d", "--depth", help="Expand fields", default=1)
def marketplace(symbol, depth):
    """
    Market information
    """
    from rich.pretty import pprint

    from src.schemas.markets import Market

    result = Market.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("content", default="1")
def ship(symbol, content):
    """
    Ship info. Second argument determines content
    """
    from rich.pretty import pprint

    from src.schemas.ships import Cargo, Nav, Ship
    from src.support.tables import report_result

    ship = Ship.get(symbol=symbol)
    if content == "cargo":
        pprint(f"{ship.symbol}")
        report_result(ship.cargo_status(), Cargo)
    elif content == "nav":
        pprint(f"{ship.symbol}")
        report_result(ship.navigation_status(), Nav)
    else:
        pprint(ship, max_depth=int(content))


@click.command()
@click.argument("content", default="1")
def ships(content):
    """
    Return all ship information
    """
    from rich.console import Console
    from rich.pretty import pprint

    from src.schemas.ships import Cargo, Nav, ShipsManager
    from src.support.tables import report_result

    console = Console()

    result = ShipsManager.all()
    if content == "cargo":
        for ship in result.ships:
            console.rule(f"{ship.symbol}")
            report_result(ship.cargo_status(), Cargo)
    elif content == "nav":
        for ship in result.ships:
            console.rule(f"{ship.symbol}")
            report_result(ship.navigation_status(), Nav)
    else:
        pprint(result, max_depth=int(content))


@click.command()
@click.argument("symbol")
@click.option("-d", "--depth", help="Expand fields", default=1)
def system_waypoints(symbol, depth):
    """
    Return SystemWaypoints information
    """
    from rich.pretty import pprint

    from src.schemas.systems import SystemWaypoints

    result = SystemWaypoints.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.option("-d", "--depth", help="Expand fields", default=1)
def system(symbol, depth):
    """
    Return System information
    """
    from rich.pretty import pprint

    from src.schemas.systems import System

    result = System.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.option("--ship", help="Ship type", required=True)
@click.option("--waypoint", help="Shipyard waypoint", required=True)
@click.option("-d", "--depth", help="Expand fields", default=1)
def buy_ship(ship, waypoint, depth):
    """
    Purchase a ship.

    You must have a ship docked at this waypoint and it must have a shipyard.
    """
    from rich.pretty import pprint

    from src.schemas.ships import ShipsManager

    result = ShipsManager.buy_ship(ship_type=ship, waypoint_symbol=waypoint)
    pprint(result, max_depth=int(depth))


@click.command()
@click.option("-d", "--depth", help="Expand fields", default=1)
def status(depth):
    """
    Purchase a ship.
    You must have a ship docked at this waypoint to purchase.
    """
    from rich.pretty import pprint

    from src.api import PATHS, bare_client

    result = bare_client.get(PATHS.SERVER_STATUS)
    pprint(result.json(), max_depth=int(depth))


@click.command()
@click.option("--ship", "-s", help="ship symbol", required=True)
@click.option("--id", "-c", help="Contract ID", required=True)
@click.option("--mine", "-d", help="destination to mine", required=True)
def contract_mining(ship, id, mine):
    """
    Set a ship on a loop procurring contract items
    """
    from src.logic.main import mining_contract_loop

    mining_contract_loop(ship_symbol=ship, contract_id=id, mining_destination=mine)


@click.command()
@click.option("--ship", "-s", help="ship symbol", required=True)
@click.option("--dest", "-d", help="destination to mine", required=True)
def mining(ship, dest):
    """
    Set a ship on the mining loop
    """
    from src.logic.main import mining_loop

    mining_loop(ship_symbol=ship, destination=dest)


@click.command()
@click.option("--ship", "-s", help="ship symbol", required=True)
@click.option("--dest", "-d", help="destination", required=True)
def navigate(ship, dest):
    """
    Set a ship to navigate to a destination
    """
    from src.logic.actions.ships import SimpleShipNavigateAction

    SimpleShipNavigateAction(ship_symbol=ship, destination=dest).process()


@click.command()
@click.option("--ship", "-s", help="ship symbol", required=True)
@click.option("--dest", "-d", help="destination", required=True)
def survey(ship, dest):
    """
    Set a ship to navigate to a destination and survey it endlessly
    """
    from src.logic.actions.surveys import SurveyDestinationAction

    SurveyDestinationAction(ship_symbol=ship, destination=dest).process()


cli_group.add_command(register)
cli_group.add_command(me)
cli_group.add_command(contracts)
cli_group.add_command(waypoint)
cli_group.add_command(shipyard)
cli_group.add_command(marketplace)
cli_group.add_command(ship)
cli_group.add_command(ships)
cli_group.add_command(buy_ship)
cli_group.add_command(system_waypoints)
cli_group.add_command(system)
cli_group.add_command(status)
cli_group.add_command(mining)
cli_group.add_command(contract_mining)
cli_group.add_command(navigate)
cli_group.add_command(survey)

if __name__ == "__main__":
    cli_group()
