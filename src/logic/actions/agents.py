from rich.console import Console

from src.schemas.agent import Agent
from src.support.tables import attrs_to_rich_table


class ShowAgentStatus:
    name = ":man: Agent status"
    description = "Display the agent status"

    def sleep(self):
        pass

    def process(self):
        agent = Agent.me()
        console = Console()
        console.print(attrs_to_rich_table(Agent, [agent]))
