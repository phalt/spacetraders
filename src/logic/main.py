from typing import List
from rich.console import Console
from src.logic.actions.ships import ShipNavigate
from src.logic.actions.agents import ShowAgentStatus

from time import sleep

INIT_ACTIONS = [ShowAgentStatus()]

AUTOMATION_ACTIONS: List = [
    ShipNavigate(symbol="HALLETT-7", destination="X1-KS52-51225B")
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
        if not AUTOMATION_ACTIONS:
            break
        console.print(":counterclockwise_arrows_button:", emoji=True)
        for action in AUTOMATION_ACTIONS:
            console.rule(action.name)
            action.process()
            action.sleep()


if __name__ == "__main__":
    main()
