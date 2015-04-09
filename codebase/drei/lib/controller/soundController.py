__author__ = 'Luis'

import pygame

class SoundController(object):

    def __init__(self):
        #TODO Put it in a thread
        pygame.init()

    def load(self, songTitle):
        self.song = pygame.mixer.music.load(songTitle)

    def play(self):
        clock = pygame.time.Clock()

        pygame.mixer.music.play()

        while True:
            clock.tick(60)

    def stop(self):
        pygame.quit()