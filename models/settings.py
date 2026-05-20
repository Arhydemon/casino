from database.database_manager import DatabaseManager
from models.settings import Settings


class SettingsRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_settings(self) -> Settings | None:
        row = self.db.fetchone("SELECT * FROM settings LIMIT 1")
        if row is None:
            return None
        return Settings(
            sound_enabled=row["sound_enabled"],
        )

    def create_settings(self, sound_enabled: int = 0) -> int:
        return self.db.insert(
            "INSERT INTO settings (sound_enabled) VALUES (?)",
            (sound_enabled,),
        )

    def save_settings(self, settings: Settings) -> None:
        self.db.execute(
            """
            UPDATE settings
            SET sound_enabled = ?
            WHERE id = (
                SELECT id FROM settings
                ORDER BY id
                LIMIT 1
            )
            """,
            (settings.sound_enabled,),
        )