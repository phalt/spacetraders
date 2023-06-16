from typing import List
from rich.console import Console
from src.logic.actions.ships import ShowShipCargoStatus
from src.logic.actions.agents import ShowAgentStatus

from time import sleep

INIT_ACTIONS = [ShowAgentStatus(), ShowShipCargoStatus()]

AUTOMATION_ACTIONS: List = []


def main():
    "The main automation loop"
    console = Console()
    with console.status("Launching to space... :star:"):
        sleep(2)

    for action in INIT_ACTIONS:
        console.rule(action.name)
        action.process()
        action.sleep()

    while True:
        print(":counterclockwise_arrows_button:")
        for action in AUTOMATION_ACTIONS:
            console.rule(action.name)
            action.process()
            action.sleep()


if __name__ == "__main__":
    main()
