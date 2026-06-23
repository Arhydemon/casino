import random
from games.base_game import BaseGame
from models.game_result import GameResult
from settings import Config as cfg


class RouletteGame(BaseGame):
    # тут у мя константы класса
    NUMBER_BET = "number" # на конкретное число
    COLOR_BET = "color" # на цвет
    EVEN_ODD_BET = "even_odd" # чётность
    RED = "red"
    BLACK = "black"
    GREEN = "green"
    EVEN = "even" # чётно
    ODD = "odd" # нечётно
    COLORS = (RED, BLACK, GREEN) # кортеж доступных цветов, проверка на дебила
    EVEN_ODD_VALUES = (EVEN, ODD) # тож самое ток с чётностью
    RED_NUMBERS = cfg.ROULETTE_RED_NUMBERS # списочек красных чисел рулеточки

    def __init__(self, bet: int, bet_type: str, bet_value: int | str) -> None: # конструктор рулетки
        super().__init__(bet)
        self.bet_type = bet_type # тип ставки
        self.bet_value = bet_value # значение ставочки тут сеттер работает
        self.number: int | None = None # выпавшее число
        self.color: str | None = None # выпавший цвет
        self._validate_bet_choice() # снова проверка на дебила

    @property # бет_тайп сделал свойством чтобы обращаться к атрибуту
    def bet_type(self) -> str: # геттер для бет тайпа
        return self._bet_type

    @bet_type.setter
    def bet_type(self, value: str) -> None:
        self._bet_type = value
        # проверка отдельно

    @property
    def bet_value(self) -> int | str:
        return self._bet_value

    @bet_value.setter
    def bet_value(self, value: int | str) -> None:
        self._bet_value = value

    @property
    def number(self) -> int | None:
        return self._number

    @number.setter
    def number(self, value: int | None) -> None:
        self._number = value

    @property
    def color(self) -> str | None:
        return self._color

    @color.setter
    def color(self, value: str | None) -> None:
        self._color = value

    @staticmethod
    def get_number_color(number: int) -> str:
        if number == cfg.ROULETTE_MIN_NUMBER:
            return RouletteGame.GREEN
        if number in RouletteGame.RED_NUMBERS:
            return RouletteGame.RED
        return RouletteGame.BLACK

    def play_round(self) -> GameResult:
        self.number = random.randint(cfg.ROULETTE_MIN_NUMBER, cfg.ROULETTE_MAX_NUMBER) # рандомное число
        self.color = self.get_number_color(self.number) # определение цвета 
        self.win_amount = self.calculate_result() # подсчёт выигрыша
        self.is_win = self.win_amount > 0 # если выигрыш > 0 то ура победа, если 0, то значит плак плак

        return GameResult(
            game="roulette",
            bet=self.bet,
            bet_type=self.bet_type,
            bet_value=self.bet_value,
            number=self.number,
            color=self.color,
            is_win=self.is_win,
            win_amount=self.win_amount,
            balance_change=self.get_balance_change(),
        )

    # что я наделал 0_о
    def calculate_result(self) -> int:
        if self.number is None or self.color is None:
            return 0
        if self.bet_type == self.NUMBER_BET:
            if self.number == int(self.bet_value):
                return self.bet * cfg.ROULETTE_NUMBER_PAYOUT_MULTIPLIER
            return 0
        if self.bet_type == self.COLOR_BET:
            if self.color == self.bet_value:
                return self.bet * cfg.ROULETTE_OUTSIDE_BET_PAYOUT_MULTIPLIER
            return 0
        if self.bet_type == self.EVEN_ODD_BET:
            if self.number == cfg.ROULETTE_MIN_NUMBER:
                return 0
            if self.bet_value == self.EVEN and self.number % 2 == 0:
                return self.bet * cfg.ROULETTE_OUTSIDE_BET_PAYOUT_MULTIPLIER
            if self.bet_value == self.ODD and self.number % 2 != 0:
                return self.bet * cfg.ROULETTE_OUTSIDE_BET_PAYOUT_MULTIPLIER
            return 0
        return 0

    def _validate_bet_choice(self) -> None: # _ внутренний метод класса. тут полная проверка на дурака
        if self.bet_type == self.NUMBER_BET:
            if not isinstance(self.bet_value, int):
                raise ValueError("для ставки на число нужно передать int")
            if not cfg.ROULETTE_MIN_NUMBER <= self.bet_value <= cfg.ROULETTE_MAX_NUMBER:
                raise ValueError(
                    f"число в рулетке должно быть от {cfg.ROULETTE_MIN_NUMBER} до {cfg.ROULETTE_MAX_NUMBER}"
                )
            return
        if self.bet_type == self.COLOR_BET:
            if self.bet_value not in self.COLORS:
                raise ValueError("цвет должен быть red black или green")
            return
        if self.bet_type == self.EVEN_ODD_BET:
            if self.bet_value not in self.EVEN_ODD_VALUES:
                raise ValueError("значение должно быть even или odd")
            return
        raise ValueError("тип ставки должен быть number color или even_odd")
