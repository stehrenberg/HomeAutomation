__author__ = 'Luis'

from lib.periphery.dmx import DMXConnection, ColorFactory
from lib.periphery.dmx.PixelTubeDevice import PixelTubeDevice
from lib.periphery.dmx.LEDBarDevice import LEDBarDevice
from lib.periphery.dmx.DMXDevice import DMXDevice
from lib.logger.Logger import Logger


class DMXHandler:
    """Class handles a number of DMX devices."""

    DEVICE_ADDRESS = '/dev/ttyUSB%d'
    NR_USB_PORTS = 4

    def __init__(self):
        """Create an empty handler and connect to the DMX interface."""

        self.logger = Logger()

        self.dmx_devices = list()
        self.nr_pixels = 0

        self.connection = DMXConnection.search_port(DMXHandler.DEVICE_ADDRESS, DMXHandler.NR_USB_PORTS)

    def is_connected(self):
        """Checks the connection with the DMX interface."""

        return self.connection is not None

    def get_available_pixels(self):
        """Return the number of pixels."""

        return self.nr_pixels

    def is_valid(self, check_device):
        """Test if the device is valid for this DMXHandler, i.e. it doesn't use the same port as another device"""

        start_address = check_device.get_dmx_address()
        end_address = start_address + check_device.get_nr_pixels() - 1

        for device in self.dmx_devices:
            start = device.get_dmx_address()
            end = start + device.get_nr_pixels()

            if start_address in range(start, end) or end_address in range(start, end):
                return False

        return True

    def get_channel(self, pixel):
        """Return the channel of that pixel.
        Return None if the channel does not exist.
        """

        # TODO Works just with a sorted list of devices ascending by there dmx_address
        for device in self.dmx_devices:
            if pixel > device.get_nr_pixels():
                pixel -= device.get_nr_pixels()
            else:
                return device.get_dmx_address() + pixel*DMXDevice.NR_CHANNELS

        return None

    def add_device(self, device):
        """Add the device to the handler.
        Checks if there is no conflict with other devices.
        """

        if isinstance(device, DMXDevice):
            if self.is_valid(device):
                self.nr_pixels += device.get_nr_pixels()
                self.dmx_devices.append(device)

    def remove_device(self, device):
        """Remove the device from the handler."""

        if isinstance(device, DMXDevice):
            if device in self.dmx_devices:
                self.nr_pixels -= device.get_nr_pixels()
                self.dmx_devices.remove(device)

    def set_pixel_color(self, pixel, color=ColorFactory.BLACK):
        """Set the pixel to the given color."""

        if not self.is_connected():
            raise DMXConnection.NoConnectionException

        channel = self.get_channel(pixel)

        if channel is None:
            self.logger.log(Logger.WARNING, "Invalid channel %d" % channel)
        else:
            self.connection.set_channel(channel + DMXDevice.RED_CHANNEL,   color.get_red())
            self.connection.set_channel(channel + DMXDevice.GREEN_CHANNEL, color.get_green())
            self.connection.set_channel(channel + DMXDevice.BLUE_CHANNEL,  color.get_blue(), True)

    def set_overall_color(self, color):
        """Set the color of every device."""

        for pixel in range(self.get_available_pixels()):
            self.set_pixel_color(pixel, color)

    def test(self):
        """Test if all connected devices works correctly by setting the main colors."""

        from time import sleep

        color_list = [ColorFactory.RED,
                      ColorFactory.GREEN,
                      ColorFactory.BLUE]

        for color in color_list:
            for i in range(self.get_available_pixels()):
                self.set_pixel_color(i, color)
                sleep(0.06)
                self.set_pixel_color(i)

    def clear(self):
        """Reset the color on all devices."""

        self.set_overall_color(ColorFactory.BLACK)


if __name__ == '__main__':
    handler = DMXHandler()
    tube = PixelTubeDevice(0)

    bar = LEDBarDevice(48)

    if handler.is_connected():
        logger = Logger()
        logger.log(Logger.INFO, "Is connected")

        handler.add_device(tube)
        handler.add_device(bar)

        from time import sleep

        colours = [ColorFactory.RED,
                   ColorFactory.GREEN,
                   ColorFactory.BLUE,
                   ColorFactory.YELLOW,
                   ColorFactory.MAGENTA,
                   ColorFactory.CYAN,
                   ColorFactory.ORANGE,
                   ColorFactory.PURPLE,
                   ColorFactory.LIME,
                   ColorFactory.ROYAL,
                   ColorFactory.PINK,
                   ColorFactory.AZURE]

        while True:
            try:
                for colour in colours:
                    for k in range(handler.get_available_pixels()):
                        handler.set_pixel_color(k, colour)
                        sleep(.1)
                    handler.clear()
            except KeyboardInterrupt:
                handler.clear()
