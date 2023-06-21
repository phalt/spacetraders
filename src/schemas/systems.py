from typing import Dict, List, Self, Union

import attrs

from src.api import PATHS, client, safe_get
from src.schemas.errors import Error

from .waypoint import Waypoint, WaypointSummary


@attrs.define
class SystemWaypoints:
    total: int
    page: int
    limit: int
    waypoints: List[Waypoint]

    @classmethod
    def get(cls, symbol: str) -> Self:
        api_response = client.get(PATHS.system_waypoints(symbol=symbol))
        api_response.raise_for_status()
        meta = api_response.json()["meta"]
        waypoints = [Waypoint(**x) for x in api_response.json()["data"]]

        return cls(
            total=meta["total"],
            page=meta["page"],
            limit=meta["limit"],
            waypoints=waypoints,
        )


@attrs.define
class System:
    symbol: str
    sectorSymbol: str
    type: str
    x: int
    y: int
    waypoints: List[WaypointSummary]
    factions: List[Dict]

    @classmethod
    def build(cls, data: Dict) -> Self:
        waypoints = [WaypointSummary(**x) for x in data.pop("waypoints")]
        return cls(**data, waypoints=waypoints)

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.system(symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
