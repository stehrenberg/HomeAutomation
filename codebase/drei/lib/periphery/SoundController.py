__author__ = 'Luis'

import platform
import Const


# real implementation on raspberry pi
if platform.machine() == Const.PI_PLATFORM:
    import pygame
    from thread import start_new_thread

    def play(song_title):
        start_new_thread(init_and_play, (song_title,))

    def init_and_play(song_title):
        pygame.mixer.init()
        pygame.mixer.music.load(song_title)
        pygame.mixer.music.play()

else:
    def play(song_title):
        print "SoundController: Loading file " + song_title
