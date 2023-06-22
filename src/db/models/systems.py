import enum
from datetime import datetime
from typing import Any, Dict, List, Self
from uuid import UUID, uuid4

from sqlalchemy import orm

from src.db import get_db
from src.db.base_class import Base
from src.support.datetime import utc_now

from .waypoints import MappedEnum


class SystemMappingMappedEnum(enum.StrEnum):
    # It is free to claim by any explorer
    UN_MAPPED = "un_mapped"
    # It has been claimed by an explorer but not visited yet
    INCOMPLETE = "incomplete"
    # An explorer has visited and recorded what is here in the db.
    MAPPED = "mapped"


class SystemMappingStatusModel(Base):
    """
    Stores information about who mapped what
    """

    __tablename__ = "systems_mapping"

    id: orm.Mapped[UUID] = orm.mapped_column(primary_key=True, default=uuid4)
    symbol: orm.Mapped[str]
    mapped: orm.Mapped[SystemMappingMappedEnum]
    ship_symbol: orm.Mapped[str] = orm.mapped_column(index=True)
    date_time: orm.Mapped[datetime] = orm.mapped_column(default=utc_now())

    @classmethod
    def set_mapping(cls, symbol: str, mapped: MappedEnum, ship_symbol: str) -> None:
        with get_db() as db:
            already_exists = cls.in_progress_for_ship(ship_symbol=ship_symbol).filter(
                cls.symbol == symbol, cls.mapped == mapped
            )
            if already_exists.count() == 1:
                return
            sm = cls(symbol=symbol, mapped=mapped, ship_symbol=ship_symbol)
            db.add(sm)
            db.commit()

    @classmethod
    def in_progress_for_ship(cls, ship_symbol: str) -> List[Self]:
        """
        Get any in progress mappings for a ship.
        Useful when scripts crash!
        """
        with get_db() as db:
            results = db.query(cls).filter(
                cls.ship_symbol == ship_symbol,
                cls.mapped == SystemMappingMappedEnum.INCOMPLETE,
            )
        return results


class SystemModel(Base):
    __tablename__ = "systems"

    symbol: orm.Mapped[str] = orm.mapped_column(primary_key=True, index=True)
    sectorSymbol: orm.Mapped[str]
    type: orm.Mapped[str]
    x: orm.Mapped[int]
    y: orm.Mapped[int]
    waypoints: orm.Mapped[List[Dict[str, Any]]]
    factions: orm.Mapped[List[Dict[str, Any]]]
    mapped: orm.Mapped[MappedEnum] = orm.mapped_column(default=MappedEnum.UN_MAPPED)
