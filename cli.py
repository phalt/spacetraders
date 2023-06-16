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
def register(symbol, faction):
    """
    Register a new agent.
    """
    from src.schemas import AgentManager, Error
    from rich.pretty import pprint
    from structlog import get_logger

    log = get_logger(__name__)

    result = AgentManager.register_new(symbol=symbol, faction=faction)
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
    from src.schemas import Agent
    from rich.pretty import pprint

    result = Agent.me()
    pprint(result)


@click.command()
@click.argument("depth", default=1)
def contracts(depth):
    """
    Returns contracts available to you
    """
    from src.schemas import ContractManager
    from rich.pretty import pprint

    result = ContractManager.get()
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def waypoint(symbol, depth):
    """
    Return Waypoint information
    """
    from src.schemas import Waypoint
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
    from src.schemas import Shipyard
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
    from src.schemas import Market
    from rich.pretty import pprint

    result = Market.get(symbol=symbol)
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("content", required=False)
@click.argument("depth", default=1)
def ship(symbol, content, depth):
    """
    Return Ship information
    Second argument determines content
    """
    from src.schemas import Ship
    from rich.pretty import pprint

    ship = Ship.get(symbol=symbol)
    if content == "cargo":
        pprint(ship.cargo_status(), max_depth=int(depth))
    elif content == "nav":
        pprint(ship.navigation_status(), max_depth=int(depth))
    else:
        content = content or 1
        pprint(ship, max_depth=int(content))


@click.command()
@click.argument("depth", default=1)
def ships(depth):
    """
    Return all ship information
    """
    from src.schemas import ShipsManager
    from rich.pretty import pprint

    result = ShipsManager.all()
    pprint(result, max_depth=int(depth))


@click.command()
@click.argument("symbol")
@click.argument("depth", default=1)
def system_waypoints(symbol, depth):
    """
    Return SystemWaypoints information
    """
    from src.schemas import SystemWaypoints
    from rich.pretty import pprint

    result = SystemWaypoints.get(symbol=symbol)
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
    from src.schemas import ShipsManager
    from rich.pretty import pprint

    result = ShipsManager.buy_ship(ship_type=ship, waypoint_symbol=waypoint)
    pprint(result, max_depth=int(depth))


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

if __name__ == "__main__":
    cli_group()
