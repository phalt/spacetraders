from typing import Any, Dict, List, Optional, Self, Union

import attrs

from src.api import PATHS, safe_get
from src.schemas.errors import Error
from src.schemas.markets import Market


@attrs.define
class WaypointFaction:
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
class WaypointSummary:
    symbol: str
    type: str
    x: int
    y: int


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
    faction: WaypointFaction

    async def can_refuel(self) -> bool:
        """
        True if this Waypoint has a market place and that
        market place sells fuel
        """
        has_market_place = any([t.symbol == "MARKETPLACE" for t in self.traits])
        if has_market_place:
            marketplace = await Market.get(self.symbol)
            # Note we use tradeGoods because we should be at this location to see them.
            sells_fuel = any([c.symbol == "FUEL" for c in marketplace.tradeGoods])
            return sells_fuel

    @classmethod
    def build(cls, data: Dict) -> Self:
        orbitals = [Orbital(**x) for x in data.pop("orbitals")]
        traits = []
        for trait_data in data.pop("traits", []):
            trait = Trait(**trait_data)
            if trait.symbol == "SHIPYARD":
                result = Shipyard.get(symbol=data["symbol"])
                match result:
                    case Shipyard():
                        trait.shipyard = result
            traits.append(trait)
        return cls(**data, orbitals=orbitals, traits=traits)

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.waypoint(symbol=symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result


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
    async def get(cls, symbol: str) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.shipyard(symbol=symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
