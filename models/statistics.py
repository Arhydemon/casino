from models.base_entity import BaseEntity
# общий родитель моделей, даёт сравнение и нормальный вывод объекта


class Statistics(BaseEntity): # КЛАСС СО СТАТИСТИКОЙ ИГРОКА! # хранит количество игр, побед и общую сумму выигрышей
    def __init__(self, games_played: int, wins: int, total_win: int) -> None:
        self.games_played = games_played # сработает сеттер games_played
        self.wins = wins
        self.total_win = total_win

    @property # кол во игр через statistics.games_played
    def games_played(self) -> int:
        return self._games_played

    @games_played.setter
    def games_played(self, value: int) -> None:
        self._games_played = int(value)

    @property
    def wins(self) -> int:
        return self._wins

    @wins.setter
    def wins(self, value: int) -> None:
        self._wins = int(value)

    @property
    def total_win(self) -> int:
        return self._total_win

    @total_win.setter
    def total_win(self, value: int) -> None:
        self._total_win = int(value)

    def add_game(self) -> None: # вызывается после КАЖДОЙ игры, неважно победа или проигрыш
        self.games_played += 1

    def add_win(self, win_amount: int) -> None:
        self.wins += 1 # количество побед увеличивается на один
        self.total_win = win_amount + self.total_win

    def compare_value(self): # нужен из-за BaseEntity
        return self.total_win

    def display_text(self) -> str: # вернёт строку типа игр: 10, побед: 4
        return f"игр: {self.games_played}, побед: {self.wins}"
