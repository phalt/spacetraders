from typing import List, Dict, Self, Optional, Any, Union, TYPE_CHECKING
import attrs

from cachetools import cached

from src.settings import cache
from src.api import client, PATHS
from src.api.utils import data_or_error

from .nav import Nav
from .errors import Error
from .transactions import Transaction
from .mining import Extraction
from .generic import Cooldown

if TYPE_CHECKING:
    pass


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

    def navigation_status(self) -> Union[Nav, Error]:
        api_response = client.get(PATHS.ship_nav(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return Nav(**result)
            case _:
                return result

    def cargo_status(self) -> Union[Cargo, Error]:
        api_response = client.get(PATHS.ship_cargo(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return Cargo(**result)
            case _:
                return result

    def navigate(self, waypoint: str) -> Union[Nav, Error]:
        """
        Navigate to a waypoint.
        """
        api_response = client.post(
            PATHS.ship_navigate(self.symbol), data={"waypointSymbol": waypoint}
        )
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return Nav(**result["nav"])
            case _:
                return result

    def orbit(self) -> Union[Nav, Error]:
        """
        Put ship in orbit
        """
        api_response = client.post(PATHS.ship_orbit(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return Nav(**result["nav"])
            case _:
                return result

    def dock(self) -> Union[Nav, Error]:
        """
        Dock ship
        """
        api_response = client.post(PATHS.ship_dock(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return Nav(**result["nav"])
            case _:
                return result

    def refuel(self) -> Union[Dict, Error]:
        """
        Refuel ship
        """
        from .agent import Agent

        api_response = client.post(PATHS.ship_refuel(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return dict(
                    agent=Agent(**result["agent"]),
                    fuel=Fuel(**result["fuel"]),
                    transaction=Transaction(**result["transaction"]),
                )
            case _:
                return result

    def extract(self) -> Union[Dict, Error]:
        """
        Perform mining extraction at the current waypoint.
        """
        api_response = client.post(PATHS.ship_extract(self.symbol))
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                yield_ = result["extraction"].pop("yield")
                return dict(
                    extraction=Extraction(**result["extraction"], yield_=yield_),
                    cooldown=Cooldown(**result["cooldown"]),
                    cargo=Cargo(**result["cargo"]),
                )
            case _:
                return result

    def sell(self, symbol: str, amount: int) -> Union[Dict, Error]:
        """
        Sell some items in cargo.
        """
        from .agent import Agent

        api_response = client.post(
            PATHS.ship_sell(self.symbol), data={"symbol": symbol, "units": amount}
        )
        result = data_or_error(api_response=api_response)
        match result:
            case dict():
                return dict(
                    agent=Agent(**result["agent"]),
                    cargo=Cargo(**result["cargo"]),
                    transaction=Transaction(**result["transaction"]),
                )
            case _:
                return result


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

    @staticmethod
    def buy_ship(ship_type: str, waypoint_symbol: str) -> Union[Ship, Error]:
        """
        Purchase a ship
        """
        post_data = dict(shipType=ship_type, waypointSymbol=waypoint_symbol)
        api_result = client.post(PATHS.SHIPS, data=post_data)
        result = data_or_error(api_result)
        match result:
            case dict():
                return Ship(**result["ship"])
            case _:
                return result
