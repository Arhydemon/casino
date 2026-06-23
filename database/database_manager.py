from pathlib import Path # Path нужен для изячной работы с путями и папками
import sqlite3
from settings import Config as cfg


class DatabaseManager: # ГЛАВНЫЙ КЛАСС ДЛЯ РАБОТЫ С БАЗОЙ! подключается к app.db, выполняет SQL и создаёт таблицы
    def __init__(self, db_path: str = cfg.DB_PATH) -> None: # database/app.db
        Path(db_path).parent.mkdir(parents=True, exist_ok=True) # превращает строку в объект пути
        # .parent получает родительскую папку, .mkdir() создаёт эту папку
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    def execute(self, query: str, # SQL запрос
                params: tuple = ()) -> sqlite3.Cursor: # значения для знаков ? в запросе то есть плейсхолдеров
        # курсор эта объект с результатом выполненного запроса
        with self._connection: # with автоматически сохраняет изменения в БД
            return self._connection.execute(query, params)

    def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None: # fetchone() берёт только одну найденную строку
        cursor = self._connection.execute(query, params)
        return cursor.fetchone()

    def create_tables(self) -> None: # создаёт все необходимые таблицы
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            balance INTEGER NOT NULL
        )"""
        )
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            games_played INTEGER NOT NULL,
            wins INTEGER NOT NULL,
            total_win INTEGER NOT NULL
        )"""
        )
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sound_enabled INTEGER NOT NULL
        )"""
        )

    def close(self) -> None:
        self._connection.close()
