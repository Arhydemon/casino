from database.database_manager import DatabaseManager
from models.statistics import Statistics

class StatisticsRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_statistics(self) -> Statistics | None:
        row = self.db.fetchone("SELECT * FROM statistics LIMIT 1")
        if row is None:
            return None
        return Statistics(
            games_played=row["games_played"],
            wins=row["wins"],
            total_win=row["total_win"],
        )

    def create_statistics(self) -> int:
        return self.db.insert(
            """
            INSERT INTO statistics (games_played, wins, total_win)
            VALUES (?, ?, ?)
            """,
            (0, 0, 0),
        )

    def save_statistics(self, statistics: Statistics) -> None:
        self.db.execute(
            """
            UPDATE statistics
            SET games_played = ?,
                wins = ?,
                total_win = ?
            WHERE id = (
                SELECT id FROM statistics
                ORDER BY id
                LIMIT 1
            )
            """,
            (
                statistics.games_played,
                statistics.wins,
                statistics.total_win,
            ),
        )

    def reset_statistics(self) -> None:
        self.db.execute(
            """
            UPDATE statistics
            SET games_played = ?,
                wins = ?,
                total_win = ?
            WHERE id = (
                SELECT id FROM statistics
                ORDER BY id
                LIMIT 1
            )
            """,
            (0, 0, 0),
        )
