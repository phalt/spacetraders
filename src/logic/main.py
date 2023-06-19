from rich.console import Console
from src.logic.actions.mining import MiningLoop
from src.logic.actions.contracts import ContractMiningLoop


def mining_loop(ship_symbol, destination):
    action = MiningLoop(ship_symbol=ship_symbol, destination=destination)
    console = Console()
    while True:
        console.rule(action.name)
        action.process()


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
