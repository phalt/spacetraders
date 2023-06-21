from rich.console import Console

from src.logic.actions.contracts import ContractMiningLoop
from src.logic.actions.mining import MiningLoop


async def mining_loop(ship_symbol, destination, with_surveys):
    action = MiningLoop(
        ship_symbol=ship_symbol, destination=destination, with_surveys=with_surveys
    )
    console = Console()
    console.rule(action.name)
    while True:
        await action.process()


def mining_contract_loop(ship_symbol, contract_id, mining_destination):
    action = ContractMiningLoop(
        ship_symbol=ship_symbol,
        contract_id=contract_id,
        mining_destination=mining_destination,
    )
    console = Console()
    contract_fulfilled = False
    while contract_fulfilled is False:
        console.rule(action.name)
        contract_fulfilled = action.process()
