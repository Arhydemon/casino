from pathlib import Path
import sqlite3

from config import DB_PATH


class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH) -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        with self._connection:
            return self._connection.execute(query, params)

    def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        cursor = self._connection.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        cursor = self._connection.execute(query, params)
        return cursor.fetchall()

    def insert(self, query: str, params: tuple = ()) -> int:
        cursor = self.execute(query, params)
        return cursor.lastrowid

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

    def __enter__(self) -> "DatabaseManager":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()