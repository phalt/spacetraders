from typing import List, Self
import attrs

from cachetools import cached

from src.settings import cache
from src.api import client, PATHS
from .waypoint import Waypoint


@attrs.define
class SystemWaypoints:
    total: int
    page: int
    limit: int
    waypoints: List[Waypoint]

    @classmethod
    @cached(cache)
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
