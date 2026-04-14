import pygame
import os

class MusicPlayer:
    def __init__(self):
        self.base = os.path.dirname(__file__)

        self.playlist = [
            os.path.join(self.base, "music", "ILLIT  - Billyeoon Goyangi (Do the Dance).mp3"),
            os.path.join(self.base, "music", "1|1_Do_It_Like_That_TOMORROW_X_TOGETHER_Jonas_Brothers_320.mp3"),
            os.path.join(self.base, "music", "Lucky Girl Syndrome.mp3")
        ]

        self.current = 0

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return self.playlist[self.current]