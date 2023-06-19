from typing import Any, Dict, Optional

import attrs


@attrs.define
class Error:
    message: str
    code: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
