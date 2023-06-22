from typing import Any, Dict, List

from sqlalchemy import orm

from src.db.base_class import Base


class WaypointModel(Base):
    __tablename__ = "waypoints"

    systemSymbol: orm.Mapped[str]
    symbol: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    # Should only be false when a ship has laid claim to visiting it so other ships skip it.
    visited: orm.Mapped[bool] = orm.mapped_column(default=None, nullable=True)
    # The traits at this waypoint.
    traits: orm.Mapped[List[Dict[str, Any]]]
    orbitals: orm.Mapped[List[Dict[str, Any]]]
    type: orm.Mapped[str]
    x: orm.Mapped[int]
    y: orm.Mapped[int]
    faction: orm.Mapped[Dict[str, Any]]
    chart: orm.Mapped[Dict[str, Any]]
