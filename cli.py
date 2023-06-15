import click


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


cli_group.add_command(test_api_connectivity)

if __name__ == "__main__":
    cli_group()
