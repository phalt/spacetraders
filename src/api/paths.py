import attrs

BASE_PATH = "https://api.spacetraders.io/v2"


@attrs.define
class Paths:
    """
    All paths for the API should be stored here.
    Static paths should be hard coded constants.
    Generated paths should be functions.
    """

    REGISTER: str = f"{BASE_PATH}/register"
    AGENT: str = f"{BASE_PATH}/my/agent"
    SHIPS: str = f"{BASE_PATH}/my/ships"
    CONTRACTS: str = f"{BASE_PATH}/my/contracts"

    def ship(self, symbol: str) -> str:
        """
        Generate API path for a specific ship
        """
        return f"{BASE_PATH}/my/ships/{symbol}"

    def system_waypoints(self, symbol: str) -> str:
        """
        Generate the API path for system_waypoints.
        """
        parts = symbol.split("-")
        system = "-".join(parts[:2])
        return f"{BASE_PATH}/systems/{system}/waypoints"

    def waypoint(self, symbol: str) -> str:
        """
        Generate the API path for a waypoint.
        """
        waypoint = symbol
        return f"{self.system_waypoints(symbol=symbol)}/{waypoint}"

    def shipyard(self, symbol: str) -> str:
        """
        Generate the API path for a shipyard
        """
        return f"{self.waypoint(symbol=symbol)}/shipyard"

    def accept_contract(self, contract_id: str) -> str:
        """
        Generate the API path for accepting a contract.
        """
        return f"{BASE_PATH}/my/contracts/{contract_id}/accept"


PATHS = Paths()
