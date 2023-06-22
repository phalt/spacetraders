import attrs

BASE_PATH = "https://api.spacetraders.io/v2"


@attrs.define
class Paths:
    """
    All paths for the API should be stored here.
    Static paths should be hard coded constants.
    Generated paths should be functions.
    """

    SERVER_STATUS: str = BASE_PATH
    REGISTER: str = f"{BASE_PATH}/register"
    MY_AGENT: str = f"{BASE_PATH}/my/agent"
    MY_SHIPS: str = f"{BASE_PATH}/my/ships"
    MY_CONTRACTS: str = f"{BASE_PATH}/my/contracts"
    MY_FACTIONS: str = f"{BASE_PATH}/my/factions"
    FACTIONS: str = f"{BASE_PATH}/factions"

    def contract(self, contract_id: str) -> str:
        return f"{self.MY_CONTRACTS}/{contract_id}"

    def ship(self, symbol: str) -> str:
        """
        Generate API path for a specific ship
        """
        return f"{BASE_PATH}/my/ships/{symbol}"

    def ship_nav(self, symbol: str) -> str:
        """
        API path for ship nav status
        """
        return f"{self.ship(symbol=symbol)}/nav"

    def ship_cargo(self, symbol: str) -> str:
        """
        API path for ship cargo status
        """
        return f"{self.ship(symbol=symbol)}/cargo"

    def ship_navigate(self, symbol: str) -> str:
        """
        API path for making a ship navigate to a waypoint
        """
        return f"{self.ship(symbol=symbol)}/navigate"

    def ship_orbit(self, symbol: str) -> str:
        """
        API path to put ship into orbit
        """
        return f"{self.ship(symbol=symbol)}/orbit"

    def ship_dock(self, symbol: str) -> str:
        """
        API path to dock ship
        """
        return f"{self.ship(symbol=symbol)}/dock"

    def ship_refuel(self, symbol: str) -> str:
        """
        API path to refuel ship
        """
        return f"{self.ship(symbol=symbol)}/refuel"

    def ship_sell(self, symbol: str) -> str:
        """
        API path to sell stuff
        """
        return f"{self.ship(symbol=symbol)}/sell"

    def ship_jump(self, symbol: str) -> str:
        """
        API path to jump ship
        """
        return f"{self.ship(symbol=symbol)}/jump"

    def ship_extract(self, symbol: str) -> str:
        """
        API path to perform mining extraction
        """
        return f"{self.ship(symbol=symbol)}/extract"

    def ship_survey(self, symbol: str) -> str:
        """
        API path to perform surveying
        """
        return f"{self.ship(symbol=symbol)}/survey"

    def ship_chart(self, symbol: str) -> str:
        """
        API path to perform charting
        """
        return f"{self.ship(symbol=symbol)}/chart"

    def ship_negotiate_contract(self, symbol: str) -> str:
        """
        API path to perform negotiation of a contract
        """
        return f"{self.ship(symbol=symbol)}/negotiate/contract"

    def system_waypoints(self, symbol: str) -> str:
        """
        Generate the API path for system_waypoints.
        """
        parts = symbol.split("-")
        system = "-".join(parts[:2])
        return f"{BASE_PATH}/systems/{system}/waypoints"

    def system(self, symbol: str) -> str:
        """
        Generate the API path for a system.
        """
        return f"{BASE_PATH}/systems/{symbol}"

    def waypoint(self, symbol: str) -> str:
        """
        Generate the API path for a waypoint.
        """
        waypoint = symbol
        return f"{self.system_waypoints(symbol=symbol)}/{waypoint}"

    def jumpgate(self, symbol: str) -> str:
        """
        Generate the API path for a jumpgate.
        """
        return f"{self.waypoint(symbol=symbol)}/jump-gate"

    def shipyard(self, symbol: str) -> str:
        """
        Generate the API path for a shipyard
        """
        return f"{self.waypoint(symbol=symbol)}/shipyard"

    def market(self, symbol: str) -> str:
        """
        Generate the API path for a market
        """
        return f"{self.waypoint(symbol=symbol)}/market"

    def contract_accept(self, contract_id: str) -> str:
        """
        Generate the API path for accepting a contract.
        """
        return f"{BASE_PATH}/my/contracts/{contract_id}/accept"

    def contract_fulfill(self, contract_id: str) -> str:
        """
        Generate the API path for fulfilling a contract.
        """
        return f"{BASE_PATH}/my/contracts/{contract_id}/fulfill"

    def contract_deliver(self, contract_id: str) -> str:
        """
        Generate the API path for delivering on a contract.
        """
        return f"{BASE_PATH}/my/contracts/{contract_id}/deliver"


PATHS = Paths()
