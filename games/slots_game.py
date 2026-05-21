import random
from games.base_game import BaseGame

class SlotsGame(BaseGame):
    SYMBOLS = ("cherry", "lemon", "bell", "star", "seven")
    def __init__(self, bet: int) -> None:
        super().__init__(bet)
        self.reels: list[str] = []

    def play_round(self) -> dict:
        self.reels = [random.choice(self.SYMBOLS) for _ in range(3)]
        self.win_amount = self.calculate_result()
        self.is_win = self.win_amount > 0
        return {
            "game": "slots",
            "bet": self.bet,
            "reels": self.reels,
            "is_win": self.is_win,
            "win_amount": self.win_amount,
            "balance_change": self.get_balance_change(),
        }

    def calculate_result(self) -> int:
        if len(self.reels) != 3:
            return 0
        unique_symbols = set(self.reels)
        if len(unique_symbols) == 1:
            return self.bet * 5
        if len(unique_symbols) == 2:
            return self.bet * 2
        return 0

    # я здесь чистит состояние объекта
    def reset(self) -> None:
        self.reels = []
        self.is_win = False
        self.win_amount = 0
