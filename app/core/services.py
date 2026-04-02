from app.app_state import AppState, Player
from app.core.database import DatabaseManager
from app.core.repositories import ProfileRepository, StatisticsRepository, SettingsRepository

class AppStateService:
    def __init__(self):
        self.db = DatabaseManager() # создаётся объект для работы с БД
        self.profile_repository = ProfileRepository(self.db) # cоздаётся репозиторий профиля, которому передаётся db
        self.statistics_repository = StatisticsRepository(self.db) # такая же хуйня как выше
        self.settings_repository = SettingsRepository(self.db)

    def initialize_database(self) -> None:
        self.db.initialize()

    def load_state(self) -> AppState:
        profile = self.profile_repository.get_profile()
        if profile is None:
            profile = self.profile_repository.create_default_profile()
        statistics = self.statistics_repository.get_statistics(profile.id)
        settings = self.settings_repository.get_settings(profile.id)
        state = AppState() # создаём объект состояния приложения
        state.player = Player(name=profile.name, balance=profile.balance)

        if statistics is not None:
            pass
        if settings is not None:
            pass
        return state

    def save_state(self, state: AppState) -> None:
        profile = self.profile_repository.get_profile()
    
        if profile is None:
            profile = self.profile_repository.create_default_profile()
    
        self.profile_repository.update_balance(
            profile.id,
            state.player.balance
        )