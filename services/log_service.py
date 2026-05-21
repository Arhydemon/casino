from datetime import datetime
from config import LOG_PATH

class LogService:
    def __init__(self, login: str, log_path: str = LOG_PATH) -> None:
        self.login = login
        self.log_path = log_path
        self.time_in = datetime.now()

    def save_session(self) -> None:
        time_out = datetime.now()
        with open(self.log_path, "a", encoding="utf-8") as file:
            file.write(
                f"{self.login} | "
                f"{self._format_time(self.time_in)} | "
                f"{self._format_time(time_out)}\n"
            )

    @staticmethod
    def _format_time(value: datetime) -> str:
        return value.strftime("%d.%m.%y %H:%M:%S")
