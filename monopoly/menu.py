from monopoly.game import Game, all_games, run
from monopoly.user import get_users
from monopoly.player import create_players, get_players
from dataclasses import dataclass
from rich.console import Console
import enquiries


############################################
# MENU
############################################


@dataclass
class Menu:
    console = Console()

    def start_new_game(self):
        self.console.clear()
        users = get_users()
        chosen_users = enquiries.choose("Choose players:", users, multi=True)

        game = Game().new()
        players = create_players(game.id, chosen_users)

        game.update_players(players)
        run(game)

    def resume_game(self):
        self.console.clear()
        games = all_games()

        if len(games) == 0:
            exit(0)

        chosen_game = enquiries.choose(
            "Which game do you want to resume?", [*games, "Cancel"]
        )

        if chosen_game == "Cancel":
            exit(0)

        run(chosen_game)  # type: ignore

    def exit(self):
        self.console.clear()
        exit(0)
