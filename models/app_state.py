from models.base_entity import BaseEntity # общий родитель моделей. даёт сравнение и вывод через print
from models.player import Player # класс игрока, в нём лежат логин и баланс
from models.settings import Settings 
from models.statistics import Statistics # класс со статистикой игр


class AppState(BaseEntity): # ОБЩЕЕ СОСТОЯНИЕ ПРИЛОЖЕНИЯ!
    # тут в одном месте хранятся игрок, статистика и настройки! эти объекты сначала загружаются из БД через AppStateService
    def __init__(
        self, player: Player, settings: Settings, statistics: Statistics) -> None: # передаётся готовый объект игрока
        self.player = player # сеттер player
        self.statistics = statistics # statistics
        self.settings = settings # и settings

    @property # нужен чтобы получать игрока через state.player
    def player(self) -> Player:
        return self._player

    @player.setter
    def player(self, value: Player) -> None:
        self._player = value

    @property
    def statistics(self) -> Statistics:
        return self._statistics

    @statistics.setter
    def statistics(self, value: Statistics) -> None:
        self._statistics = value

    @property
    def settings(self) -> Settings:
        return self._settings

    @settings.setter
    def settings(self, value: Settings) -> None:
        self._settings = value

    def update_balance(self, amount: int) -> None:
        self.player.balance = self.player.balance + amount

    def record_game(self, win: bool, win_amount: int = 0) -> None:
        self.statistics.add_game()
        if win:
            self.statistics.add_win(win_amount)

    def compare_value(self):
        return self.player.balance

    def display_text(self) -> str:
        return f"{self.player.login}: {self.player.balance}"
