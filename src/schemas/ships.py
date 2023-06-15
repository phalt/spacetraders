from typing import List, Dict, Self, Optional, Any
import attrs

from cachetools import cached

from src.settings import cache
from src.api import client, PATHS

from .nav import Nav


@attrs.define
class Cargo:
    capacity: int
    units: int
    inventory: List[Dict[str, int]]


@attrs.define
class Registration:
    name: str
    factionSymbol: str
    role: str


@attrs.define
class Module:
    symbol: str
    name: str
    description: str
    requirements: Dict[str, Any]
    range: Optional[int] = None
    capacity: Optional[int] = None


@attrs.define
class Mount:
    symbol: str
    name: str
    description: str
    strength: int
    requirements: Optional[Dict[str, Any]] = None
    deposits: Optional[List[str]] = None


@attrs.define
class Engine:
    symbol: str
    name: str
    description: str
    condition: int
    speed: int
    requirements: Dict[str, Any]


@attrs.define
class Reactor:
    symbol: str
    name: str
    description: str
    condition: int
    powerOutput: int
    requirements: Dict[str, Any]


@attrs.define
class Frame:
    symbol: str
    name: str
    description: str
    moduleSlots: int
    mountingPoints: int
    fuelCapacity: int
    condition: int
    requirements: Dict[str, Any]


@attrs.define
class Fuel:
    current: int
    capacity: int
    consumed: Dict[str, Any]


@attrs.define
class Crew:
    current: int
    capacity: int
    required: int
    rotation: str
    morale: int
    wages: int


@attrs.define
class Ship:
    symbol: str
    nav: Nav
    crew: Crew
    fuel: Fuel
    frame: Frame
    reactor: Reactor
    engine: Engine
    modules: List[Module]
    mounts: List[Mount]
    registration: Registration
    cargo: Cargo

    @classmethod
    def build(cls, data: Dict) -> Self:
        crew = Crew(**data["crew"])
        fuel = Fuel(**data["fuel"])
        engine = Engine(**data["engine"])
        reactor = Reactor(**data["reactor"])
        frame = Frame(**data["frame"])
        registration = Registration(**data["registration"])
        cargo = Cargo(**data["cargo"])
        modules = [Module(**x) for x in data["modules"]]
        mounts = [Mount(**x) for x in data["mounts"]]
        nav = Nav.build(data["nav"])

        return cls(
            symbol=data["symbol"],
            modules=modules,
            mounts=mounts,
            registration=registration,
            cargo=cargo,
            engine=engine,
            reactor=reactor,
            frame=frame,
            fuel=fuel,
            crew=crew,
            nav=nav,
        )

    @classmethod
    @cached(cache)
    def get(cls, symbol: str) -> Self:
        api_result = client.get(url=PATHS.ship(symbol=symbol))
        api_result.raise_for_status()
        return cls.build(api_result.json()["data"])


@attrs.define
class ShipsManager:
    total: int
    page: int
    limit: int
    ships: List[Ship]

    @classmethod
    @cached(cache)
    def all(cls) -> Self:
        api_result = client.get(PATHS.SHIPS)
        api_result.raise_for_status()
        meta = api_result.json()["meta"]
        ships = [Ship(**d) for d in api_result.json()["data"]]
        return cls(
            total=meta["total"], page=meta["page"], limit=meta["limit"], ships=ships
        )
