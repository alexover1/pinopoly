from monopoly.player import Player
from monopoly.property import properties
from dataclasses import dataclass
from rich.markdown import Markdown
from enum import Enum
from typing import Any
from enquiries import *
import json, random
from time import sleep


class Moves(Enum):
    BUY_PROPERTY = ("Buy a property", "property")
    BUY_HOUSE = ("Buy a house or hotel", "house")
    END_TURN = ("End turn", "end_turn")
    EXIT = ("Exit game", "exit")


def update_json(fdir, values):
    new_val = {}
    for d in values:
        new_val.update(d)

    with open(fdir, "r") as f:
        data = json.load(f)
        f.close()

    with open(fdir, "w") as f:
        updated = {**data, **new_val}
        json.dump(updated, f)
        f.close()


############################################
# TURN HANDLER
############################################


@dataclass
class Turn:
    """Handles all actions a player can perform on their turn"""

    game: Any

    def __post_init__(self):
        self.player: Player = self.game.players[self.game.turn]
        self.console = self.game.console

    def visit(self, action: str):
        method_name = f"visit_{action}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(action)

    def no_visit_method(self, action: str):
        raise Exception(f"No visit_{action} method defined")

    def visit_property(self, _):
        with open("monopoly/assets/house.txt", "r") as f:
            a = f.read()
            self.console.print(a)

        p = random.randint(0, len(properties) - 1)
        property = properties[p]

        self.console.print(Markdown(f"# {property.name}"))
        self.console.print(property.table())

        if confirm(f"Do you want to buy {property}?", single_key=True, default=True):
            dir = f"generated/{self.game.id}/players/{self.player.name}.json"
            update_json(dir, [{"properties": [*self.player.properties, p]}])

        self.console.clear()
        self.game.advance()

    def visit_house(self, _):
        self.console.clear()
        print("yo")

        sleep(2)
        self.console.clear()
        self.game.take_turn()

    def visit_end_turn(self, _):
        self.console.clear()
        self.game.advance()

    def visit_exit(self, _):
        self.console.clear()
        exit(0)
