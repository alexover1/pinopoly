from pathlib import Path
from monopoly.property import Colors, properties
from dataclasses import dataclass, field
from rich.table import Table
from rich import box
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
            json.dump({"balance": self.balance, "properties": self.properties}, f)
            f.close()
        return self

    def update_balance(self, newbal):
        self.balance = newbal
        self.save()
        return self

    def buy_property(self, property):
        self.properties.append(property.id())
        self.balance -= property.price
        self.save()
        property.update_ownership(self).save(self.game_id)
        return self

    def get_properties(self):
        list = []
        for p in self.properties:
            property = properties[p].load(self.game_id)
            property.update_ownership(self)
            list.append(property)

        return list

    def properties_table(self):
        properties = self.get_properties()

        table = Table()
        table.box = box.SIMPLE

        table.add_column("Property")
        table.add_column("Houses")
        table.add_column("House price", style="cyan")
        table.add_column("Rent", style="cyan")
        table.add_column("Mortgage", style="green")

        for p in properties:
            table.add_row(
                f"{p.colored()}",
                f"{p.house_count}",
                f"${p.house_price}",
                f"${p.rent[p.house_count]}",
                f"${p.mortgage}",
            )

        return table

    def has_full_set(self, color: Colors):
        property_list = list(filter(lambda p: p.color == color, self.get_properties()))

        if color == (Colors.BROWN or Colors.BLUE):
            return len(property_list) == 2

        return len(property_list) == 3


############################################
# METHODS
###########################################


def get(name, game_id):
    path = Path(f"generated/{game_id}/players/{name}.json")

    if not path.exists():
        return None

    with path.open() as f:
        data = json.load(f)
        return Player(name, game_id, data["balance"], data["properties"])


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
