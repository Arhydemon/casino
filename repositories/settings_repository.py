from database.database_manager import DatabaseManager
from models.settings import Settings
from settings import Config as cfg


class SettingsRepository: # СВЯЗЬ МЕЖДУ ТАБЛИЦЕЙ settings И ОБЪЕКТОМ Settings! тупо звук создаём и всё впринципе
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_settings(self) -> Settings | None:
        row = self.db.fetchone("SELECT * FROM settings LIMIT 1")
        if row is None:
            return None
        return Settings(
            sound_enabled=bool(row["sound_enabled"]),
        )

    def create_settings(
        self, sound_enabled: bool = bool(cfg.DEFAULT_SOUND_ENABLED)
    ) -> None:
        self.db.execute(
            "INSERT INTO settings (sound_enabled) VALUES (?)",
            (int(sound_enabled),),
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
            (int(settings.sound_enabled),),
        )
