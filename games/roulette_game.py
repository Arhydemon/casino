import random
from games.base_game import BaseGame

class RouletteGame(BaseGame):
    RED_NUMBERS = {
        1,
        3,
        5,
        7,
        9,
        12,
        14,
        16,
        18,
        19,
        21,
        23,
        25,
        27,
        30,
        32,
        34,
        36,
    }

    # здесь хранит параметры ставки и проверяет их на старте
    def __init__(self, bet: int, bet_type: str, bet_value: int | str) -> None:
        super().__init__(bet)
        # сам тип ставки number color even_odd
        self.bet_type = bet_type
        # в этом месте значение ставки например 7 или red
        self.bet_value = bet_value
        # тут будет выпавшее число после прокрутки
        self.number: int | None = None
        # здесь будет цвет выпавшего числа
        self.color: str | None = None
        # сам сразу валидирует входные данные
        self._validate_bet_choice()

    @staticmethod
    def get_number_color(number: int) -> str:
        if number == 0:
            return "green"
        if number in RouletteGame.RED_NUMBERS:
            return "red"
        return "black"

    # тут крутит раунд и возвращает полный словарь результата
    def play_round(self) -> dict:
        # здесь имитируем выпадение числа на рулетке
        self.number = random.randint(0, 36)
        # сам считаем цвет по таблице
        self.color = self.get_number_color(self.number)
        # в этом месте считаем выплату по правилам ставки
        self.win_amount = self.calculate_result()
        # тут выставляем флаг победы
        self.is_win = self.win_amount > 0

        # здесь нужна ui чтобы показать все детали раунда
        return {
            "game": "roulette",
            "bet": self.bet,
            "bet_type": self.bet_type,
            "bet_value": self.bet_value,
            "number": self.number,
            "color": self.color,
            "is_win": self.is_win,
            "win_amount": self.win_amount,
            "balance_change": self.get_balance_change(),
        }

    # сам считает выигрыш по типу ставки
    def calculate_result(self) -> int:
        if self.number is None or self.color is None:
            return 0
        # логика для ставки на точное число
        if self.bet_type == "number":
            if self.number == int(self.bet_value):
                return self.bet * 35
            return 0
        # тут логика для ставки на цвет
        if self.bet_type == "color":
            if self.color == self.bet_value:
                return self.bet
            return 0
        # для ставки на четность
        if self.bet_type == "even_odd":
            if self.number == 0:
                return 0
            if self.bet_value == "even" and self.number % 2 == 0:
                return self.bet
            if self.bet_value == "odd" and self.number % 2 != 0:
                return self.bet
            return 0
        return 0
    # сам сбрасывает состояние объекта перед новым использованием
    def reset(self) -> None:
        self.number = None
        self.color = None
        self.is_win = False
        self.win_amount = 0
    # в этом месте валидирует корректность ставки чтобы не ловить мусор
    def _validate_bet_choice(self) -> None:
        if self.bet_type == "number":
            if not isinstance(self.bet_value, int):
                raise ValueError("для ставки на число нужно передать int")
            if not 0 <= self.bet_value <= 36:
                raise ValueError("число в рулетке должно быть от 0 до 36")
            return
        if self.bet_type == "color":
            if self.bet_value not in ("red", "black", "green"):
                raise ValueError("цвет должен быть red black или green")
            return
        if self.bet_type == "even_odd":
            if self.bet_value not in ("even", "odd"):
                raise ValueError("значение должно быть even или odd")
            return
        raise ValueError("тип ставки должен быть number color или even_odd")
