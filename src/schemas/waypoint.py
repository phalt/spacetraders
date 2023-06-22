from typing import Any, Dict, List, Optional, Self, Union

import attrs
from sqlalchemy import update

from src.api import PATHS, safe_get
from src.db import get_db
from src.db.models.charts import ChartModel
from src.db.models.waypoints import MappedEnum, WaypointModel
from src.schemas.errors import Error
from src.schemas.markets import Market
from src.support.datetime import DateTime


@attrs.define
class WaypointFaction:
    symbol: str


@attrs.define
class Chart:
    submittedBy: str
    submittedOn: DateTime
    waypointSymbol: Optional[str] = None

    def asdict(self) -> Dict:
        return dict(
            submittedBy=self.submittedBy,
            submittedOn=self.submittedOn.raw,
            waypointSymbol=self.waypointSymbol,
        )

    @classmethod
    def build(cls, data: Dict) -> Self:
        return cls(
            waypointSymbol=data.get("waypointSymbol", None),
            submittedBy=data.get("submittedBy"),
            submittedOn=DateTime.build(data.get("submittedOn")),
        )

    @classmethod
    def save(self) -> Optional[Self]:
        """
        Save this chart to the database.
        """
        chart_model = ChartModel(
            waypointSymbol=self.waypointSymbol,
            submittedBy=self.submittedBy,
            submittedOn=self.submittedOn.raw,
        )

        with get_db() as db:
            db.add(chart_model)
            db.commit()


@attrs.define
class Trait:
    symbol: str
    name: str
    description: str
    shipyard: Optional["Shipyard"] = None


@attrs.define
class Orbital:
    symbol: str


@attrs.define
class WaypointSummary:
    symbol: str
    type: str
    x: int
    y: int


@attrs.define
class Waypoint:
    systemSymbol: str
    symbol: str
    type: str
    x: int
    y: int
    orbitals: List[Orbital]
    traits: List[Trait]
    chart: Chart
    faction: WaypointFaction
    mapped: Optional[MappedEnum] = MappedEnum.UN_MAPPED

    def save(self, mapped: Optional[MappedEnum] = MappedEnum.UN_MAPPED) -> None:
        """
        Persist in the database
        """
        model = WaypointModel(
            systemSymbol=self.systemSymbol,
            symbol=self.symbol,
            mapped=mapped,
            traits=[attrs.asdict(t) for t in self.traits],
            orbitals=[attrs.asdict(o) for o in self.orbitals],
            type=self.type,
            x=self.x,
            y=self.y,
            faction=attrs.asdict(self.faction),
            chart=self.chart.asdict(),
        )

        with get_db() as db:
            db.add(model)
            db.commit()

    def set_mapped(self) -> None:
        with get_db() as db:
            db.execute(
                update(WaypointModel)
                .where(WaypointModel.symbol == self.symbol)
                .values(mapped=MappedEnum.MAPPED)
            )
            db.commit()
        self.mapped = MappedEnum.MAPPED

    @classmethod
    def from_db(cls, symbol: str) -> Optional[Self]:
        """
        Get a persisted instance of this from the database, if one exists.
        """
        with get_db() as db:
            waypoint_model: WaypointModel = (
                db.query(WaypointModel)
                .filter(WaypointModel.symbol == symbol)
                .one_or_none()
            )

        if waypoint_model:
            data = waypoint_model.__dict__
            data.pop("_sa_instance_state")
            return cls.build(data)
        return None

    async def can_refuel(self) -> bool:
        """
        True if this Waypoint has a market place and that
        market place sells fuel
        """
        has_market_place = any([t.symbol == "MARKETPLACE" for t in self.traits])
        if has_market_place:
            marketplace = await Market.get(self.symbol)
            if isinstance(marketplace, Market):
                # Note we use tradeGoods because we should be at this location to see them.
                sells_fuel = any([c.symbol == "FUEL" for c in marketplace.tradeGoods])
                return sells_fuel
        return False

    @classmethod
    def build(cls, data: Dict) -> Self:
        orbitals = [Orbital(**x) for x in data.pop("orbitals")]
        traits = []
        chart = Chart.build(data.pop("chart"))
        faction = WaypointFaction(**data.pop("faction"))
        for trait_data in data.pop("traits", []):
            trait = Trait(**trait_data)
            if trait.symbol == "SHIPYARD":
                result = Shipyard.get(symbol=data["symbol"])
                match result:
                    case Shipyard():
                        trait.shipyard = result
            traits.append(trait)
        return cls(
            **data, orbitals=orbitals, traits=traits, chart=chart, faction=faction
        )

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        db_result = cls.from_db(symbol=symbol)
        if db_result:
            return db_result
        else:
            result = await safe_get(path=PATHS.waypoint(symbol=symbol))
            match result:
                case dict():
                    api_result = cls.build(result)
                    api_result.save()
                    return api_result
                case _:
                    return result


@attrs.define
class Shipyard:
    """
    A Shipyard is available if a Waypoint has a Trait that is
    SHIPYARD
    """

    symbol: str
    shipTypes: List[Dict[str, str]]
    transactions: List[Dict[str, Union[str, int]]]
    ships: List[Dict[str, Any]]

    @classmethod
    def build(cls, data: Dict) -> Self:
        return cls(**data)

    @classmethod
    async def get(cls, symbol: str) -> Union[Self, Error]:
        result = await safe_get(path=PATHS.shipyard(symbol=symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
