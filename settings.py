from models.base_entity import BaseEntity


class ConfigMap(BaseEntity): # СВОЯ УПРОЩЁННАЯ ВЕРСИЯ СЛОВАРЯ! хранит пары ключ значение внутри кортежа
    def __init__(self, pairs: tuple[tuple[object, object], ...]) -> None: # внешний кортеж хранит все пары, а # внутренний кортеж хранит ключ и значение
        # ... значит что таких пар может быть сколько угодно
        self.pairs = pairs

    @property
    def pairs(self) -> tuple[tuple[object, object], ...]:
        return self._pairs

    @pairs.setter
    def pairs(self, value: tuple[tuple[object, object], ...]) -> None:
        self._pairs = value

    def __iter__(self): # это магический метод который делает объект перебираемым!!! позволяет перебирать ConfigMap через for
        for key, value in self.pairs: # распаковка каждой пары на key и value
            yield key # yield по одному возвращает каждый ключ и запоминает где остановился цикл

    def keys(self) -> tuple: # возвращает кортеж со всеми ключами
        return tuple(key for key, value in self.pairs) # проходит по всем ключам и берёт только кий

    def get(self, key, default=None): # ищет значение по ключу
        for item_key, value in self.pairs:
            if item_key == key:
                return value
        return default

    def __getitem__(self, key): # обращение через [] чтобы обращаться как к списку или словарю, решил повыёживаться, pairs у меня не словарь и поэтому падает по другому
        for item_key, value in self.pairs:
            if item_key == key:
                return value
        raise KeyError(key)

    def compare_value(self):
        return len(self.pairs)

    def display_text(self) -> str:
        return f"элементов: {len(self.pairs)}"


class Config:
    APP_TITLE = "дым дым казино" # название окна приложения
    APP_MENU_TITLE = "Казик" # заголовок главного меню

    DB_PATH = "database/app.db" # путь до SQLite-базы
    LOG_PATH = "log.txt" 
    ASSETS_DIR = "assets"
    TEXT_ENCODING = "utf-8" # кодировка для нормальной работы русского текста на всякий
    LOG_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S" # день.месяц.год часы:минуты:секунды

    DEFAULT_PLAYER_LOGIN = "Макарончик" # логин нового игрока по умолчанию
    DEFAULT_BALANCE = 1000 # начальный баланс нового игрока
    DEFAULT_SOUND_ENABLED = True # звук по умолчанию включён

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    WINDOW_MAXIMIZED = True # сразу развернуть окно на весь экран
    WINDOW_PREVENT_CLOSE = False # False - окно можно закрыть обычным способом
    THEME_MODE = "dark" # тёмная тема приложения
    FONT_FAMILY = "Segoe UI" # основной шрифт
    BODY_TEXT_SIZE = 14 # размер обычного текста
    TITLE_TEXT_SIZE = 24 # размер текста заголовков

    MIN_BET = 1 # минимальная разрешённая ставка
    DEFAULT_BET = 100 # ставка, которая сразу показана в поле ввода

    SOUND_SPIN_TRACK = "sounds/roulette_spin.mp3" # можно на чё угодно поменять, ток название надо такое
    SOUND_VOLUME = 1000 # громкость звука для Windows MCI значение 1000 максимум
    
    # минимальное и максимальное число рулетки
    ROULETTE_MIN_NUMBER = 0
    ROULETTE_MAX_NUMBER = 36
    ROULETTE_RED_NUMBERS = {
        1,
        3,
        5,
        7,
        9,
        12,
        14,
        16,
        18,
        19,
        21,
        23,
        25,
        27,
        30,
        32,
        34,
        36,
    }
    ROULETTE_WHEEL_ORDER = (
        0,
        32,
        15,
        19,
        4,
        21,
        2,
        25,
        17,
        34,
        6,
        27,
        13,
        36,
        11,
        30,
        8,
        23,
        10,
        5,
        24,
        16,
        33,
        1,
        20,
        14,
        31,
        9,
        22,
        18,
        29,
        7,
        28,
        12,
        35,
        3,
        26,
    )
    ROULETTE_NUMBER_PAYOUT_MULTIPLIER = 35 # ставка на конкретное число умножается на 35
    ROULETTE_OUTSIDE_BET_PAYOUT_MULTIPLIER = 1 # ставка на цвет или чётность умножается на 1
    ROULETTE_SPIN_DURATION_SECONDS = 5 # рулетка крутится 5 секунд ЗА КАКОЕ ВРЕМЯ шарик должен добраться до результата
    ROULETTE_SPIN_EXTRA_TURNS = 5 # перед остановкой шарик делает 5 дополнительных кругов СКОЛЬКО ПОЛНЫХ КРУГОВ он сделает по дороге
    ROULETTE_EASING_POWER = 3 # отвечает за плавное замедление шарика
    ROULETTE_SPIN_FPS = 60 # обновлений анимации в секунду
    ROULETTE_MIN_ANIMATION_STEPS = 24 # минимальное количество шагов анимации

    SLOT_SYMBOLS = ConfigMap(
        (
            ("cherry", "🍒"),
            ("lemon", "🍋"),
            ("bell", "🔔"),
            ("star", "⭐"),
            ("seven", "7"),
        )
    )
    SLOT_REEL_COUNT = 3 # количество барабанов в слотах
    SLOT_PAYTABLE = ConfigMap(((3, 5), (2, 2))) # таблица выплат
    SLOTS_SPIN_DURATION_SECONDS = 4 # длительность крутки
    SLOT_SPIN_STEPS_PER_SECOND = 22 # количество смен символов за секунду
    SLOT_SPIN_PHASE_MODULO = 2 # каждые два шага повторяется цикл анимации
    # чётный шаг - барабан увеличен и наклонён вправо
    # нечётный шаг - обычный размер и наклон влево
    SLOT_REEL_SCALE_ACTIVE = 1.04 # размер барабана на активном шаге
    SLOT_REEL_SCALE_IDLE = 1.0 # размер барабана на обычном шаге 
    SLOT_REEL_ROTATION_ACTIVE = 0.015 # наклон барабана вправо на активном шаге
    SLOT_REEL_ROTATION_IDLE = -0.015 # наклон барабана влево на обычном шаге
