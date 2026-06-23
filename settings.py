from models.base_entity import BaseEntity
from enum import Enum # Enum нужен чтобы сделать нормальный набор постоянных вариантов
from dataclasses import dataclass, field

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

class SlotSymbol(Enum): # вместо маппинга
    CHERRY = "🍒"
    LEMON = "🍋"
    BELL = "🔔"
    STAR = "⭐"
    SEVEN = "7"

def create_slot_paytable():
    return ConfigMap(((3, 5), (2, 2)))

# в томл долго переделывать, то есть там будет примерно: WINDOW_WIDTH = data["window"]["width"]
@dataclass(frozen=True)
class ConfigData:
    APP_TITLE: str = "дым дым казино" # название окна приложения
    APP_MENU_TITLE: str = "Казик" # заголовок главного меню

    DB_PATH: str = "database/app.db" # путь до SQLite-базы
    LOG_PATH: str = "log.txt" 
    ASSETS_DIR: str = "assets"
    TEXT_ENCODING: str = "utf-8" # кодировка для нормальной работы русского текста на всякий
    LOG_DATETIME_FORMAT: str = "%d.%m.%Y %H:%M:%S" # день.месяц.год часы:минуты:секунды

    DEFAULT_PLAYER_LOGIN: str = "Макарончик" # логин нового игрока по умолчанию
    DEFAULT_BALANCE: int = 1000 # начальный баланс нового игрока
    DEFAULT_SOUND_ENABLED: bool = True # звук по умолчанию включён

    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080
    WINDOW_MAXIMIZED: bool = True # сразу развернуть окно на весь экран
    WINDOW_PREVENT_CLOSE: bool = False # False - окно можно закрыть обычным способом
    THEME_MODE: str = "dark" # тёмная тема приложения
    FONT_FAMILY: str = "Segoe UI" # основной шрифт
    BODY_TEXT_SIZE: int = 14 # размер обычного текста
    TITLE_TEXT_SIZE: int = 24 # размер текста заголовков

    MIN_BET: int = 1 # минимальная разрешённая ставка
    DEFAULT_BET: int = 100 # ставка, которая сразу показана в поле ввода

    SOUND_SPIN_TRACK: str = "sounds/roulette_spin.mp3" # можно на чё угодно поменять, ток название надо такое
    SOUND_VOLUME: int = 1000 # громкость звука для Windows MCI значение 1000 максимум
    
    # минимальное и максимальное число рулетки
    ROULETTE_MIN_NUMBER: int = 0
    ROULETTE_MAX_NUMBER: int = 36
    ROULETTE_RED_NUMBERS: frozenset[int] = frozenset({
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
    })
    ROULETTE_WHEEL_ORDER: tuple[int, ...] = (
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
    ROULETTE_NUMBER_PAYOUT_MULTIPLIER: int = 35 # ставка на конкретное число умножается на 35
    ROULETTE_OUTSIDE_BET_PAYOUT_MULTIPLIER: int = 1 # ставка на цвет или чётность умножается на 1
    ROULETTE_SPIN_DURATION_SECONDS: int = 5 # рулетка крутится 5 секунд ЗА КАКОЕ ВРЕМЯ шарик должен добраться до результата
    ROULETTE_SPIN_EXTRA_TURNS: int = 5 # перед остановкой шарик делает 5 дополнительных кругов СКОЛЬКО ПОЛНЫХ КРУГОВ он сделает по дороге
    ROULETTE_EASING_POWER: int = 3 # отвечает за плавное замедление шарика
    ROULETTE_SPIN_FPS: int = 60 # обновлений анимации в секунду
    ROULETTE_MIN_ANIMATION_STEPS: int = 24 # минимальное количество шагов анимации
    SLOT_SYMBOLS: tuple = tuple(SlotSymbol) # все символы слотов из Enum, tuple чтобы набор случайно не менять 
    SLOT_REEL_COUNT: int = 3 # количество барабанов в слотах
    SLOT_PAYTABLE: ConfigMap = field(
        default_factory=create_slot_paytable
    ) # таблица выплат
    SLOTS_SPIN_DURATION_SECONDS: int = 4 # длительность крутки
    SLOT_SPIN_STEPS_PER_SECOND: int = 22 # количество смен символов за секунду
    SLOT_SPIN_PHASE_MODULO: int = 2 # каждые два шага повторяется цикл анимации
    # чётный шаг - барабан увеличен и наклонён вправо
    # нечётный шаг - обычный размер и наклон влево
    SLOT_REEL_SCALE_ACTIVE: float = 1.04 # размер барабана на активном шаге
    SLOT_REEL_SCALE_IDLE: float = 1.0 # размер барабана на обычном шаге 
    SLOT_REEL_ROTATION_ACTIVE: float = 0.015 # наклон барабана вправо на активном шаге
    SLOT_REEL_ROTATION_IDLE: float = -0.015 # наклон барабана влево на обычном шаге

Config = ConfigData() # готовый объект настроек для всего проекта
