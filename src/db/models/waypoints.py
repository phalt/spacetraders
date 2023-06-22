import enum
from typing import Any, Dict, List

from sqlalchemy import orm

from src.db.base_class import Base


class MappedEnum(enum.StrEnum):
    # It is free to claim by any explorer
    UN_MAPPED = "un_mapped"
    # It has been claimed by an explorer but not visited yet
    INCOMPLETE = "incomplete"
    # An explorer has visited and recorded what is here in the db.
    MAPPED = "mapped"


class WaypointModel(Base):
    __tablename__ = "waypoints"

    systemSymbol: orm.Mapped[str]
    symbol: orm.Mapped[str] = orm.mapped_column(primary_key=True, index=True)
    mapped: orm.Mapped[MappedEnum] = orm.mapped_column(default=MappedEnum.UN_MAPPED)
    # The traits at this waypoint.
    traits: orm.Mapped[List[Dict[str, Any]]]
    orbitals: orm.Mapped[List[Dict[str, Any]]]
    type: orm.Mapped[str]
    x: orm.Mapped[int]
    y: orm.Mapped[int]
    faction: orm.Mapped[Dict[str, Any]]
    chart: orm.Mapped[Dict[str, Any]]
