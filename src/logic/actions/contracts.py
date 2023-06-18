import attrs
from time import sleep
from rich.console import Console
from rich.table import Table

from src.schemas.ships import Ship, Cargo
from src.schemas.mining import Extraction
from src.schemas.transactions import Transaction
from src.schemas.contracts import Contract, ContractManager
from src.schemas.errors import Error
from src.support.tables import report_result


from .ships import AbstractShipNavigate


@attrs.define
class ContractMiningLoop(AbstractShipNavigate):
    ship_symbol: str
    contract_id: str
    mining_destination: str
    contract: Contract = None
    contract_good: str = None
    console: Console = Console()
    expenses: int = 0
    non_contract_good_sales: int = 0
    delivery_this_run: bool = False

    def get_contract(self):
        contracts_manager = ContractManager.get()
        contract = [c for c in contracts_manager.contracts if c.id == self.contract_id]
        assert contract, f"No contract with ID {self.contract_id} found!"
        self.contract = contract[0]

    @property
    def name(self) -> str:
        return f"Ship {self.ship_symbol} peforming contract {self.contract_id}"

    def sleep(self):
        pass

    def mine_until_cargo_full(self, ship: Ship) -> Ship:
        """
        Mine until the cargo is full, then report the contents of the cargo.
        """
        ship.orbit()
        cargo_status = ship.cargo_status()
        if cargo_status.units == cargo_status.capacity:
            self.console.print("Cargo is full")
            report_result(cargo_status, Cargo)
            return ship

        self.console.print("Mining...")
        while cargo_status.units < cargo_status.capacity:
            result = ship.extract()
            if isinstance(result, Error):
                report_result(result, Extraction)
                cooldown = result.data.get("cooldown", None)
                if cooldown:
                    sleep(cooldown["remainingSeconds"])
            else:
                report_result(result["extraction"], Extraction)
                cooldown = result["cooldown"].remainingSeconds
                self.console.print(f"Cooldown for {cooldown} seconds")
                sleep(cooldown)
            cargo_status = ship.cargo_status()

        self.console.print("Cargo is full")
        report_result(cargo_status, Cargo)
        return ship

    def sell_cargo_that_isnt_contract_good(self, ship: Ship, do_not_sell: str) -> Ship:
        """
        Sell all the contents of the cargo except trade good.
        """
        ship.dock()
        cargo = ship.cargo_status()
        items_units = [
            (x["symbol"], x["units"])
            for x in cargo.inventory
            if x["symbol"] != do_not_sell
        ]
        self.console.print(f"Total cargo to sell: {items_units}")
        for symbol, units in items_units:
            self.console.log(f"Selling {symbol}...")
            result = ship.sell(symbol=symbol, amount=units)
            if isinstance(result, Error):
                report_result(result, Ship)
            else:
                transaction = result["transaction"]
                report_result(transaction, Transaction)
                self.non_contract_good_sales += transaction.totalPrice
        return ship

    def set_up_contract(self) -> None:
        """
        Makes sure the contract is accepted and not fulfilled etc.
        Prints some useful information about it.
        """
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
        self.contract.deliver(
            ship_symbol=ship.symbol, trade_symbol=self.contract_good, amount=amount
        )

    def process(self):
        self.get_contract()
        self.set_up_contract()
        ship = Ship.get(symbol=self.ship_symbol)
        enough_trade_goods_to_sell = self.enough_contract_goods_to_sell(ship)
        if enough_trade_goods_to_sell is False:
            ship = self.navigate_to(ship, destination=self.mining_destination)
            ship = self.mine_until_cargo_full(ship)
            ship = self.sell_cargo_that_isnt_contract_good(
                ship, do_not_sell=self.contract_good
            )
        else:
            self.console.print(f"We have enough {self.contract_good} to sell!")
            self.navigate_to(
                ship=ship,
                destination=self.contract.terms.deliver[0]["destinationSymbol"],
            )
            self.deliver_goods(ship=ship)

        self.get_contract()
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
            str(self.non_contract_good_sales),
        )

        self.console.print(table)

        return units_fulfilled == units_required
