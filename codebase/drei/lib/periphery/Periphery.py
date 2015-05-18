__author__ = 'luis'


import DMXHandler
import PixelTubeDevice
import SoundController
import ColorFactory


class Periphery:

    def __init__(self):
        self.sound = SoundController.SoundController()

        self.light = DMXHandler.DMXHandler()

        tube = PixelTubeDevice.PixelTubeDevice(0)
        # bar = LEDBarDevice.LEDBarDevice(48)

        if self.light.is_connected():
            print "Is connected"

            self.light.add_device(tube)
            # self.light.add_device(bar)

            self.light.test()

    # Turn on light number index
    def light_on(self, pixel, color_str):
        print("light " + str(pixel) + " turned on")

        color = ColorFactory.create_from_hex(color_str)

        self.light.set_pixel_color(pixel=pixel*4, color=color)
        self.light.set_pixel_color(pixel=pixel*4+1, color=color)
        self.light.set_pixel_color(pixel=pixel*4+2, color=color)

    # Turn off light number index
    def light_off(self, pixel):
        print("light " + str(pixel) + " turned off")

        self.light.set_pixel_color(pixel=pixel*4)
        self.light.set_pixel_color(pixel=pixel*4+1)
        self.light.set_pixel_color(pixel=pixel*4+2)

    # Play sound at given directory
    def play_sound(self, file):
        print("sound at " + file + " played")
        # TODO: play corresponding sound

        self.sound.load(song_title='lib/periphery/soundFiles/' + file)
        # TODO: FIX: self.sound.play()
