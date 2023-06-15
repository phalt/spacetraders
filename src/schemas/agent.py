from typing import Self
import attrs

from .waypoint import Waypoint

from src.api import client, PATHS


@attrs.define
class Agent:
    def __str__(self):
        return f":man_astronaut: {self.accountId} - {self.symbol}"

    accountId: str
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str

    @classmethod
    def me(cls) -> Self:
        """
        Returns the "you" version of an Agent
        """
        api_response = client.get(PATHS.AGENT)
        api_response.raise_for_status()
        return cls(**api_response.json()["data"])

    def headquarters_info(self) -> Waypoint:
        return Waypoint.get(self.headquarters)
