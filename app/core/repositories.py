# слой, который работает с базой данных, если его не будет, то sql придется везде писать и я заебусь
from app.core.database import DatabaseManager
from app.core.models import *
# настоебал этот sql уже
# ПРОФИЛЬ
class ProfileRepository: # репозиторий для работы с таблицей profile
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_profile(self) -> ProfileModel | None:
        with self.db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, balance FROM profile LIMIT 1")
            row = cursor.fetchone
            
            if row in None:
                return None
            
            return ProfileModel(
                id=row["id"],
                name=row['name'],
                balance=row['balance']
            )
        
    def create_default_profile(self) -> ProfileModel:
        # создание профиля по умолчанию
        with self.db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO profile (name, balance)
                VALUES (?, ?)
                """, ("Игрок", 1000))
            
            # сохранение id созданного ТОЛЬКО ЧТО ПРОФИЛЯ
            profile_id = cursor.lastrowid

            # СРАЗУ ЖЕ создаем связанную статистику для этого профиля
            cursor.execute("""
                INSERT INTO statistics (profile_id, games_played, games_won, total_win)
                VALUES (?, ?, ?, ?)
            """, (profile_id, 0, 0, 0))

            # создаю настройки по умолчанию для этого профиля 
            cursor.execute("""
                INSERT INTO settings (profile_id, sound_enabled, theme)
                VALUES (?, ?, ?)
            """, (profile_id, 1, "dark"))

            connection.commit()  # сохранение всей этой хуйни
            return ProfileModel(
                id=profile_id,
                name='Обезьяна ебаная',
                balance=1000
            )
        
    def update_balance(self, profile_id: int, new_balance: int) -> None:
        with self.db.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE profile
                SET balance = ?
                WHERE id = ?
            """, (new_balance, profile_id))
            
            connection.commit()

class StatisticsRepository: # репозиторий для работы с таблицей statistics
    def __init__(self, db: DatabaseManager):
        self.db = db

        def get_statistics(self, profile_id: int) -> StatisticsModel | None: # получаем статистику по id профиля
            with self.db.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, profile_id, games_played, games_won, total_win
                    FROM statistics
                    WHERE profile_id = ?
                """, (profile_id,))

                row = cursor.fetchone()
                if row is None:
                    return None
                
                return StatisticsModel(
                id=row["id"],
                profile_id=row["profile_id"],
                games_played=row["games_played"],
                games_won=row["games_won"],
                total_win=row["total_win"]
            )

    def update_statistics(
        self,
        profile_id: int,
        games_played: int,
        games_won: int,
        total_win: int
    ) -> None:
        # обновляю статистику игрока
        with self.db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE statistics
                SET games_played = ?, games_won = ?, total_win = ?
                WHERE profile_id = ?
            """, (games_played, games_won, total_win, profile_id))
            connection.commit()

class SettingsRepository: # репозиторий для работы с таблицей settings
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_settings(self, profile_id: int) -> SettingsModel | None: # настройки конкретного профиля
        with self.db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, profile_id, sound_enabled, theme
                FROM settings
                WHERE profile_id = ?
            """, (profile_id,))
            row = cursor.fetchone()
            if row is None:
                return None

            # sound_enabled хранится в БД как 0 или 1, поэтому преобразуем в bool
            return SettingsModel(
                id=row["id"],
                profile_id=row["profile_id"],
                sound_enabled=bool(row["sound_enabled"]),
                theme=row["theme"]
            )

    def update_sound(self, profile_id: int, sound_enabled: bool) -> None: # со звуком работа
        with self.db.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE settings
                SET sound_enabled = ?
                WHERE profile_id = ?
            """, (int(sound_enabled), profile_id))
            connection.commit()