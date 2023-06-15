from typing import List, Dict, Self
import attrs

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
        traits = ([Trait(**x) for x in data.pop("traits")],)

        return cls(**data, orbitals=orbitals, traits=traits)

    @staticmethod
    def get(symbol: str) -> Self:
        print(PATHS.waypoint(symbol=symbol))
        api_result = client.get(PATHS.waypoint(symbol=symbol))
        return Waypoint.build(api_result.json()["data"])
