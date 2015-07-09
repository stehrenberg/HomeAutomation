__author__ = 'luis'

from lib.periphery.dmx import DMXHandler, PixelTubeDevice, ColorFactory
from lib.periphery.sound import SoundController
from lib.logger.Logger import Logger


class Periphery:
    """Periphery controls the sound and the light controller."""

    STATUS_LED = 15

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

    def light_on(self, pixel, color_str):
        """Turn on the light on the given index.
        The color string has to be a hexadecimal representation of a rgb color.
        """

        pixel -= 1
        self.logger.log(Logger.INFO, "light " + str(pixel) + " turned on")

        color = ColorFactory.create_from_hex(color_str)

        self.light.set_pixel_color(pixel=pixel*3+1, color=color)
        self.light.set_pixel_color(pixel=pixel*3+2, color=color)

    # Turn off light number index
    def light_off(self, pixel):
        """Turns off the light on the given index."""

        pixel -= 1
        self.logger.log(Logger.INFO, "light " + str(pixel) + " turned off")

        self.light.set_pixel_color(pixel=pixel*3+1)
        self.light.set_pixel_color(pixel=pixel*3+2)

    def set_status_light(self, color_str):
        """Set the status light to the given color string.
        The color string has to be a hexadecimal representation of a rgb color.
        """

        color = ColorFactory.create_from_hex(color_str)
        self.light.set_pixel_color(self.STATUS_LED, color=color)

    def play_sound(self, file_path):
        """Play the sound on the given path."""

        self.logger.log(Logger.INFO, "sound at " + file_path + " played")

        self.sound.play(song_title='resources/sounds/' + file_path)
