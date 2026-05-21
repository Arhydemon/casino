from __future__ import annotations
import ctypes
from pathlib import Path
import threading
import uuid
from config import ASSETS_DIR, SOUND_CLICK, SOUND_LOSE, SOUND_ROULETTE_SPIN, SOUND_SLOTS_SPIN, SOUND_WIN
from models.settings import Settings

try:
    # тут читает длительность аудиофайла чтобы можно было синкать анимации
    from mutagen import File as MutagenFile
except Exception:
    # здесь нужна чтобы проект не падал если пакет не установлен
    MutagenFile = None

try:
    # сам дает быстрый способ проигрывать короткие звуки
    from playsound3 import playsound
except Exception:
    playsound = None


class SoundService:
    # тут управляет всеми звуками проекта и их состоянием
    def __init__(self, page, settings: Settings) -> None:
        # здесь держим настройки чтобы уважать переключатель звука
        self.settings = settings
        self._mci_lock = threading.Lock()
        self.aliases: dict[str, str] = {}
        # тут собираем пути к каждому звуку
        self.paths = {
            "click": self._sound_path(SOUND_CLICK),
            "roulette": self._sound_path(SOUND_ROULETTE_SPIN),
            "slots": self._sound_path(SOUND_SLOTS_SPIN),
            "win": self._sound_path(SOUND_WIN),
            "lose": self._sound_path(SOUND_LOSE),
        }
        self._open_all()

    def play_click(self, force: bool = False) -> None:
        self.play("click", force=force)

    def play_roulette(self, force: bool = False) -> None:
        self.play("roulette", force=force)

    def start_roulette_spin(self) -> None:
        if not self.settings.is_sound_enabled():
            return

        alias = self._ensure_alias("roulette")
        if alias is None:
            return

        self._play_roulette_loop(alias)

    def stop_roulette_spin(self) -> None:
        alias = self.aliases.get("roulette")
        if alias is None:
            return
        self._mci(f"stop {alias}")

    def start_slots_spin(self) -> None:
        if not self.settings.is_sound_enabled():
            return
        alias = self._ensure_alias("slots")
        if alias is None:
            return
        self._play_slots_loop(alias)

    def stop_slots_spin(self) -> None:
        alias = self.aliases.get("slots")
        if alias is None:
            return
        self._mci(f"stop {alias}")

    def play_slots(self, force: bool = False) -> None:
        self.play("slots", force=force)

    def play_result(self, is_win: bool, force: bool = False) -> None:
        if is_win:
            self.play("win", force=force)
        else:
            self.play("lose", force=force)

    # сам возвращает длительность аудио чтобы можно было ровно синкаться по времени
    def get_duration_seconds(self, sound_name: str, fallback: float = 0.0) -> float:
        path = self.paths.get(sound_name)
        if path is not None and path.exists():
            duration_from_file = self._duration_from_file(path)
            if duration_from_file > 0:
                return duration_from_file
        alias = self.aliases.get(sound_name)
        if alias is None:
            return max(0.0, float(fallback))
        length_text = self._mci_query(f"status {alias} length")
        if not length_text:
            return max(0.0, float(fallback))
        try:
            length_ms = int(length_text.strip())
        except ValueError:
            return max(0.0, float(fallback))
        if length_ms <= 0:
            return max(0.0, float(fallback))
        return length_ms / 1000.0

    # здесь универсально запускает одиночный звук по имени
    def play(self, sound_name: str, force: bool = False) -> None:
        if not force and not self.settings.is_sound_enabled():
            return
        path = self.paths.get(sound_name)
        if path is None or not path.exists():
            return
        thread = threading.Thread(target=self._play, args=(sound_name, path), daemon=True)
        thread.start()

    def close(self) -> None:
        for alias in self.aliases.values():
            self._mci(f"close {alias}")
        self.aliases.clear()

    def _open_all(self) -> None:
        for name, path in self.paths.items():
            if not path.exists():
                continue
            self._ensure_alias(name)

    def _sound_path(self, relative_path: str) -> Path:
        project_root = Path(__file__).resolve().parent.parent
        return (project_root / ASSETS_DIR / relative_path).resolve()

    def _play(self, sound_name: str, path: Path) -> None:
        alias = self.aliases.get(sound_name)
        if alias is not None:
            self._play_alias(alias)
            return
        played = self._play_with_playsound(path)
        if played:
            return

    def _play_with_playsound(self, path: Path) -> bool:
        if playsound is None:
            return False
        try:
            playsound(str(path), block=False, backend="wmplayer")
            return True
        except TypeError:
            try:
                playsound(str(path), block=False)
                return True
            except Exception:
                return False
        except Exception:
            try:
                playsound(str(path), block=False, backend="winmm")
                return True
            except Exception:
                return False
    def _play_alias(self, alias: str) -> None:
        self._mci(f"stop {alias}")
        self._mci(f"play {alias} from 0")

    # сам крутит звук рулетки по кругу
    def _play_roulette_loop(self, alias: str) -> None:
        self._mci(f"stop {alias}")
        self._mci(f"play {alias} from 0 repeat")

    # в этом месте крутит звук слотов по кругу
    def _play_slots_loop(self, alias: str) -> None:
        self._mci(f"stop {alias}")
        self._mci(f"play {alias} from 0 repeat")

    def _ensure_alias(self, sound_name: str) -> str | None:
        alias = self.aliases.get(sound_name)
        if alias is not None:
            return alias

        path = self.paths.get(sound_name)
        if path is None or not path.exists():
            return None
        alias = f"sound_{uuid.uuid4().hex}"
        safe_path = str(path.resolve())
        open_code = self._mci(f'open "{safe_path}" type mpegvideo alias {alias}')
        if open_code != 0:
            return None
        self._mci(f"set {alias} time format milliseconds")
        self._mci(f"setaudio {alias} volume to 1000")
        self.aliases[sound_name] = alias
        return alias

    def _mci(self, command: str) -> int:
        with self._mci_lock:
            return ctypes.windll.winmm.mciSendStringW(command, None, 0, None)

    def _mci_query(self, command: str) -> str:
        buffer = ctypes.create_unicode_buffer(128)
        with self._mci_lock:
            code = ctypes.windll.winmm.mciSendStringW(command, buffer, len(buffer), None)
        if code != 0:
            return ""
        return buffer.value

    @staticmethod
    def _duration_from_file(path: Path) -> float:
        if MutagenFile is None:
            return 0.0
        try:
            audio_file = MutagenFile(str(path))
        except Exception:
            return 0.0
        if audio_file is None:
            return 0.0
        info = getattr(audio_file, "info", None)
        length = getattr(info, "length", 0.0)
        try:
            value = float(length)
        except (TypeError, ValueError):
            return 0.0
        if value <= 0:
            return 0.0
        return value
