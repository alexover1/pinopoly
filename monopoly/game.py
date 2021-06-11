from monopoly.user import User
from enquiries import *


class GameMaster:
    def __init__(self, players):
        self.step = 0
        self.players = players

    def __repr__(self):
        return f"GameMaster"

    def advance(self):
        if (self.step + 1) > len(self.players) - 1:
            self.step = 0
            return
        self.step += 1

    def turn(self):
        return f"{self.players[self.step]}"


def run():
    game = GameMaster([User("John", "red"), User("Sarah", "green")])
    round_count = 10

    for i in range(round_count):
        choice = choose(
            f"It's {game.turn()}'s turn",
            ["Buy a property", "Buy a house or hotel", "End turn", "Exit game"],
        )

        if choice == "Buy a property":
            # TODO: buy a property
            game.advance()
        elif choice == "Buy a house or hotel":
            # TODO: buy a house or hotel
            game.advance()
        elif choice == "End turn":
            game.advance()
        elif choice == "Exit game":
            break
