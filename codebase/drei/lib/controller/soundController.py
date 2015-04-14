__author__ = 'Luis'

import pygame


class SoundController(object):
    def __init__(self):
        # TODO Put it in a thread
        pygame.init()

    def load(self, songTitle):
        self.song = pygame.mixer.music.load(songTitle)

    def play(self):

        try:
            clock = pygame.time.Clock()

            pygame.mixer.music.play()

            while True:
                clock.tick(60)

        except KeyboardInterrupt:
            print "sound: KeyboardInterrupt"
            self.stop()


def stop(self):
    pygame.quit()