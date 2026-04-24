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
    def balance(self, value: int) -> int:
        if value >= 0:
            self._balance = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player): # если other НЕ является Player ТО сразу False
            return False
        return self.login == other.login # иначе они равны
    
    def __ls__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.balance < other.balance