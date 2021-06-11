import json
import os, glob


class User:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return f"{self.name}"


def create_user(name, color):
    user = User(name, color)

    data = {"name": name, "color": color}

    with open(f"monopoly/generated/{name}.json", "w") as f:
        json.dump(data, f)

    return user


def delete_users():
    dir = "monopoly/generated"
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
