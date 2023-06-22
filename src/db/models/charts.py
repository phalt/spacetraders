from sqlalchemy import orm

from src.db.base_class import Base


class ChartModel(Base):
    __tablename__ = "charts"

    waypointSymbol: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    submittedBy: orm.Mapped[str]
    submittedOn: orm.Mapped[str]
