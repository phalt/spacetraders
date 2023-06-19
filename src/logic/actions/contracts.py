from typing import Optional
import attrs
from rich.console import Console
from rich.table import Table

from src.schemas.ships import Ship
from src.schemas.contracts import Contract
from src.support.tables import report_result


from .ships import AbstractShipNavigate, AbstractSellCargo, AbstractMining


@attrs.define
class ContractMiningLoop(AbstractShipNavigate, AbstractSellCargo, AbstractMining):
    ship_symbol: str
    contract_id: str
    mining_destination: str
    contract: Optional[Contract] = None
    contract_good: Optional[str] = ""
    console: Console = Console()
    expenses: int = 0
    cargo_sales: int = 0
    delivery_this_run: bool = False

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} peforming contract {self.contract_id}"

    def sleep(self):
        pass

    def set_up_contract(self) -> None:
        """
        Makes sure the contract is accepted and not fulfilled etc.
        Prints some useful information about it.
        """
        if self.contract:
            report_result(self.contract, Contract)
            if not self.contract.accepted:
                self.console.print("Accepting contract...")
                self.contract.accept()

            self.contract_good: str = self.contract.terms.deliver[0]["tradeSymbol"]

    def enough_contract_goods_to_sell(self, ship: Ship) -> bool:
        """
        If 2/3 of the cargo hold is the contract good then return True.
        """
        cargo_limit = int(ship.cargo.capacity * 0.7)
        contract_goods_in_cargo = sum(
            [
                x["units"]
                for x in ship.cargo.inventory
                if x["symbol"] == self.contract_good
            ]
        )
        if contract_goods_in_cargo > cargo_limit:
            return True
        else:
            self.console.print(
                f"Got {contract_goods_in_cargo} / {cargo_limit} {self.contract_good}"
            )
            return False

    def deliver_goods(self, ship: Ship):
        """
        Deliver the goods for the contract with the ship
        """
        amount = sum(
            [
                x["units"]
                for x in ship.cargo.inventory
                if x["symbol"] == self.contract_good
            ]
        )
        self.console.print(f"Delivering {amount} of {self.contract_good}")
        if self.contract_good and self.contract:
            self.contract.deliver(
                ship_symbol=ship.symbol, trade_symbol=self.contract_good, amount=amount
            )

    def process(self):
        self.contract = Contract.get(self.contract_id)
        self.set_up_contract()
        ship = Ship.get(symbol=self.ship_symbol)
        enough_trade_goods_to_sell = self.enough_contract_goods_to_sell(ship)
        if enough_trade_goods_to_sell is False:
            ship = self.navigate_to(ship, destination=self.mining_destination)
            ship = self.mine_until_cargo_full(ship)
            ship = self.sell_cargo(ship, do_not_sell_symbols=[self.contract_good])
        else:
            self.console.print(f"We have enough {self.contract_good} to sell!")
            self.navigate_to(
                ship=ship,
                destination=self.contract.terms.deliver[0]["destinationSymbol"],
            )
            self.deliver_goods(ship=ship)

        self.contract = Contract.get(self.contract_id)
        table = Table(title="Contract progress")
        table.add_column("Delivered total")
        table.add_column("Goal")
        table.add_column("Fulfillment reward")
        table.add_column("Expenses this run")
        table.add_column("Other sales earned")

        units_fulfilled = self.contract.terms.deliver[0]["unitsFulfilled"]
        units_required = self.contract.terms.deliver[0]["unitsRequired"]

        table.add_row(
            str(units_fulfilled),
            str(units_required),
            str(self.contract.terms.payment["onFulfilled"]),
            str(self.expenses),
            str(self.cargo_sales),
        )

        self.console.print(table)

        return units_fulfilled == units_required
