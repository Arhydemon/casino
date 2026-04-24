class Settings:
    def __init__(self, sound_enabled: int) -> None:
        self.sound_enabled = sound_enabled

    def is_sound_enabled(self) -> bool:
        return self.sound_enabled == 1
    
    def enable_sound(self) -> bool:
        self.enable_sound = 1

    def disable_sound(self) -> bool:
        self.enable_sound = 0