from typing import List, Dict, Self, Union, Any
import attrs

from cachetools import cached

from src.settings import cache
from src.api import client, PATHS


@attrs.define
class Cargo:
    capacity: int
    units: 0
    inventory: List[Dict[str, int]]

@attrs.define
class Registration:
    name: str
    factionSymbol: str
    role: str
@attrs.define
class Ship:
    registration: Registration
    cargo: Cargo

    @classmethod
    def build(cls, data: str) -> Self:
        registration = Registration(**data['registration'])
        cargo = Cargo(**data['cargo'])

        return cls(
            registration=registration,
            cargo=cargo
        )

    @classmethod
    @cached(cache)
    def get(cls, symbol: str) -> Self:
        api_result = client.get(PATHS.ship(symbol=symbol))
        api_result.raise_for_status()
        return cls.build(api_result.json()['data'])

@attrs.define
class ShipsManager:
    total: int
    page: int
    limit: int
    ships: List[Ship] = []

    @classmethod
    @cached(cache)
    def all(cls) -> Self:
        api_result = client.get(PATHS.SHIPS)
        api_result.raise_for_status()
        from rich.pretty import pprint
        pprint(api_result.json())
        meta = api_result.json()['meta']
        return cls(
            total=meta['total'],
            page=meta['page'],
            limit=meta['limit']
        )
