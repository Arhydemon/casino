class Player:
    def __init__(self, login: str, balance: int) -> None:
        self._login = login
        self._balance = balance
    @property
    def login(self) -> str:
        return self._login

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        if value >= 0:
            self._balance = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.login == other.login

    def __lt__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.balance < other.balance
