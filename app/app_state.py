from dataclasses import dataclass, field # чтобы не ебаться с классами

@dataclass
class Player:
    # ОПИСЫВАЕМ ИГРОКА 
    name: str ="Игрок" # имя долбаебика
    balance: int = 1000 # стартовый балик

    def deposit(self, amount: int) -> None: 
        if amount > 0: # amount - сумма, на которую нужно пополнить баланс
            self.balance += amount # если всё заебок, то прибавление суммы к балику

    def withdraw(self, amount: int) -> bool: # withdraw - вывести/снять бабки со счёта
        if amount <= 0:
            return False # нельзя списать ты чо еблан
        if amount > self.balance:
            return False # не ну ты вообще еблан блять
        self.balance -= amount
        return True 
    
@dataclass
class AppState:
    # ОБЩЕЕ СОСТОЯНИЕ ПРИЛОЖЕНИЯ ЙОУ
    player : Player = field(default_factory=Player) # default_factory создаёт нового игрока
    current_game : str = "menu" # текущая игра
    current_bet : int = 0 # текущая ставка 
    last_result : str = "" # ластовое сообщение о результатике

    def set_game(self, game_name: str) -> None:
        self.current_game = game_name

    def set_bet(self, amount: int) -> bool:
        if amount <= 0:
            return False
        if amount > self.player.balance:
            return False
        self.current_bet = amount
        return True
    
    def clear_bet(self) -> None:
        self.current_bet = 0

    def win(self) -> bool:
        if self.current_bet <= 0:
            self.last_result = "Ставка не указана еблан"
            return False
        win_amount: int = self.current_bet
        self.player.deposit(win_amount)
        self.last_result = f"Вы выиграли {win_amount}" # а потом всё сольешь один хуй
        return True

    def lose(self) -> bool:
        if self.current_bet <= 0:
            self.last_result = "Ставка не указана еблан"
            return False
        lose_amount: int = self.current_bet
        if self.player.withdraw(lose_amount):
            self.last_result = f"Вы проебали {lose_amount}" # а я говорил нахуй
            return True
        self.last_result = "Недостаточно средств"
        return False
