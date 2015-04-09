__author__ = 'Uni'

import soundController
import tubeController

song = 'soundFiles/Knight-Rider-Theme-Song.mp3'
# song = 'soundFiles/Windows Error.wav'

sound = soundController.SoundController()
sound.load(song)

tube = tubeController.TubeController()
tube.start()

sound.play()