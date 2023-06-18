from typing import List
from rich.console import Console
from src.logic.actions.mining import MiningLoop
from src.logic.actions.contracts import ContractMiningLoop
from src.logic.actions.agents import ShowAgentStatus

from time import sleep

INIT_ACTIONS = [ShowAgentStatus()]

AUTOMATION_ACTIONS: List = [
    MiningLoop(ship_symbol="GOOGL-3", destination="X1-KS52-51225B")
]


def main():
    "The main automation loop"
    console = Console()
    with console.status("Launching to space... :star:"):
        sleep(1)

    for action in INIT_ACTIONS:
        console.rule(action.name)
        action.process()
        action.sleep()

    while True:
        for action in AUTOMATION_ACTIONS:
            console.rule(action.name)
            action.process()
            action.sleep()


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
