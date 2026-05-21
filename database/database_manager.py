from pathlib import Path
import sqlite3
from config import DB_PATH

class DatabaseManager:
    # тут поднимает подключение к sqlite и подготавливает работу с row объектами
    def __init__(self, db_path: str = DB_PATH) -> None:
        # здесь заранее создает папку под базу чтобы не словить ошибку по пути
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        # сам открывает живое соединение с файлом базы
        self._connection = sqlite3.connect(db_path)
        # в этом месте делает доступ к колонкам по имени а не по индексу
        self._connection.row_factory = sqlite3.Row

    # исполняет запрос на изменение данных КАК УГОДНО ПО ТИПУ insert/update/delete/create
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        # здесь оборачивает команду в транзакцию с автокомитом
        with self._connection:
            return self._connection.execute(query, params)
        
    # тянет ровно одну строку из базы
    def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        cursor = self._connection.execute(query, params)
        return cursor.fetchone()

    # список строк из базы
    def fetchall(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        cursor = self._connection.execute(query, params)
        return cursor.fetchall()

    # insert и возвращает id вставленной записи
    def insert(self, query: str, params: tuple = ()) -> int:
        # здесь просто переиспользует общий execute чтобы не дублировать логику
        cursor = self.execute(query, params)
        # сам отдает lastrowid чтобы потом можно было привязыватьск записи
        return cursor.lastrowid

    # создаёт таблицы при первом запуске приложения
    def create_tables(self) -> None:
        # профиль игрока логин + баланс
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            balance INTEGER NOT NULL
        )"""
        )

        # здесь хранит статистику по играм
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            games_played INTEGER NOT NULL,
            wins INTEGER NOT NULL,
            total_win INTEGER NOT NULL
        )"""
        )

        # хранит пользовательские настройки
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sound_enabled INTEGER NOT NULL
        )"""
        )

    # закрывает подключение к базе
    def close(self) -> None:
        self._connection.close()

    # позволяет писать with DatabaseManager as db
    def __enter__(self) -> "DatabaseManager":
        return self

    # гарантирует закрытие соединенипосле блока with на сто миллионов процентов
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
