__author__ = 'Luis'

from lib.periphery.dmx.DMXDevice import DMXDevice


class PixelTubeDevice(DMXDevice):
    """Class handles the PixelTube device."""

    NR_PIXELS = 16

    def __init__(self, dmx_address):
        DMXDevice.__init__(self, dmx_address=dmx_address, nr_pixels=PixelTubeDevice.NR_PIXELS)
