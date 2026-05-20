from config import DEFAULT_BALANCE
from database.database_manager import DatabaseManager
from repositories.profile_repository import ProfileRepository
from repositories.settings_repository import SettingsRepository
from repositories.statistics_repository import StatisticsRepository

def main() -> None:
    with DatabaseManager() as db:
        db.create_tables()
        # создаю репозитории - это класс, который работает с конкретной таблицей
        profile_repository = ProfileRepository(db)
        statistics_repository = StatisticsRepository(db)
        settings_repository = SettingsRepository(db)

        # проверка есть ли профиль игрока
        profile = profile_repository.get_profile()
        if profile is None:
            profile_repository.create_profile(
                login="Ватрушка",
                balance=DEFAULT_BALANCE,
            )
            print("Создан новый профиль")
        
        # поверка есть ли статистика.
        statistics = statistics_repository.get_statistics()
        if statistics is None:
            statistics_repository.create_statistics()
            print("Создана начальная статистика")

        settings = settings_repository.get_settings()
        if settings is None:
            settings_repository.create_settings()
            print("Созданы настройки по умолчанию")
    print("База данных готова")

if __name__ == "__main__":
    main()