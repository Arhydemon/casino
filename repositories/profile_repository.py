from database.database_manager import DatabaseManager
from models.player import Player # превращение данных полученные из БД


class ProfileRepository: # СВЯЗЬ МЕЖДУ ТАБЛИЦЕЙ profile И КЛАССОМ Player! получает игрока из БД, создаёт профиль и обновляет баланс
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_profile(self) -> Player | None:
        row = self.db.fetchone("SELECT * FROM profile LIMIT 1")
        if row is None:
            return None
        return Player(
            login=row["login"],
            balance=row["balance"],
        )

    def create_profile(self, login: str, balance: int) -> None:
        self.db.execute(
            "INSERT INTO profile (login, balance) VALUES (?, ?)",
            (login, balance),
        )

    def update_balance(self, balance: int) -> None:
        self.db.execute(
            """
            UPDATE profile
            SET balance = ?
            WHERE id = (
                SELECT id FROM profile
                ORDER BY id
                LIMIT 1
            )
            """,
            (balance,),
        )
