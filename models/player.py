from models.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, login: str, balance: int) -> None:
        self.login = login
        self.balance = balance

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str) -> None:
        self._login = value

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        self._balance = int(value)

    # этот метод обязателен из-за BaseEntity
    def compare_value(self):
        return self.balance

    # этот метод обязателен из-за BaseEntity
    def display_text(self) -> str:
        return f"{self.login}: {self.balance}"
