from monopoly.user import create_user, delete_users
from monopoly.game import run
import enquiries
import art


def main():
    art.tprint("pinopoly")
    options = [
        "Start a new game",
        "Resume existing game",
        "Add a user",
        "Delete all users",
    ]
    choice = enquiries.choose("Choose one of these options: ", options)

    if choice == "Delete all users":
        if enquiries.confirm(
            "Are you sure you want to delete all users?", single_key=True
        ):
            delete_users()
    elif choice == "Add a user":
        name = enquiries.freetext("What do you want to name the user?")
        create_user(name, "red")
    elif choice == "Start a new game":
        run()
    else:
        print(choice)


if __name__ == "__main__":
    main()