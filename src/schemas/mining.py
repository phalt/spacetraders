from typing import Dict, List
import attrs


@attrs.define
class Survey:
    """
    A survey result
    """

    signature: str
    symbol: str
    deposits: List[Dict]
    expiration: str
    size: str


@attrs.define
class Extraction:
    """
    The result of a mining operation
    """

    shipSymbol: str
    yield_: Dict
