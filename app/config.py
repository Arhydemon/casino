from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # типа корень проекта
DATA_DIR = BASE_DIR / 'data' # тут будет бд лежать
DATABASE_PATH = DATA_DIR / 'casino.db' # путь к базе данных