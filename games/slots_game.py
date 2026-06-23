import random
from games.base_game import BaseGame
from models.game_result import GameResult
from settings import Config as cfg, SlotSymbol


class SlotsGame(BaseGame): # наследуется
    SYMBOLS = cfg.SLOT_SYMBOLS

    def __init__(self, bet: int) -> None:
        super().__init__(bet) # супер вызывает инит родителя
        self.reels: list[SlotSymbol] = [] # сами барабанчики

    @property # делает из метода атрибут/свойство, но внутри всё еще метод, просто вызывается как атрибут!!!
    def reels(self) -> list[SlotSymbol]:
        return self._reels

    @reels.setter
    def reels(self, value: list[SlotSymbol]) -> None:
        self._reels = value

    def play_round(self) -> GameResult: # сыграть один раунд и вернуть результат игры
        self.reels = [random.choice(self.SYMBOLS) for _ in range(cfg.SLOT_REEL_COUNT)] # _ типа переменная не нужна, просто повторение действия
        self.win_amount = self.calculate_result()
        self.is_win = self.win_amount > 0
        return GameResult(
            game="slots",
            bet=self.bet,
            reels=self.reels,
            is_win=self.is_win,
            win_amount=self.win_amount,
            balance_change=self.get_balance_change(),
        )

    def calculate_result(self) -> int:
        if len(self.reels) != cfg.SLOT_REEL_COUNT: # если не равно колву барабанчиков то плоха
            return 0
        unique_symbols = set(self.reels) # сет чтобы не было повторов
        max_matches = max(self.reels.count(symbol) for symbol in unique_symbols) # а это считает скок символов максимум и max вернет результатик
        multiplier = cfg.SLOT_PAYTABLE.get(max_matches, 0) # множитель смотрит в кфг
        return self.bet * multiplier # ставочка и множитель
