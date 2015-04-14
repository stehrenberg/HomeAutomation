__author__ = 'Uni'

import soundController
import tubeController
from time import sleep

song = 'soundFiles/Knight-Rider-Theme-Song.mp3'
# song = 'soundFiles/Windows Error.wav'

try:
    sound = soundController.SoundController()
    sound.load(song)

    tube = tubeController.TubeController()
    tube.start()

    sound.play()
    sleep(60)

except KeyboardInterrupt:
    print "main: KeyboardInterrupt"
    sound.stop()
    tube.clear()