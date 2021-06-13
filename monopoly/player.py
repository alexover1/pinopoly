from monopoly.user import User
from dataclasses import dataclass, field
import os, glob, json


############################################
# PLAYER
############################################


@dataclass
class Player:
    name: str
    game_id: str
    balance: int = 1500
    properties: list = field(default_factory=lambda: [])

    def __repr__(self):
        return f"{self.name}"

    def save(self):
        with open(f"generated/{self.game_id}/players/{self.name}.json", "w") as f:
            print(self.__dict__)
            json.dump({"balance": self.balance, "properties": self.properties}, f)
            f.close()
        return self

    def update_balance(self, newbal):
        self.balance = newbal
        self.save()
        return self


############################################
# METHODS
###########################################


def get_players(game_id):
    dir = f"generated/{game_id}/players/*.json"
    filelist = glob.glob(dir)

    players = []
    for fn in filelist:
        with open(fn, "r") as f:
            name = os.path.basename(fn).split(".")[0]
            data = json.load(f)
            players.append(Player(name, game_id, data["balance"], data["properties"]))
            f.close()

    return sorted(players, key=lambda k: k.name)


def create_players(game_id: str, users: list) -> list:
    players = []
    for user in users:
        players.append(Player(user.name, game_id).save())

    return players
