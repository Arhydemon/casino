class Statistics:
    def __init__(self, games_played: int, wins: int, total_win: int) -> None:
        self.games_played = games_played
        self.wins = wins
        self.total_win = total_win

    def add_game(self) -> None:
        self.games_played += 1
    
    def add_win(self, win_amount: int) -> None:
        self.wins += 1
        self.total_win = win_amount + self.total_win
        
    def reset(self) -> None:
        self.games_played = 0
        self.wins = 0
        self.total_win = 0