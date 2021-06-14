import monopoly.player
import monopoly.turn
import monopoly.property
from dataclasses import dataclass, field
from rich.console import Console
from typing import List
from enquiries import *
import random, string, json, glob, os
from pathlib import Path


def random_id():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(16)
    )


############################################
# GAME
############################################


@dataclass
class Game:
    players: list = field(default_factory=lambda: [])
    id: str = ""
    turn: int = 0
    step: int = 1
    console = Console()

    def __post_init__(self):
        self.players = self.get_players()
        if not self.id:
            self.id = random_id()

    def __repr__(self):
        return f"Game {self.id}"

    ############################################

    def new(self):
        os.mkdir(f"generated/{self.id}")
        os.mkdir(f"generated/{self.id}/players")
        os.mkdir(f"generated/{self.id}/properties")

        with open(f"generated/{self.id}/game.json", "w") as f:
            json.dump(
                {"turn": self.turn, "step": self.step},
                f,
                indent=2,
                sort_keys=True,
            )
            f.close()
        return self

    def advance(self):
        """Called at the end of a player's turn, advances to the next player's turn"""

        if (self.turn + 1) > len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

        self.step += 1
        self.player = self.players[self.turn]
        return self.save()

    def save(self):
        with open(f"generated/{self.id}/game.json", "w") as f:
            json.dump({"turn": self.turn, "step": self.step}, f)
            f.close()
        return self

    ############################################

    def get_players(self) -> List[monopoly.player.Player]:
        dir = f"generated/{self.id}/players/*.json"
        filelist = glob.glob(dir)

        players = []
        for fn in filelist:
            with open(fn, "r") as f:
                name = os.path.basename(fn).split(".")[0]
                data = json.load(f)
                players.append(
                    monopoly.player.Player(
                        name, self.id, data["balance"], data["properties"]
                    )
                )
                f.close()

        return sorted(players, key=lambda k: k.name)

    def update_players(self, players):
        self.players = players
        return self

    def take_turn(self):
        with open("monopoly/assets/bank.txt", "r") as f:
            a = f.read()
            self.console.print(a)
        choice = choose(
            f"It's {self.players[self.turn]}'s turn",
            [
                "Properties",
                "Pay rent",
                "End turn",
                "Exit game",
            ],
        )

        for m in monopoly.turn.Moves:
            if choice == m.value[0]:
                monopoly.turn.Turn(self).visit(m.value[1])


############################################
# METHODS
############################################


def run(game: Game):
    while True:
        game.take_turn()


def all_games() -> List[Game]:
    dir = "generated/**/game.json"
    filelist = glob.glob(dir)
    games = []

    for fn in filelist:
        path = Path(fn)

        with open(fn, "r") as f:
            data = json.load(f)
            id = os.path.basename(path.parent.absolute())
            games.append(Game(id=id, turn=data["turn"], step=data["step"]))
            f.close()

    return games
