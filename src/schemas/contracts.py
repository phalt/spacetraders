from typing import Self, List, Dict, Optional, Any
import attrs

from src.api import client, PATHS

from structlog import get_logger

log = get_logger(__name__)


@attrs.define
class Term:
    """
    Represents the terms and conditions of a contract
    """

    deadline: str
    payment: Dict[str, int]
    deliver: Optional[Dict[str, Any]]


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
    def build(cls, data) -> Self:
        terms = Term(**data.pop("terms"))
        return cls(**data, terms=terms)

    def accept(self) -> None:
        """
        Accepts a contract if it has not been accepted yet.
        """

        assert (
            self.accepted is False
        ), "Cannot accept a contract that is already accepted!"

        result = client.post(PATHS.accept_contract(self.id))
        result.raise_for_status()
        log.info(f"Accepted contract {self.id}")
        log.info(result.json())
        self.accepted = True


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
    def get(cls) -> Self:
        """
        Returns all contracts available to use
        """
        api_response = client.get(PATHS.CONTRACTS)
        api_response.raise_for_status()
        meta = api_response.json()["meta"]
        contracts = [Contract.build(x) for x in api_response.json()["data"]]
        return cls(
            total=meta["total"],
            page=meta["page"],
            limit=meta["limit"],
            contracts=contracts,
        )
