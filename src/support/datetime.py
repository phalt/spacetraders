from datetime import datetime
from typing import Self

import attrs
import pytz

from src.settings import config


@attrs.define
class DateTime:
    """
    My own datetime logic because I hate myself
    """

    raw: str
    utc_time: datetime
    local_time: datetime

    @classmethod
    def build(cls, datetime_string: str) -> Self:
        utc_time = datetime.fromisoformat(datetime_string)
        tz = config.get("time", "zone")
        local_timezone = utc_time.astimezone(tz=pytz.timezone(tz))
        return cls(raw=datetime_string, utc_time=utc_time, local_time=local_timezone)
