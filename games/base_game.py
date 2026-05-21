from abc import ABC, abstractmethod

class BaseGame(ABC):
    # базовый класс для всех игр чтобы общая логика не дублировалась
    def __init__(self, bet: int) -> None:
        self.bet = bet
        # победа или нет
        self.is_win = False
        # сколько денег дал выигрыш
        self.win_amount = 0

    @property
    def bet(self) -> int:
        # просто возвращает текущую ставку
        return self._bet
    
    @bet.setter
    def bet(self, value: int) -> None:
        # не дает создать игру со ставкой 0 или меньше мы же н ебланы)
        if value <= 0:
            raise ValueError("ставка должна быть больше 0")
        self._bet = value

    @staticmethod
    def can_make_bet(bet: int, balance: int) -> bool:
        # проверяет можно ли вообще сделать ставку с таким балансом 
        return 0 < bet <= balance
    
    def get_balance_change(self) -> int:
        if self.is_win:
            return self.win_amount
        return -self.bet # я ваще ахуел что можно делать просто через -
    
    @abstractmethod # у каждого дочернего класса обязательно должен быть свой метод с таким именем
    def play_round(self) -> dict:
        # этот метод обязаны сделать все дочерние игры
        pass

    @abstractmethod # 
    def calculate_result(self) -> int:
        # этот метод тоже обязаны сделать все дочерние игры
        pass
    
    @abstractmethod
    def reset(self) -> None:
        # тут каждая игра сама решает как сбрасывать свое состояние
        pass