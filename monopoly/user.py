from dataclasses import dataclass
import os, glob, json


############################################
# USER
###########################################


@dataclass
class User:
    name: str
    wins: int = 0

    def __repr__(self):
        return f"{self.name}"

    def save(self):
        with open(f"generated/users/{self.name}.json", "w") as f:
            json.dump(self.__dict__, f)
            f.close()
        return self


############################################
# METHODS
###########################################


def get_users() -> list[User]:
    """Returns a list of users from the generated/users directory"""
    dir = "generated/users/*.json"
    filelist = glob.glob(dir)

    users = []
    for f in filelist:
        with open(f, "r") as f:
            data = json.load(f)
            users.append(User(data["name"], data["wins"]))
            f.close()

    return sorted(users, key=lambda k: k.name)


def delete_users():
    dir = "generated/users"
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
