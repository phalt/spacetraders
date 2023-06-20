from typing import Any, Dict, List

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    type_annotation_map = {Dict[str, Any]: JSON, List[Dict[str, Any]]: JSON}
