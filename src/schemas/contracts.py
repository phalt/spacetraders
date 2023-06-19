from typing import Dict, List, Self, Union

import attrs
from structlog import get_logger

from src.api import PATHS, client, safe_get, safe_post

from .errors import Error
from .ships import Cargo

log = get_logger(__name__)


@attrs.define
class Term:
    """
    Represents the terms and conditions of a contract
    """

    deadline: str
    payment: Dict[str, int]
    deliver: List[Dict]


@attrs.define
class Contract:
    """
    A single contract
    """

    id: str
    factionSymbol: str
    type: str
    terms: Term
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str

    @classmethod
    def get(cls, contract_id: str) -> Union[Self, Error]:
        result = safe_get(path=PATHS.contract(contract_id=contract_id))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result

    @classmethod
    def build(cls, data) -> Self:
        terms = Term(**data.pop("terms"))
        return cls(**data, terms=terms)

    def fulfill(self) -> Union[Dict, Error]:
        """
        Fullfills a contract.
        """
        from .agent import Agent

        result = safe_post(path=PATHS.contract_fulfill(self.id))
        match result:
            case dict():
                self.fulfilled = True
                return dict(
                    contract=Contract.build(result["contract"]),
                    agent=Agent(**result["agent"]),
                )
            case _:
                return result

    def accept(self) -> Union[Dict, Error]:
        """
        Accepts a contract if it has not been accepted yet.
        """
        from .agent import Agent

        result = safe_post(path=PATHS.contract_accept(self.id))
        match result:
            case dict():
                self.accepted = True
                return dict(
                    contract=Contract.build(result["contract"]),
                    agent=Agent(**result["agent"]),
                )
            case _:
                return result

    def deliver(
        self, ship_symbol: str, trade_symbol: str, amount: int
    ) -> Union[Dict, Error]:
        result = safe_post(
            path=PATHS.contract_deliver(self.id),
            data={
                "shipSymbol": ship_symbol,
                "tradeSymbol": trade_symbol,
                "units": amount,
            },
        )
        match result:
            case dict():
                return dict(
                    contract=Contract.build(result["contract"]),
                    cargo=Cargo(**result["cargo"]),
                )
            case _:
                return result


@attrs.define
class ContractManager:
    """
    Represents all the contracts available to you.
    """

    total: int
    page: int
    limit: int
    contracts: List[Contract]

    @classmethod
    def all(cls) -> Self:
        """
        Returns all contracts available to use
        """
        api_response = client.get(PATHS.MY_CONTRACTS)
        api_response.raise_for_status()
        meta = api_response.json()["meta"]
        contracts = [Contract.build(x) for x in api_response.json()["data"]]
        return cls(
            total=meta["total"],
            page=meta["page"],
            limit=meta["limit"],
            contracts=contracts,
        )
