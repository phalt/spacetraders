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
    from src.api.client import test_connectivity
    from rich.pretty import pprint

    result = test_connectivity()
    pprint("API connection established, here is your Agent details:")
    pprint(result)


cli_group.add_command(test_api_connectivity)

if __name__ == "__main__":
    cli_group()
