from dataclasses import dataclass  # позволяет быстро создавать классы без ебли

# прикол моделей в том, чтобы хранить в них данные из базы данных, без них ебанешься
# Модель = структура данных + представление сущности
@dataclass
class ProfileModel: # профиль игрока
    id: int # уникальный id игрока в базе
    name: str # имя игрока
    balance: int # баланс игрока

@dataclass
class StatisticsModel: # статистика
    id: int
    profile_id: int # к какому игроку относится
    games_played: int # скок игр сыграно
    games_won: int # скок игр выиграно
    total_win: int # общий выигрыш 

@dataclass
class SettingsModel:
    id: int
    profile_id: int # к кому настройки относятся надеюсь не заебланил
    sound_enabled: bool # включен ли звук
    theme: str # какая тема