from models.player import Player
from models.settings import Settings
from models.statistics import Statistics

class AppState:
    def __init__(self, player: Player, settings: Settings, statistics: Statistics) -> None:
        self.player = player
        self.statistics = statistics
        self.settings = settings

    def update_balance(self, amount: int) -> None:
        self.player.balance = self.player.balance + amount

    def record_game(self, win: bool, win_amount: int = 0) -> None:
        self.statistics.add_game()
        if win:
            self.statistics.add_win(win_amount)
