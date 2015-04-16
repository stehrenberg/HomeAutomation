__author__ = 'Luis'


import soundController
import tubeController
from time import sleep


SONG = 'soundFiles/Knight-Rider-Theme-Song.mp3'

try:
    sound = soundController.SoundController()
    sound.load(SONG)
    sound.play()

    tube = tubeController.TubeController()
    tube.start()

    sleep(20)
    sound.stop()
    tube.stop()

except KeyboardInterrupt:
    sound.stop()
    tube.stop()
