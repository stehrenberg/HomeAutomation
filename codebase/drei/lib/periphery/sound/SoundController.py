__author__ = 'Luis'

import platform

import Const
from lib.logger.Logger import Logger


# real implementation on raspberry pi
if platform.machine() == Const.PI_PLATFORM:
    class SoundController:
        """Controls the sound."""

        def __init__(self):
            self.logger = Logger()
            self.logger.log(Logger.INFO, "Started")
            print("Soundcontroller started")

        def play(self, song_title):
            """Play the song on the path."""

            from thread import start_new_thread
            self.logger.log(Logger.INFO, "Playing file " + song_title)
            start_new_thread(self.init_and_play, (song_title,))

        def init_and_play(self, song_title):
            """Initialize the sound controller and plays the sound."""

            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(song_title)
            pygame.mixer.music.play()

else:
    class SoundController:
        """Mock-Up Class for controlling the sound."""

        def __init__(self):
            self.logger = Logger()
            self.logger.log(Logger.INFO, "Started")

        def play(self, song_title):
            """Play the song on the path."""

            self.logger.log(Logger.INFO, "Loading file " + song_title)
