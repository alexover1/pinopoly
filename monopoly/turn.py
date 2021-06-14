from monopoly.player import Player
from monopoly.property import properties
from dataclasses import dataclass
from enum import Enum
from typing import Any
from enquiries import *
import json, random
from time import sleep


class Moves(Enum):
    BUY_PROPERTY = ("Buy a property", "property")
    BUY_HOUSE = ("Buy a house or hotel", "house")
    PAY_RENT = ("Pay rent", "rent")
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
        self.console.clear()
        return method(action)

    def no_visit_method(self, action: str):
        raise Exception(f"No visit_{action} method defined")

    def visit_property(self, _):
        p = random.randint(0, len(properties) - 1)
        property = properties[p].load(self.game.id)

        self.console.print(property.table())
        self.console.print(f"You currently have [green]${self.player.balance}[/green]")
        self.console.print(
            f"If you buy {property.colored()}, you will have [green]${self.player.balance - property.price}[/green]\n"
        )

        if confirm(f"Do you want to buy {property}?", single_key=True, default=True):
            # Buy property
            self.player.properties.append(p)
            self.player.balance -= property.price
            self.player.save()
            property.update_ownership(self.player).save(self.game.id)

        self.console.clear()
        self.game.advance()

    def visit_house(self, _):
        if not len(self.player.properties) > 0:
            return self.go_back("You do not have any properties")

        choice = choose(
            "Which property do you want to buy a house on?",
            self.player.get_properties(),
        )

        if not choice:
            return self.go_back("[red]error[/red] Something went wrong")

        if not self.player.has_full_set(choice.color):  # type: ignore
            color = choice.color.value  # type: ignore
            return self.go_back(
                f"You do not have all of the [{color.lower()}]{color}[/{color.lower()}] properties"
            )

        self.console.print(f"You currently have [green]${self.player.balance}[/green]")
        self.console.print(
            f"Buying a house on {choice.colored()} will cost [green]${choice.house_price}[/green]\n"  # type: ignore
        )

        if confirm(f"Do you want to buy a house?", single_key=True, default=True):
            choice.house_count += 1  # type: ignore
            choice.save(self.game.id)  # type: ignore
            self.player.balance -= choice.price  # type: ignore
            self.player.save()

        self.game.take_turn()

    def visit_rent(self, _):

        self.console.print(self.player.properties_table())

        chosen_player = choose(
            "Who are you paying rent to?", [*self.game.players, "Go back"]
        )

        if chosen_player == "Go back":
            return self.go_back()

        list = chosen_player.get_properties()  # type: ignore
        chosen_property = choose("Which property?", [*list, "Go back"])

        if chosen_property == "Go back":
            return self.go_back()

        rent = chosen_property.rent[chosen_property.house_count]  # type: ignore
        self.player.balance -= rent
        self.go_back(
            f"You now have [green]${self.player.balance}[/green] ([red]-${rent}[/red])"
        )

    def visit_end_turn(self, _):
        self.console.clear()
        self.game.advance()

    def visit_exit(self, _):
        self.console.clear()
        exit(0)

    def go_back(self, message: str = None):
        if message:
            self.console.print(message)
            sleep(2)
        return self.game.take_turn()
