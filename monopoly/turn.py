import monopoly.player
import monopoly.property
from dataclasses import dataclass
from enum import Enum
from typing import Any
from rich.markdown import Markdown
from enquiries import *
import random, time


class Moves(Enum):
    BUY_PROPERTY = ("Properties", "properties")
    PAY_RENT = ("Pay rent", "rent")
    END_TURN = ("End turn", "end_turn")
    EXIT = ("Exit game", "exit")


############################################
# TURN HANDLER
############################################


@dataclass
class Turn:
    """Handles all actions a player can perform on their turn"""

    game: Any

    def __post_init__(self):
        self.player: monopoly.player.Player = self.game.players[self.game.turn]
        self.console = self.game.console

    def visit(self, action: str):
        """Performs the requested action"""
        method_name = f"visit_{action}"
        method = getattr(self, method_name, self.no_visit_method)
        self.console.clear()
        return method(action)

    def no_visit_method(self, action: str) -> Exception:
        """Throws an error because an action was requested that was not defined"""
        raise Exception(f"No visit_{action} method defined")

    ############################################

    def visit_properties(self, _):
        """Maps out a player's properties"""

        self.console.print(self.player.properties_table())

        choice = choose("", ["Buy new property", "Buy a house or hotel", "Go back"])

        if choice == "Buy new property":
            return self.visit_new_property()
        elif choice == "Buy a house or hotel":
            return self.visit_house(None)
        elif choice == "Go back":
            return self.go_back()

    ############################################

    def visit_new_property(self):
        """Buys a new property"""

        self.console.clear()
        p = random.randint(0, len(monopoly.property.properties) - 1)
        property = monopoly.property.properties[p].load(self.game.id)

        if property.owner:
            return self.go_back(f"That property is already owned by {property.owner}")

        if (self.player.balance - property.price) < 0:
            return self.go_back(
                f"You do not have enough money to buy {property.colored()}"
            )

        self.console.print(Markdown(f"# {property.name.value}"))
        self.console.print(property.table())
        self.console.print(f"You currently have [green]${self.player.balance}[/green]")
        self.console.print(
            f"If you buy {property.colored()}, you will have [green]${self.player.balance - property.price}[/green] (-[red]${property.price}[/red])\n"
        )

        if confirm(f"Do you want to buy {property}?", single_key=True, default=True):
            # Buy property
            self.player.properties.append(p)
            self.player.balance -= property.price
            self.player.save()
            property.update_ownership(self.player).save(self.game.id)

            self.console.clear()
            return self.game.advance()

        self.console.clear()
        self.go_back()

    ############################################

    def visit_house(self, _):
        """Buys a house on a player's property"""

        if not len(self.player.properties) > 0:
            return self.go_back("You do not have any properties")

        property = choose(
            "Which property do you want to buy a house on?",
            [*self.player.get_properties(), "Go back"],
        )

        if property == "Go back":
            return self.go_back()

        if not self.player.has_full_set(property.color):
            color = property.color.value
            return self.go_back(
                f"You do not have all of the [{color.lower()}]{color}[/{color.lower()}] properties"
            )

        self.console.print(f"You currently have [green]${self.player.balance}[/green]")
        self.console.print(
            f"Buying a house on {property.colored()} will cost [green]${property.house_price}[/green]\n"
        )

        if confirm(f"Do you want to buy a house?", single_key=True, default=True):
            property.house_count += 1
            property.save(self.game.id)
            self.player.balance -= property.price
            self.player.save()

        self.go_back()

    ############################################

    def visit_rent(self, _):
        """Takes away money from current player based on rent amount"""

        with open("monopoly/assets/bank.txt", "r") as f:
            a = f.read()
            self.console.print(a)

        filtered_players = list(
            filter(lambda x: x.name != self.player.name, self.game.players)
        )

        # Get player
        chosen_player = choose(
            "Who are you paying rent to?", [*filtered_players, "Go back"]
        )
        if chosen_player == "Go back":
            return self.go_back()

        # Get property
        chosen_property = choose(
            "Which property?", [*chosen_player.get_properties(), "Go back"]
        )
        if chosen_property == "Go back":
            return self.go_back()

        # Pay rent
        rent = chosen_property.rent[chosen_property.house_count]
        self.player.balance -= rent
        self.go_back(
            f"You now have [green]${self.player.balance}[/green] ([red]-${rent}[/red])"
        )

    ############################################

    def visit_end_turn(self, _):
        """Ends current turn and moves on to next one"""

        self.console.clear()
        self.game.advance()

    def visit_exit(self, _):
        """Exits the game"""

        self.console.clear()
        exit(0)

    def go_back(self, message: str = None):
        """Goes back to move selection"""

        if message:
            self.console.print(message)
            time.sleep(2)

        self.console.clear()
        return self.game.take_turn()
