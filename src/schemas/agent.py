import attrs


@attrs.define
class Agent:
    accountId: str
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
