from typing import Dict, List, Optional, Self, Union

import attrs
from sqlalchemy import update

from src.api import PATHS, client, safe_get, sync_get
from src.db import get_db
from src.db.models.systems import SystemMappingStatusModel, SystemModel
from src.db.models.waypoints import MappedEnum
from src.schemas.errors import Error

from .factions import FactionSummary
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
    factions: List[FactionSummary]
    mapped: Optional[MappedEnum] = MappedEnum.UN_MAPPED

    def save(self, mapped: Optional[MappedEnum] = MappedEnum.UN_MAPPED) -> None:
        """
        Persist in the database
        """
        model = SystemModel(
            sectorSymbol=self.sectorSymbol,
            symbol=self.symbol,
            mapped=mapped,
            waypoints=[attrs.asdict(w) for w in self.waypoints],
            type=self.type,
            x=self.x,
            y=self.y,
            factions=[attrs.asdict(f) for f in self.factions],
        )

        with get_db() as db:
            db.add(model)
            db.commit()

    def mapping_in_progress(self, ship_symbol: str) -> None:
        with get_db() as db:
            db.execute(
                update(SystemModel)
                .where(SystemModel.symbol == self.symbol)
                .values(mapped=MappedEnum.INCOMPLETE)
            )
            SystemMappingStatusModel.set_mapping(
                symbol=self.symbol,
                mapped=MappedEnum.INCOMPLETE,
                ship_symbol=ship_symbol,
            )
            db.commit()
        self.mapped = MappedEnum.INCOMPLETE

    def mapping_complete(self, ship_symbol: str) -> None:
        with get_db() as db:
            db.execute(
                update(SystemModel)
                .where(
                    SystemModel.symbol == self.symbol,
                    SystemModel.mapped == MappedEnum.INCOMPLETE,
                )
                .values(mapped=MappedEnum.MAPPED)
            )
            SystemMappingStatusModel.set_mapping(
                symbol=self.symbol,
                mapped=MappedEnum.MAPPED,
                ship_symbol=ship_symbol,
            )
            db.commit()
        self.mapped = MappedEnum.MAPPED

    @classmethod
    def from_db(cls, symbol: str) -> Optional[Self]:
        """
        Get a persisted instance of this from the database, if one exists.
        """
        with get_db() as db:
            system_model: SystemModel = (
                db.query(SystemModel).filter(SystemModel.symbol == symbol).one_or_none()
            )

        if system_model:
            data = system_model.__dict__
            data.pop("_sa_instance_state")
            return cls.build(data)
        return None

    @classmethod
    def build(cls, data: Dict) -> Self:
        waypoints = [WaypointSummary(**x) for x in data.pop("waypoints")]
        factions = [FactionSummary(**f) for f in data.pop("factions")]
        return cls(**data, waypoints=waypoints, factions=factions)

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        db_result = cls.from_db(symbol=symbol)
        if db_result:
            return db_result
        result = await safe_get(path=PATHS.system(symbol))
        match result:
            case dict():
                api_result = cls.build(result)
                api_result.save()
                return api_result
            case _:
                return result
            
    @classmethod
    def sync_get(cls, symbol: str) -> Union[Self, Error]:
        db_result = cls.from_db(symbol=symbol)
        if db_result:
            return db_result
        result = sync_get(path=PATHS.system(symbol))
        match result:
            case dict():
                api_result = cls.build(result)
                api_result.save()
                return api_result
            case _:
                return result


@attrs.define
class JumpGateSystem:
    factionSymbol: str
    symbol: str
    sectorSymbol: str
    type: str
    x: int
    y: int
    distance: int

    @classmethod
    def build(cls, data: Dict) -> Self:
        return cls(**data)


@attrs.define
class JumpGate:
    jumpRange: int
    factionSymbol: str
    connectedSystems: List[JumpGateSystem]

    @classmethod
    def build(cls, data: Dict) -> Self:
        connected_systems = [
            JumpGateSystem.build(x) for x in data.pop("connectedSystems")
        ]
        return cls(**data, connectedSystems=connected_systems)

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.jumpgate(symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
            
    @classmethod
    def sync_get(cls, symbol: str) -> Union[Self, Error]:
        result = sync_get(path=PATHS.jumpgate(symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
