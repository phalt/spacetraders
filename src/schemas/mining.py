from typing import Dict
import attrs


@attrs.define
class Extraction:
    """
    The result of a mining operation
    """

    shipSymbol: str
    yield_: Dict
