__author__ = 'luis'


import TubeController
import SoundController
import ColorFactory


class Periphery:

    def __init__(self):
        self.light = TubeController.TubeController()
        self.sound = SoundController.SoundController()

    # Turn on light number index
    def light_on(self, index, color_str):
        print("light " + index + " turned on")
        # TODO: turn corresponding light on

        color = ColorFactory.create_from_hex(color_str)

        self.light.user_add(nr=index, color=color)

    # Turn off light number index
    def light_off(self, index):
        print("light " + index + " turned off")
        # TODO: turn corresponding light off

        self.light.user_rem(nr=index)

    # Play sound at given directory
    def play_sound(self, directory):
        print("sound at " + directory + " played")
        # TODO: play corresponding sound

        self.sound.load(song_title=directory)
        self.sound.play()