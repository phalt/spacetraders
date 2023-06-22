from typing import Any, Dict, Self

import attrs
from structlog import get_logger

log = get_logger(__name__)


@attrs.define
class Route:
    departure: Dict[str, Any]
    destination: Dict[str, Any]
    arrival: str
    departureTime: str


@attrs.define
class Nav:
    systemSymbol: str
    waypointSymbol: str
    route: Route
    status: str
    flightMode: str

    @classmethod
    def build(cls, data: Dict) -> Self:
        route = Route(**data.pop("route"))
        return cls(**data, route=route)
