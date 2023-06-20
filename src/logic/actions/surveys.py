from time import sleep
from typing import List

import attrs
from rich.console import Console

from src.schemas.errors import Error
from src.schemas.mining import Survey
from src.schemas.ships import Ship
from src.support.tables import report_result

from .ships import AbstractShipNavigate


@attrs.define
class SurveyDestinationAction(AbstractShipNavigate):
    """
    Will survey a destination in an endless loop.
    """

    ship_symbol: str
    destination: str
    console: Console = Console()
    cargo_sales: int = 0
    expenses: int = 0

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} survey @ {self.destination}"

    def survey(self, ship: Ship) -> Ship:
        """
        Surveys a destination
        """
        result = ship.survey()
        match result:
            case Error():
                report_result(result, Survey)
                cooldown = result.data.get("cooldown")
                if cooldown:
                    sleep(cooldown["remainingSeconds"])
            case dict():
                surveys: List[Survey] = result["surveys"]
                for survey in surveys:
                    report_result(survey, Survey)
                    survey.save()
                cooldown = result["cooldown"].remainingSeconds
                sleep(cooldown)
        return ship

    def process(self):
        self.console.rule(self.name)
        ship = Ship.get(symbol=self.ship_symbol)
        ship = self.navigate_to(ship, self.destination)
        while True:
            ship = self.survey(ship)
