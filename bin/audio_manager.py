from pgzero import music
class AudioManager:
    _instance = None
    
    def __init__(self):
            AudioManager._instance = self
            self.music_active = True
            self.sounds = None
    
    @staticmethod
    def get_instance():
        if AudioManager._instance is None:
            AudioManager()
        return AudioManager._instance
    
    def initialize(self, sounds_module):
        self.sounds = sounds_module
    
    def play_sfx(self, sfx_name):
        if self.music_active and self.sounds:
            try:
                sound = getattr(self.sounds, sfx_name, None)
                if sound:
                    sound.set_volume(0.5)
                    sound.play()
            except AttributeError:
                print(f"'{sfx_name}' não encontrado.")
    def play_music(self):
        music.play('soundtrack')
    def set_music_active(self, active):
        self.music_active = active