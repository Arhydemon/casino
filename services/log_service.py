from datetime import datetime
from settings import Config as cfg


class LogService: # ну чё, это просто СЕРВИС ДЛЯ ЗАПИСИ СЕАНСА В log.txt
    # запоминает время запуска приложения и при закрытии записывает время выхода
    def __init__(self, login: str, log_path: str = cfg.LOG_PATH) -> None:
        self.login = login
        self.log_path = log_path
        self.time_in = datetime.now()

    def save_session(self) -> None:
        time_out = datetime.now()
        row = (
            f"|{self.login:<12}| "
            f"{self.time_in.strftime(cfg.LOG_DATETIME_FORMAT)} | "
            f"{time_out.strftime(cfg.LOG_DATETIME_FORMAT)} |"
        )
        with open(self.log_path, "a", encoding=cfg.TEXT_ENCODING) as file:
            file.write("+------------+---------------------+---------------------+\n")
            file.write("| login      | time_in             | time_out            |\n")
            file.write("|------------|---------------------|---------------------|\n")
            file.write(f"{row}\n")
            file.write("+------------+---------------------+---------------------+\n")
