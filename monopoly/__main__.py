from monopoly.user import User, delete_users, all_users
from monopoly.game import Game, all_games, run
import enquiries, art, sys


def delete_last_line(count=1):
    for _ in range(count):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")


def main():
    art.tprint("pinopoly")
    options = [
        "Start a new game",
        "Resume existing game",
        "Add a user",
        "Manage users",
        "Delete all users",
        "Exit",
    ]
    choice = enquiries.choose("Welcome to pinopoly", options)

    if choice == "Start a new game":
        delete_last_line(7)

        players = []
        for player in all_users():
            players.append(player.name)

        choice = enquiries.choose("Choose players:", players, multi=True)

        game = Game(choice).new()
        run(game)
    elif choice == "Resume existing game":
        games = all_games()
        if not len(games) > 0:
            exit(0)

        choice = enquiries.choose(
            "Which game do you want to resume?", [*games, "Cancel"]
        )

        delete_last_line(7)

        if choice == "Cancel":
            exit(0)

        run(choice)  # type: ignore
    elif choice == "Add a user":
        name = enquiries.freetext("What is the player's name?")
        User(name).save()
    elif choice == "Delete all users":
        if enquiries.confirm(
            "Are you sure you want to delete all users?", single_key=True
        ):
            delete_users()
    else:
        delete_last_line(7)
        exit(0)


if __name__ == "__main__":
    main()
