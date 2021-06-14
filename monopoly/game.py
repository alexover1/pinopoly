from monopoly.player import Player
from monopoly.turn import Turn, Moves
from monopoly.property import properties
from dataclasses import dataclass, field
from rich.console import Console
from enquiries import *
import random, string, json, glob, os
from pathlib import Path


############################################
# GAME
###########################################


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


def random_id():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(16)
    )


@dataclass
class Game:
    players: list = field(default_factory=lambda: [])
    id: str = ""
    turn: int = 0
    step: int = 0
    console = Console()

    def __post_init__(self):
        self.players = self.get_players()
        if not self.id:
            self.id = random_id()

    def __repr__(self):
        return f"Game {self.id}"

    def get_players(self):
        dir = f"generated/{self.id}/players/*.json"
        filelist = glob.glob(dir)

        players = []
        for fn in filelist:
            with open(fn, "r") as f:
                name = os.path.basename(fn).split(".")[0]
                data = json.load(f)
                players.append(
                    Player(name, self.id, data["balance"], data["properties"])
                )
                f.close()

        return sorted(players, key=lambda k: k.name)

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

    def update_players(self, players):
        self.players = players

    def advance(self):
        """Called at the end of a player's turn, advances to the next player's turn"""
        if (self.turn + 1) > len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

        self.step += 1
        self.player = self.players[self.turn]

        update_json(
            f"generated/{self.id}/game.json",
            [{"turn": self.turn}, {"step": self.step}],
        )

    def take_turn(self):
        self.console.clear()
        with open("monopoly/assets/bank.txt", "r") as f:
            a = f.read()
            self.console.print(a)
        choice = choose(
            f"It's {self.players[self.turn]}'s turn",
            [
                "Buy a property",
                "Buy a house or hotel",
                "Pay rent",
                "End turn",
                "Exit game",
            ],
        )

        for m in Moves:
            if choice == m.value[0]:
                Turn(self).visit(m.value[1])

    def play(self, move):
        method_name = f"play_{move}"
        method = getattr(self, method_name, self.play_error)
        return method()

    def play_error(self):
        raise Exception(f"Missing play_ method")

    def play_property(self):
        with open("monopoly/assets/house.txt", "r") as f:
            a = f.read()
            self.console.print(a)

        p = random.randint(0, len(properties) - 1)
        property = properties[p]

        self.console.print(property.table())

        if confirm(f"Do you want to buy {property}?", single_key=True, default=True):
            dir = f"generated/{self.id}/{self.player.name}.json"
            update_json(dir, [{"properties": [*self.player.properties, p]}])

        self.console.clear()
        self.advance()

    def play_house(self):
        with open("monopoly/assets/bank.txt", "r") as f:
            a = f.read()
            self.console.print(a)
        if confirm(f"Do you want to yes?", single_key=True):
            self.console.clear()
            self.advance()

    def play_end(self):
        self.advance()

    def play_exit(self):
        exit(0)


def all_games():
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


def run(game: Game):
    # round_count = 10
    # for i in range(round_count)

    while True:
        game.take_turn()
