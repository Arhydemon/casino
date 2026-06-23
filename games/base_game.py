from abc import abstractmethod # для создания обстрактных методов, которые обязательно должны быть реализованы в дочерних классах

from models.base_entity import BaseEntity
# BaseEntity общий родитель почти всех моделей в проекте
from settings import Config as cfg


class BaseGame(BaseEntity): # базовый класс для ВСЕХ ИГР!
# от него наследуются слоты и рулетка
# класс хранит общие данные: ставку, выиграл игрок или нет, сумму выигрыша
    def __init__(self, bet: int) -> None:
        # ставка игрока, тут self.bet, поэтому сработает сеттер, который чекает минимальную ставку
        self.bet = bet
        self.is_win = False # до запуска победы нет
        self.win_amount = 0 # пока не сыграется, то выигрыша не будет

    @property # декоратор
    # декоратор это специальная команда которая меняет поведение функции или метода, расположенного сразу под ней
    def bet(self) -> int:
        return self._bet # _ - внутренняя переманная класса йоу

    @bet.setter # нужен чтобы было легче жить!
    def bet(self, value: int) -> None:
        if value < cfg.MIN_BET:
            raise ValueError("ставка должна быть больше 0")
        self._bet = value

    @property
    def is_win(self) -> bool:
        return self._is_win

    @is_win.setter
    def is_win(self, value: bool) -> None:
        self._is_win = bool(value)

    @property
    def win_amount(self) -> int:
        return self._win_amount

    @win_amount.setter
    def win_amount(self, value: int) -> None:
        self._win_amount = int(value)

    @staticmethod # СТАТИСТИЧЕСКИЙ МЕТОД 
    # ОЗНАЧАЕТ, ЧТО ЭТОМУ МЕТОДУ НЕ НУЖЕН self !!!
    # МОЖНО ВЫЗЫВАТЬ ЧЕРЕЗ НАЗВАНИЕ КЛАССА!
    # ОН ПОЛУЧАЕТ ДВА ЧИСЛА И DO CHECK
    # ЕМУ НЕ НУЖНЫ ДАННЫЕ КОНКРЕТНОГО ОБЪЕКТА И ИГРЫ !!!
    def can_make_bet(bet: int, balance: int) -> bool:
        return cfg.MIN_BET <= bet <= balance

    def get_balance_change(self) -> int:
        if self.is_win:
            return self.win_amount
        return -self.bet

    @abstractmethod # он запрещает создать объект, пока метод не реализован, типа для каждой игры он свой
    def play_round(self):
        raise NotImplementedError # это аварийная заглушка.

    @abstractmethod
    def calculate_result(self) -> int:
        raise NotImplementedError

    def compare_value(self):
        return self.bet

    def display_text(self) -> str:
        return f"ставка: {self.bet}"
