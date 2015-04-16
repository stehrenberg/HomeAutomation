__author__ = 'Uni'

import SoundController
import TubeController
from time import sleep

song = 'soundFiles/Knight-Rider-Theme-Song.mp3'
# song = 'soundFiles/Windows Error.wav'

try:
    sound = SoundController.SoundController()
    sound.load(song)

    tube = TubeController.TubeController()
    tube.start()

    sound.play()
    sleep(60)

except KeyboardInterrupt:
    print "main: KeyboardInterrupt"
    sound.stop()
    tube.clear()