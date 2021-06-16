from enum import Enum
from dataclasses import dataclass
from typing import Any
import monopoly.player


class Logs(Enum):
    BUY_PROPERTY = 0
    MORTGAGE_PROPERTY = 1
    UNMORTGAGE_PROPERTY = 2
    PAY_RENT = 3
    BUY_HOUSE = 4
    SELL_HOUSE = 5


@dataclass
class Log:
    game_id: str
    player: monopoly.player.Player
    amount: int = None
    other: Any = None

    def save(self, message):
        dir = f"generated/{self.game_id}/logs.txt"

        with open(dir, "a") as f:
            f.write(message + "\n")
            f.close()

    def require(self, value, action):
        if not value:
            raise Exception(f"Log.visit_{action} ---> '{value}' is not defined")

    def visit(self, action):
        method_name = f"visit_{action.name.lower()}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(action)

    def no_visit_method(self, action: str) -> Exception:
        """Throws an error because an action was requested that was not defined"""
        raise Exception(f"No visit_{action} method defined")

    def visit_buy_property(self, action):
        self.require(self.player, action)
        self.require(self.other, action)
        self.require(self.amount, action)

        self.save(f"{self.player} bought {self.other} for ${self.amount}")

    def visit_mortgage_property(self, action):
        self.require(self.player, action)
        self.require(self.other, action)

        self.save(f"{self.player} mortgaged {self.other}")

    def visit_unmortgage_property(self, action):
        self.require(self.player, action)
        self.require(self.other, action)

        self.save(f"{self.player} unmortgaged {self.other}")

    def visit_pay_rent(self, action):
        self.require(self.player, action)
        self.require(self.other, action)
        self.require(self.amount, action)

        self.save(f"{self.player} payed ${self.amount} in rent to {self.other}")

    def visit_buy_house(self, action):
        self.require(self.player, action)
        self.require(self.other, action)

        self.save(f"{self.player} bought a house on {self.other}")
