import attrs

BASE_PATH = "https://api.spacetraders.io/v2"


@attrs.define
class Paths:
    """
    All paths for the API should be stored here
    """

    REGISTER: str = f"{BASE_PATH}/register"
    AGENT: str = f"{BASE_PATH}/my/agent"
    CONTRACTS: str = f"{BASE_PATH}/my/contracts"

    def waypoint(self, symbol: str) -> str:
        """
        Generate the API path for a waypoint.
        """
        parts = symbol.split("-")
        system = "-".join(parts[:2])
        waypoint = symbol
        return f"{BASE_PATH}/systems/{system}/waypoints/{waypoint}"

    def system_waypoints(self, symbol: str) -> str:
        """
        Generate the API path for system_waypoints.
        """
        parts = symbol.split("-")
        system = "-".join(parts[:2])
        return f"{BASE_PATH}/systems/{system}/waypoints"

    def accept_contract(self, contract_id: str) -> str:
        """
        Generate the API path for accepting a contract.
        """
        return f"{BASE_PATH}/my/contracts/{contract_id}/accept"


PATHS = Paths()
