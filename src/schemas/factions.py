from typing import List, Dict
import attrs


@attrs.define
class Faction:
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: List[Dict[str, str]]
    isRecruiting: bool
