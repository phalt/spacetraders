from typing import List, Dict, Self, Union
import attrs

from src.api import PATHS, safe_get

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
        result = safe_get(path=PATHS.MY_FACTIONS)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result

    @classmethod
    def all(cls) -> Union[Self, Error]:
        result = safe_get(path=PATHS.FACTIONS)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result
