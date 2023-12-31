from typing import Dict, List, Self, Union

import attrs

from src.api import PATHS, safe_get

from .errors import Error

@attrs.define
class FactionSummary:
    symbol: str

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
    async def mine(cls) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.MY_FACTIONS)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result

    @classmethod
    async def all(cls) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.FACTIONS)
        match result:
            case dict():
                return cls(factions=[Faction(**x) for x in result])
            case _:
                return result
