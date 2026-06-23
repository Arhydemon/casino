# ДАННЫЙ ФАЙЛ ЗАПУСКАЕТ ЗВУК НЕ ЧЕРЕЗ ФЛЕТ А НАПРЯМУЮ ЧЕРЕЗ ВИНДУ
import ctypes # ctypes позволяет Python вызывать системные функции Windows
from pathlib import Path
from models.settings import Settings
from settings import Config as cfg


class SoundService: # СЕРВИС ДЛЯ УПРАВЛЕНИЯ ЗВУКОМ! открывает mp3 и запускает его по кругу и останавливает
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.alias = "spin_sound" # alias это короткое внутреннее имя аудиофайла
        # винда дальше работает со звуком через это имя чтобы каждый раз не передавать полный путь
        self.path = self._sound_path(cfg.SOUND_SPIN_TRACK)
        self.is_open = False
        self._open()

    def start_spin(self) -> None:
        self._play_loop()

    def stop_spin(self) -> None:
        self._stop()

    def close(self) -> None:
        if self.is_open:
            self._mci(f"stop {self.alias}")
            self._mci(f"close {self.alias}")
            self.is_open = False

    def _open(self) -> None:
        if not self.path.exists():
            return
        code = self._mci(f'open "{self.path}" type mpegvideo alias {self.alias}')
        # отправляем команду открыть mp3
        # type mpegvideo тип проигрывателя Windows
        # код 0 означает, что команда выполнилась успешно
        if code == 0:
            self._mci(f"setaudio {self.alias} volume to {cfg.SOUND_VOLUME}")
            self.is_open = True

    def _play_loop(self) -> None:
        if not self.settings.sound_enabled or not self.is_open:
            return
        self._mci(f"stop {self.alias}")
        self._mci(f"play {self.alias} from 0 repeat")

    def _stop(self) -> None:
        if self.is_open:
            self._mci(f"stop {self.alias}")

    def _sound_path(self, relative_path: str) -> Path:
        project_root = Path(__file__).resolve().parent.parent
        return (project_root / cfg.ASSETS_DIR / relative_path).resolve()

    def _mci(self, command: str) -> int: 
        return ctypes.windll.winmm.mciSendStringW(command, None, 0, None)
        # ctypes.windll это доступ к библиотекам Windows
        # winmm  системная библиотека для мультимедиа
