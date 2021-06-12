from monopoly.user import User
from monopoly.property import properties
import random, string, json, art, sys, glob, os
from enquiries import *


def delete_last_line(count=1):
    for _ in range(count):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")


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


movements = [
    ("Buy a property", "property"),
    ("Buy a house or hotel", "house"),
    ("End turn", "end"),
    ("Exit game", "exit"),
]


class Game:
    def __init__(self, players, id=None, turn=0, step=1):
        self.players = self.get_players(players)
        self.turn = turn
        self.step = step

        self.id = id or "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(16)
        )

    def __repr__(self):
        return f"Game {self.id}"

    def get_players(self, names):
        players = []
        for name in names:
            dir = f"generated/users/{name}.json"
            with open(dir, "r") as f:
                data = json.load(f)
                user = User(data["name"], data["properties"])
                players.append(user)
                f.close()
        return players

    def new(self):
        with open(f"generated/games/{self.id}.json", "w") as f:
            json.dump(
                {"turn": self.turn, "step": self.step, "players": self.players}, f
            )
            f.close()
        return self

    def advance(self):
        if (self.turn + 1) > len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

        self.step += 1
        update_json(
            f"generated/games/{self.id}.json",
            [{"turn": self.turn}, {"step": self.step}],
        )

    def take_turn(self):
        art.tprint(f"{self.players[self.turn]}")
        choice = choose(
            f"It's {self.players[self.turn]}'s turn",
            ["Buy a property", "Buy a house or hotel", "End turn", "Exit game"],
        )

        for m in movements:
            if choice == m[0]:
                self.play(m[1])

    def play(self, move):
        method_name = f"play_{move}"
        method = getattr(self, method_name, self.play_error)
        return method()

    def play_error(self):
        raise Exception(f"Missing play_ method")

    def play_property(self):
        player = self.players[self.turn]
        delete_last_line(7)

        p = random.randint(0, len(properties) - 1)
        property = properties[p]
        name = property.name.value.replace(" ", "\n")

        print(art.text2art(f"{name}", font="small"))
        if confirm(f"Do you want to buy {property}?", single_key=True, default=True):
            dir = f"generated/users/{player.name}.json"
            update_json(dir, [{"properties": [*player.properties, p]}])

        delete_last_line(11)
        self.advance()

    def play_house(self):
        delete_last_line(7)
        self.advance()

    def play_end(self):
        delete_last_line(7)
        self.advance()

    def play_exit(self):
        delete_last_line(7)
        exit(0)


def all_games():
    dir = "generated/games/*.json"
    filelist = glob.glob(dir)
    games = []

    for fn in filelist:
        with open(fn, "r") as f:
            id = os.path.basename(fn).split(".")[0]
            data = json.load(f)
            game = Game(data["players"], id, data["turn"], data["step"])
            games.append(game)
            f.close()

    return games


def run(game: Game):
    # round_count = 10
    # for i in range(round_count)

    while True:
        game.take_turn()
