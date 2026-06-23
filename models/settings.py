from models.base_entity import BaseEntity


class Settings(BaseEntity): # КЛАСС С НАСТРОЙКАМИ ПРИЛОЖЕНИЯ!
    def __init__(self, sound_enabled: bool = False) -> None:
        self.sound_enabled = sound_enabled

    @property
    def sound_enabled(self) -> bool:
        return self._sound_enabled

    @sound_enabled.setter
    def sound_enabled(self, value: bool) -> None:
        self._sound_enabled = bool(value)

    def compare_value(self):
        return int(self.sound_enabled)

    def display_text(self) -> str:
        return f"звук: {self.sound_enabled}"
