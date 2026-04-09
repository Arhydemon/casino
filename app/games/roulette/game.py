import random
from dataclasses import dataclass
from app.app_state import AppState

# что конкретно выпало на спине
@dataclass
class SpinResult:
    number: int
    color: str

# итог одного раунда рулетки
@dataclass
class RouletteRoundResult:
    spin_result: SpinResult
    is_win: bool
    win_amount: int
    message: str

class RouletteGame:
    # красные числа рулетки, чтобы каждый раз не ебаться
    RED_NUMBERS = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36
    }

    def __init__(self, state: AppState):
        self.state = state

    # определяем цвет выпавшего числа
    def get_color(self, number: int) -> str:
        if number == 0:
            return "green"
        if number in self.RED_NUMBERS:
            return "red"
        return "black"

    # обычный честный спин
    def spin(self) -> SpinResult:
        number = random.randint(0, 36)
        return SpinResult(number=number, color=self.get_color(number))

    # спин с уже известным числом
    # нужен чтобы анимация и логика не дрались друг с другом как долбоебы
    def spin_with_number(self, forced_number: int) -> SpinResult:
        return SpinResult(
            number=forced_number,
            color=self.get_color(forced_number)
        )

    # проверка на чет
    def is_even(self, number: int) -> bool:
        return number != 0 and number % 2 == 0

    # проверка на нечет
    def is_odd(self, number: int) -> bool:
        return number != 0 and number % 2 != 0

    # сколько накинуть сверху
    def calculate_win_amount(self, bet_type: str, amount: int) -> int:
        if bet_type == "number":
            return amount * 35
        if bet_type in ["color", "even", "odd"]:
            return amount
        return 0

    # проверяем попал или нет
    def check_win(self, spin_result: SpinResult, bet_type: str, bet_value) -> bool:
        if bet_type == "number":
            return spin_result.number == bet_value

        if bet_type == "color":
            return spin_result.color == bet_value

        if bet_type == "even":
            return self.is_even(spin_result.number)

        if bet_type == "odd":
            return self.is_odd(spin_result.number)

        return False

    # обычный раунд без заранее известного результата
    def play_round(self, bet_type: str, bet_value, amount: int):
        spin_result = self.spin()
        return self._resolve_round(spin_result, bet_type, bet_value, amount)

    # раунд с уже известным числом из анимации
    def play_round_with_result(self, bet_type: str, bet_value, amount: int, forced_number: int):
        spin_result = self.spin_with_number(forced_number)
        return self._resolve_round(spin_result, bet_type, bet_value, amount)

    # тут уже вся грязная работа с балансом
    def _resolve_round(self, spin_result: SpinResult, bet_type: str, bet_value, amount: int):
        if amount <= 0:
            self.state.last_result = "Ставка должна быть больше нуля пжпжпж"
            return None

        if amount > self.state.player.balance:
            self.state.last_result = "Недостаточно средств нищенка"
            return None

        # сначала забираем ставку
        self.state.player.withdraw(amount)
        is_win = self.check_win(spin_result, bet_type, bet_value)

        if is_win:
            pure_win = self.calculate_win_amount(bet_type, amount)
            # возвращаем ставку + сверху выигрыш
            self.state.player.deposit(amount + pure_win)
            self.state.last_result = (
                f"Выпало {spin_result.number} "
                f"({self.translate_color(spin_result.color)}). "
                f"Ты выиграл {pure_win}!"
            )

            return RouletteRoundResult(
                spin_result=spin_result,
                is_win=True,
                win_amount=pure_win,
                message=self.state.last_result
            )

        self.state.last_result = (
            f"Выпало {spin_result.number} "
            f"({self.translate_color(spin_result.color)}). "
            f"Ты проебал {amount}."
        )

        return RouletteRoundResult(
            spin_result=spin_result,
            is_win=False,
            win_amount=0,
            message=self.state.last_result
        )

    # перевод цвета в нормальный человеческий вид
    def translate_color(self, color: str) -> str:
        if color == "red":
            return "красный"
        if color == "black":
            return "чёрный"
        if color == "green":
            return "зелёный"
        return color