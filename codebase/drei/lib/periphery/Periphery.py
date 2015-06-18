__author__ = 'luis'


import DMXHandler
import PixelTubeDevice
import SoundController
import ColorFactory
from lib.logger.Logger import Logger


class Periphery:

    STATUS_LED = 16

    def __init__(self):
        self.logger = Logger()

        self.sound = SoundController.SoundController()

        self.light = DMXHandler.DMXHandler()

        tube = PixelTubeDevice.PixelTubeDevice(0)
        # bar = LEDBarDevice.LEDBarDevice(48)

        if self.light.is_connected():
            self.logger.log(Logger.INFO, "LightController is connected")
            print("Periphery: LightController is connected")

            self.light.add_device(tube)
            # self.light.add_device(bar)

            self.light.test()
        else:
            self.logger.log(Logger.INFO, "LightController is not connected")
            print("Periphery: LightController is not connected")

    def __del__(self):
        self.light.clear()

    # Turn on light number index
    def light_on(self, pixel, color_str):
        pixel -= 1
        self.logger.log(Logger.INFO, "light " + str(pixel) + " turned on")

        color = ColorFactory.create_from_hex(color_str)

        self.light.set_pixel_color(pixel=pixel*4+1, color=color)
        self.light.set_pixel_color(pixel=pixel*4+2, color=color)
        self.light.set_pixel_color(pixel=pixel*4+3, color=color)

    # Turn off light number index
    def light_off(self, pixel):
        pixel -= 1
        self.logger.log(Logger.INFO, "light " + str(pixel) + " turned off")

        self.light.set_pixel_color(pixel=pixel*4+1)
        self.light.set_pixel_color(pixel=pixel*4+2)
        self.light.set_pixel_color(pixel=pixel*4+3)

    def set_status_light(self, color_str):
        color = ColorFactory.create_from_hex(color_str)
        self.light.set_pixel_color(self.STATUS_LED, color=color)

    # Play sound at given directory
    def play_sound(self, file):
        self.logger.log(Logger.INFO, "sound at " + file + " played")

        self.sound.play(song_title='lib/periphery/soundFiles/' + file)
