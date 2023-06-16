import attrs

@attrs.define
class Cooldown:
    """
    Usually as a result of mining
    """
    shipSymbol: str
    totalSeconds: int
    remainingSeconds: int
    expiration: str
