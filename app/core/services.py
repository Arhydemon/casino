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
            state.games_played = statistics.games_played
            state.games_won = statistics.games_won
            state.total_win = statistics.total_win

        if settings is not None:
            state.sound_enabled = settings.sound_enabled
            return state

    def save_state(self, state: AppState) -> None:
        profile = self.profile_repository.get_profile()

        if profile is None:
            profile = self.profile_repository.create_default_profile()

        # баланс
        self.profile_repository.update_balance(
            profile.id,
            state.player.balance
        )

        # статистика
        self.statistics_repository.update_statistics(
            profile_id=profile.id,
            games_played=state.games_played,
            games_won=state.games_won,
            total_win=state.total_win
        )

        # настройки (пока только звук)
        self.settings_repository.update_sound(
            profile_id=profile.id,
            sound_enabled=state.sound_enabled
        )