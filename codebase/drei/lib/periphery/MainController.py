__author__ = 'Luis'


import SoundController
import TubeController
from time import sleep


SONG = 'soundFiles/Knight-Rider-Theme-Song.mp3'

sound = SoundController.SoundController()
tube = TubeController.TubeController()

try:
    sound.load(SONG)
    sound.play()

    # TODO Don't call the run() method directly!!
    tube.run()

    sleep(20)
    sound.stop()
    tube.stop()

except KeyboardInterrupt:
    sound.stop()
    tube.stop()
