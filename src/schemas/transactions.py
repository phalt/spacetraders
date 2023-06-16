import attrs


@attrs.define
class Transaction:
    waypointSymbol: str
    shipSymbol: str
    tradeSymbol: str
    type: str
    units: int
    pricePerUnit: int
    totalPrice: int
    timestamp: str
