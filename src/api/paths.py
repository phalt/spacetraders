import attrs

BASE_PATH = "https://api.spacetraders.io/v2"


@attrs.define
class Paths:
    """
    All paths for the API should be stored here
    """

    REGISTER: str = f"{BASE_PATH}/register"
    AGENT: str = f"{BASE_PATH}/my/agent"


PATHS = Paths()
