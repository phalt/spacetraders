from typing import Self, Union, Optional
import attrs

from .waypoint import Waypoint

from src.api import PATHS, bare_client, safe_get
from src.api.utils import data_or_error
from .contracts import Contract
from .ships import Ship
from .factions import Faction
from .errors import Error


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
    def me(cls) -> Union[Self, Error]:
        """
        Returns the "you" version of an Agent
        """
        result = safe_get(path=PATHS.MY_AGENT)
        match result:
            case dict():
                return cls(**result)
            case _:
                return result

    def headquarters_info(self) -> Waypoint:
        result = Waypoint.get(self.headquarters)
        match result:
            case Waypoint():
                return result


@attrs.define
class AgentManager:
    token: str
    agent: Agent
    contract: Contract
    faction: Faction
    ship: Ship

    @classmethod
    def register_new(
        cls, symbol: str, faction: str, email: Optional[str] = None
    ) -> Union[Self, Error]:
        api_response = bare_client.post(
            PATHS.REGISTER, data={"symbol": symbol, "faction": faction, "email": email}
        )
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return cls(
                    token=result["token"],
                    agent=Agent(**result["agent"]),
                    contract=Contract.build(result["contract"]),
                    faction=Faction(**result["faction"]),
                    ship=Ship.build(result["ship"]),
                )
            case _:
                return result
