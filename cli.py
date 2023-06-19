import click

from rich import print

print(":rocket: Paul's SpaceTraders.io client :moon:")


@click.group()
def cli_group():
    """
    CLI commands for Space traders
    """


@click.command()
@click.argument("symbol")
@click.argument("faction", default="COSMIC")
@click.argument("email", default="")
def register(symbol, faction, email):
    """
    Register a new agent.
    """
    from src.schemas.agent import AgentManager
    from src.schemas.errors import Error
    from rich.pretty import pprint
    from structlog import get_logger

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
    Return Agent details about yourself
    """
    from src.schemas.agent import Agent
    from src.support.tables import report_result

    result = Agent.me()
    report_result(result, Agent)


@click.command()
@click.argument("depth", default=1)
def contracts(depth):
    """
    Returns contracts available to you
    """
    from src.schemas.contracts import ContractManager
    from rich.pretty import pprint

    result = ContractManager.all()
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def waypoint(symbol, depth):
    """
    Return Waypoint information
    """
    from src.schemas.waypoint import Waypoint
    from rich.pretty import pprint

    result = Waypoint.get(symbol=symbol)
    pprint(result, max_depth=depth)


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def shipyard(symbol, depth):
    """
    Return Shipyard information
    """
    from src.schemas.waypoint import Shipyard
    from rich.pretty import pprint

    result = Shipyard.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def market(symbol, depth):
    """
    Return Market information
    """
    from src.schemas.markets import Market
    from rich.pretty import pprint

    result = Market.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("content", default="1")
def ship(symbol, content):
    """
    Return Ship information
    Second argument determines content
    """
    from src.schemas.ships import Ship, Cargo, Nav
    from src.support.tables import report_result
    from rich.pretty import pprint

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
    from src.schemas.ships import ShipsManager, Cargo, Nav
    from src.support.tables import report_result
    from rich.pretty import pprint
    from rich.console import Console

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
@click.argument("depth", default=1)
def system_waypoints(symbol, depth):
    """
    Return SystemWaypoints information
    """
    from src.schemas.systems import SystemWaypoints
    from rich.pretty import pprint

    result = SystemWaypoints.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def system(symbol, depth):
    """
    Return System information
    """
    from src.schemas.systems import System
    from rich.pretty import pprint

    result = System.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("ship")
@click.argument("waypoint")
@click.argument("depth", default=1)
def buy_ship(ship, waypoint, depth):
    """
    Purchase a ship.
    You must have a ship docked at this waypoint to purchase.
    """
    from src.schemas.ships import ShipsManager
    from rich.pretty import pprint

    result = ShipsManager.buy_ship(ship_type=ship, waypoint_symbol=waypoint)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("depth", default=1)
def status(depth):
    """
    Purchase a ship.
    You must have a ship docked at this waypoint to purchase.
    """
    from rich.pretty import pprint
    from src.api import bare_client, PATHS

    result = bare_client.get(PATHS.SERVER_STATUS)
    pprint(result.json(), max_depth=int(depth))


@click.command()
def loop():
    """
    Begin the automation loop.
    """
    from src.logic.main import main

    main()


@click.command()
@click.argument("ship_symbol")
@click.argument("contract_id")
@click.argument("mining_destination")
def contract_mining(ship_symbol, contract_id, mining_destination):
    """
    Set a ship on a loop procurring contract items.
    Assumes contract is a simple mining contract.
    We can get all info we need from the contract.
    """
    from src.logic.main import mining_contract_loop

    mining_contract_loop(ship_symbol, contract_id, mining_destination)


@click.command()
@click.argument("ship_symbol")
@click.argument("destination")
def mining(ship_symbol, destination):
    """
    Set a ship on the mining loop automation script.
    """
    from src.logic.main import mining_loop

    mining_loop(ship_symbol, destination)


cli_group.add_command(register)
cli_group.add_command(me)
cli_group.add_command(contracts)
cli_group.add_command(waypoint)
cli_group.add_command(shipyard)
cli_group.add_command(market)
cli_group.add_command(ship)
cli_group.add_command(ships)
cli_group.add_command(buy_ship)
cli_group.add_command(system_waypoints)
cli_group.add_command(system)
cli_group.add_command(status)
cli_group.add_command(loop)
cli_group.add_command(mining)
cli_group.add_command(contract_mining)

if __name__ == "__main__":
    cli_group()
