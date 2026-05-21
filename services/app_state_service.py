from config import DEFAULT_BALANCE
from database.database_manager import DatabaseManager
from models.app_state import AppState
from repositories.profile_repository import ProfileRepository
from repositories.settings_repository import SettingsRepository
from repositories.statistics_repository import StatisticsRepository

class AppStateService:
    def __init__(self, db: DatabaseManager) -> None:
        self.profile_repository = ProfileRepository(db)
        self.statistics_repository = StatisticsRepository(db)
        self.settings_repository = SettingsRepository(db)

    def load_state(self) -> AppState:
        player = self.profile_repository.get_profile()
        if player is None:
            self.profile_repository.create_profile("Ватрушка", DEFAULT_BALANCE)
            player = self.profile_repository.get_profile()
        statistics = self.statistics_repository.get_statistics()
        if statistics is None:
            self.statistics_repository.create_statistics()
            statistics = self.statistics_repository.get_statistics()
        settings = self.settings_repository.get_settings()
        if settings is None:
            self.settings_repository.create_settings(1)
            settings = self.settings_repository.get_settings()
        if player is None or statistics is None or settings is None:
            raise RuntimeError("не удалось загрузить состояние приложения")
        return AppState(
            player=player,
            statistics=statistics,
            settings=settings,
        )

    def save_state(self, state: AppState) -> None:
        self.profile_repository.update_balance(state.player.balance)
        self.statistics_repository.save_statistics(state.statistics)
        self.settings_repository.save_settings(state.settings)
