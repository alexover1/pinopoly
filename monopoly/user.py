import os, glob, random, string, json


class User:
    def __init__(self, name, properties=[]):
        self.name = name
        self.id = "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(16)
        )
        self.properties = properties

    def __repr__(self):
        return f"{self.name}"

    def save(self):
        with open(f"generated/users/{self.name}.json", "w") as f:
            json.dump(
                {"id": self.id, "name": self.name, "properties": self.properties}, f
            )
            f.close()
        return self


def delete_users():
    dir = "generated/users"
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)


def all_users():
    dir = "generated/users/*.json"
    filelist = glob.glob(dir)
    users = []

    for f in filelist:
        with open(f, "r") as f:
            data = json.load(f)
            user = User(data["name"], data["properties"])
            users.append(user)
            f.close()

    list = sorted(users, key=lambda k: k.name)

    return list
