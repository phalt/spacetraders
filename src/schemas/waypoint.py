from typing import List, Dict, Self, Optional, Union, Any
import attrs

from cachetools import cached

from src.settings import cache
from src.api import client, PATHS


@attrs.define
class Faction:
    symbol: str


@attrs.define
class Chart:
    submittedBy: str
    submittedOn: str


@attrs.define
class Trait:
    symbol: str
    name: str
    description: str
    shipyard: Optional["Shipyard"] = None


@attrs.define
class Orbital:
    symbol: str


@attrs.define
class Waypoint:
    systemSymbol: str
    symbol: str
    type: str
    x: int
    y: int
    orbitals: List[Orbital]
    traits: List[Trait]
    chart: Chart
    faction: Faction

    @classmethod
    def build(cls, data: Dict) -> Self:
        orbitals = [Orbital(**x) for x in data.pop("orbitals")]
        traits = []
        for trait_data in data.pop("traits", []):
            trait = Trait(**trait_data)
            if trait.symbol == "SHIPYARD":
                trait.shipyard = Shipyard.get(symbol=data["symbol"])
            traits.append(trait)
        return cls(**data, orbitals=orbitals, traits=traits)

    @classmethod
    @cached(cache)
    def get(cls, symbol: str) -> Self:
        api_result = client.get(PATHS.waypoint(symbol=symbol))
        api_result.raise_for_status()
        return cls.build(api_result.json()["data"])

    def refresh(self) -> Self:
        api_result = client.get(PATHS.waypoint(symbol=self.symbol))
        api_result.raise_for_status()
        return self.build(api_result.json()["data"])


@attrs.define
class Shipyard:
    """
    A Shipyard is available if a Waypoint has a Trait that is
    SHIPYARD
    """

    symbol: str
    shipTypes: List[Dict[str, str]]
    transactions: List[Dict[str, Union[str, int]]]
    ships: List[Dict[str, Any]]

    @classmethod
    def build(cls, data: Dict) -> Self:
        return cls(**data)

    @classmethod
    @cached(cache)
    def get(cls, symbol: str) -> Self:
        api_result = client.get(PATHS.shipyard(symbol=symbol))
        api_result.raise_for_status()
        return cls.build(api_result.json()["data"])
