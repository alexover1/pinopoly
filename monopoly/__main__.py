from monopoly.menu import Menu
from monopoly.user import User, delete_users
import enquiries, art


############################################
# MAIN
############################################


def main():
    menu = Menu()
    menu.console.clear()

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
        menu.start_new_game()
    elif choice == "Resume existing game":
        menu.resume_game()
    elif choice == "Add a user":
        name = enquiries.freetext("What is the player's name?")
        if not name:
            exit(1)
        User(name).save()
    elif choice == "Delete all users":
        if enquiries.confirm(
            "Are you sure you want to delete all users?", single_key=True
        ):
            delete_users()
    else:
        menu.exit()


if __name__ == "__main__":
    main()
