from typing import Any, Dict, List

from sqlalchemy import orm

from src.db.base_class import Base


class SurveyModel(Base):
    __tablename__ = "surveys"

    signature: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    symbol: orm.Mapped[str]
    deposits: orm.Mapped[List[Dict[str, Any]]]
    expiration: orm.Mapped[str]
    size: orm.Mapped[str]
