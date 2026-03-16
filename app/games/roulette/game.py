import random
from dataclasses import dataclass
from app.app_state import AppState

@dataclass
class RSR: #ROULETTE SPIN RESULT
    number: int
    color: str

class RouletteGame: #йоу
    RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
    GREEN_NUMBERS = {0}
    BET_TYPES = {"number", "color", "even", "odd"}

    def __init__(self, state: AppState):
        self.state = state
        self.last_spin = None

    def get_color(self, number: int) -> str:
        if number in self.GREEN_NUMBERS:
            return "green"
        if number in self.RED_NUMBERS:
            return "red"
        return "black"
    
    def spin(self) -> RSR:
        number = random.randint(0,36)
        color = self.get_color(number)
        result = RSR(number, color)
        self.last_spin = result
        return result
    
    def check_win(self, bet_type: str, bet_value, result:RSR ) -> bool:
        if bet_type == "color":
            return result.color == bet_value
        if bet_type == "number":
            return result.number == bet_value
        if bet_type == "even":
            return result.number != 0 and result.number % 2 == 0
        if bet_type == "odd":
            return result.number != 0 and result.number % 2 == 1
        return False
    
    def calculate_win(self, bet_type: str, amount: int) -> int:
        if bet_type == "number":
            return amount * 35
        if bet_type in {"color", "even", "odd"}:
            return amount 
        return 0
    
    def play_round(self, bet_type: str, bet_value, amount: int): # я ёбнулся пока писал это
        result = self.spin()
        if not self.state.player.withdraw(amount):
            self.state.last_result = "пошёл нахуй, нищенка"
            return None #zazazaza
        
        win = self.check_win(bet_type, bet_value, result)
        if win:
            win_amount = self.calculate_win(bet_type, amount)
            self.state.player.deposit(amount + win_amount)
            self.state.last_result = f"выпало {result.number} ({result.color}) | выигрыш {win_amount}"
        else:
            self.state.last_result = f"выпало {result.number} ({result.color}) | проигрыш {amount}"
        return result