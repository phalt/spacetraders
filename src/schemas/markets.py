from typing import List, Dict, Self, Union
import attrs

from .transactions import Transaction
from src.api import PATHS, safe_get
from .errors import Error


@attrs.define
class TradeGood:
    symbol: str
    tradeVolume: int
    supply: str
    purchasePrice: int
    sellPrice: int


@attrs.define
class Commodity:
    symbol: str
    name: str
    description: str


@attrs.define
class Market:
    symbol: str
    marketImports: List[Commodity]
    marketExports: List[Commodity]
    exchange: List[Commodity]
    transactions: List[Transaction]
    tradeGoods: List[TradeGood]

    @classmethod
    def build(cls, data: Dict) -> Self:
        market_imports = [Commodity(**x) for x in data["imports"]]
        market_exports = [Commodity(**x) for x in data["exports"]]
        exchange = [Commodity(**x) for x in data["exchange"]]
        transactions = [Transaction(**x) for x in data.get("transactions", [])]
        trade_goods = [TradeGood(**x) for x in data.get("tradeGoods", [])]
        return cls(
            symbol=data["symbol"],
            marketImports=market_imports,
            marketExports=market_exports,
            exchange=exchange,
            transactions=transactions,
            tradeGoods=trade_goods,
        )

    @classmethod
    def get(cls, symbol: str) -> Union[Self, Error]:
        result = safe_get(path=PATHS.market(symbol=symbol))
        match result:
            case dict():
                return cls.build(result)
            case _:
                return result
