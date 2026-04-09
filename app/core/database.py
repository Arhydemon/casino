import sqlite3
from app.config import DATA_DIR, DATABASE_PATH


class DatabaseManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    """
    Это класс для работы с базой данных!!!
    ТУТ ЦЕНТР РАБОТЫ И ПОДКЛЮЧЕНИЯ К БД
    СОЗДАЁМ ТУТ ТАБЛИЧКИ
    А ЕЩЕ ТУТ ПРОЩЕ ТАК РАБОТАТЬ С ЛАЙТОМ
    """

    def connect(self) -> sqlite3.Connection: # создаёт соединение с SQLite.
        connection = sqlite3.connect(self.db_path) 
        connection.row_factory = sqlite3.Row # как словари а не кортежики
        return connection

    def initialize(self) -> None: # создание таблиц если их нихуя нет 
        with self.connect() as connection: # соединение с БД
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL DEFAULT 'Игрок',
                    balance INTEGER NOT NULL DEFAULT 10000
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    games_played INTEGER NOT NULL DEFAULT 0,
                    games_won INTEGER NOT NULL DEFAULT 0,
                    total_win INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (profile_id) REFERENCES profile(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id INTEGER NOT NULL,
                    sound_enabled INTEGER NOT NULL DEFAULT 1,
                    theme TEXT NOT NULL DEFAULT 'dark',
                    FOREIGN KEY (profile_id) REFERENCES profile(id)
                )
            """)

            connection.commit()