import attrs

BASE_PATH = "https://api.spacetraders.io/v2"


@attrs.define
class Paths:
    """
    All paths for the API should be stored here
    """

    REGISTER: str = f"{BASE_PATH}/register"
    AGENT: str = f"{BASE_PATH}/my/agent"

    def waypoint(self, symbol) -> str:
        """
        Generate the API path for a waypoint.
        """
        parts = symbol.split("-")
        system = "-".join(parts[:2])
        waypoint = symbol
        return f"{BASE_PATH}/systems/{system}/waypoints/{waypoint}"


PATHS = Paths()
