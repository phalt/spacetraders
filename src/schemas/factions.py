from typing import List, Dict, Self, Union
import attrs

from src.api import client, PATHS
from src.api.utils import data_or_error

from .errors import Error


@attrs.define
class Faction:
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[Dict[str, str]]
    isRecruiting: bool


@attrs.define
class FactionsManager:
    factions: List[Faction]

    @classmethod
    def mine(cls) -> Union[Self, Error]:
        api_response = client.get(PATHS.MY_FACTIONS)
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result

    @classmethod
    def all(cls) -> Union[Self, Error]:
        api_response = client.get(PATHS.FACTIONS)
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result
