import sqlite3
from config import DB_PATH


class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row # аналог словарика, доступ к колонкам по имени

    def execute(self, query: str, params: tuple = ()) -> None: # выполняет запрос и автоматически делает commit/rollback
        with self._connection:
            self._connection.execute(query, params)

    def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None: # возвращает одну строку или None 
        cursor = self._connection.execute(query, params)
        return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()) -> list[sqlite3.Row]: # возвращает список строк
        cursor = self._connection.execute(query, params)
        return cursor.fetchall()
    
    def create_tables(self) -> None:
        self.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            balance INTEGER NOT NULL
        )""")

        self.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            games_played INTEGER NOT NULL,
            wins INTEGER NOT NULL,
            total_win INTEGER NOT NULL
        )""")

        self.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sound_enabled INTEGER NOT NULL
        )""")

    def close(self) -> None:
        self._connection.close()