import click

from rich import print

print(":rocket: Paul's SpaceTraders.io client :moon:")


@click.group()
def cli_group():
    """
    CLI commands for Space traders
    """


@click.command()
def test_api_connectivity():
    """
    Basic API call to Spacetraders to test connectivity
    """
    from src.schemas import Agent
    from rich.pretty import pprint
    from rich import print

    result = Agent.me()
    pprint("API connection established, here is your Agent details:")
    print(str(result))
    pprint(result)


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
def contracts():
    """
    Returns contracts available to you
    """
    from src.schemas import ContractList
    from rich.pretty import pprint

    result = ContractList.get()
    pprint(result)


@click.command()
@click.argument("symbol")
def waypoint(symbol):
    """
    Return Waypoint information
    """
    from src.schemas import Waypoint
    from rich.pretty import pprint

    result = Waypoint.get(symbol=symbol)
    pprint(result)


@click.command()
@click.argument("symbol")
def shipyard(symbol):
    """
    Return Shipyard information
    """
    from src.schemas import Shipyard
    from rich.pretty import pprint

    result = Shipyard.get(symbol=symbol)
    pprint(result)


@click.command()
@click.argument("symbol")
def system_waypoints(symbol):
    """
    Return SystemWaypoints information
    """
    from src.schemas import SystemWaypoints
    from rich.pretty import pprint

    result = SystemWaypoints.get(symbol=symbol)
    pprint(result)


cli_group.add_command(test_api_connectivity)
cli_group.add_command(me)
cli_group.add_command(contracts)
cli_group.add_command(waypoint)
cli_group.add_command(shipyard)
cli_group.add_command(system_waypoints)

if __name__ == "__main__":
    cli_group()
