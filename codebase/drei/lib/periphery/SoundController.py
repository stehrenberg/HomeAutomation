__author__ = 'Luis'
import platform

if platform.machine() == "armv7l":
    import pygame

from threading import Thread


# TODO Test!!!
# real impelementation on respberrypi
if platform.machine() == "armv7l":
    class SoundController(Thread):
        """The sound controller handle the"""

        def __init__(self):
            Thread.__init__(self)
            self.running = 0
            pygame.init()

        def load(self, song_title):
            """Load a new song.
                If a new song is loaded, the actual is stopped."""

            self.running = 0
            pygame.mixer.music.load(song_title)

        def play(self):
            """Play the song, as long as its not stopped."""

            self.start()

        def run(self):
            self.running = 1

            clock = pygame.time.Clock()

            pygame.mixer.music.play()

            while self.running:
                clock.tick(60)

        def pause(self):
            """Pause the actual song."""

            self.running = 0

        def stop(self):
            """Stop the song and close the instance."""

            self.pause()
            pygame.quit()
            self.join(2)
else:
        class SoundController(Thread):


            def load(self, song_title):
                print "SoundController: Loading file " + song_title

            def play(self):
                print "SoundController: Playing"

            def pause(self):
                print("SoundController: Pausing")

            def stop(self):
                print("SoundController: Stopping")


if __name__ == '__main__':
    from time import sleep

    SONG = 'soundFiles/Knight-Rider-Theme-Song.mp3'

    sound = SoundController()
    sound.load(SONG)
    sound.play()

    print "Song started"

    sleep(30)
    sound.stop()

    print "Song stopped"
