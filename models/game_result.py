from models.base_entity import BaseEntity

# отчёт о результатах игры
# типа какая игра, какая ставка, выиграл или нет, сколько выиграл, как изменился баланс, что выпало вот
class GameResult(BaseEntity):
    def __init__( # вызывается при result = GameResult(...)
        self,
        game: str, # название игрульки
        bet: int, # ставочка
        is_win: bool,
        win_amount: int,
        balance_change: int,
        # это были обязательные выше
        bet_type: str = "", # тип ставки
        bet_value: int | str = "", 
        number: int | None = None,
        color: str = "",
        reels: list[str] | None = None, # символы на слотах
        balance: int = 0,
    ) -> None:
        self.game = game # название игры, работает сеттер на гейм
        self.bet = bet # сеттер ставочки
        self.is_win = is_win
        self.win_amount = win_amount
        self.balance_change = balance_change
        self.bet_type = bet_type # 
        self.bet_value = bet_value 
        self.number = number
        self.color = color
        self.reels = reels or []
        self.balance = balance

    @property
    def game(self) -> str:
        return self._game

    @game.setter
    def game(self, value: str) -> None:
        self._game = value

    @property
    def bet(self) -> int:
        return self._bet

    @bet.setter
    def bet(self, value: int) -> None:
        self._bet = int(value)

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

    @property
    def balance_change(self) -> int:
        return self._balance_change

    @balance_change.setter
    def balance_change(self, value: int) -> None:
        self._balance_change = int(value)

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        self._balance = int(value)

    @property
    def bet_type(self) -> str:
        return self._bet_type

    @bet_type.setter
    def bet_type(self, value: str) -> None:
        self._bet_type = value

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
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    @property
    def reels(self) -> list[str]:
        return self._reels

    @reels.setter
    def reels(self, value: list[str]) -> None:
        self._reels = value

    def compare_value(self):
        return self.win_amount

    def display_text(self) -> str:
        return f"{self.game}: {self.win_amount}"
