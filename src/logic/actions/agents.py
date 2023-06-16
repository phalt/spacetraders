from rich.table import Table
from rich.console import Console

from src.schemas import Agent


class ShowAgentStatus:
    name = ":man: Agent status"
    description = "Display the agent status"

    def sleep(self):
        pass

    def process(self):
        agent = Agent.me()
        console = Console()
        agent_info_table = Table()
        agent_info_table.add_column("AccountId")
        agent_info_table.add_column("symbol")
        agent_info_table.add_column("headquarters")
        agent_info_table.add_column("credits")
        agent_info_table.add_column("startingFaction")
        agent_info_table.add_row(
            agent.accountId,
            agent.symbol,
            agent.headquarters,
            f"${agent.credits}",
            agent.startingFaction,
        )
        console.print(agent_info_table)
