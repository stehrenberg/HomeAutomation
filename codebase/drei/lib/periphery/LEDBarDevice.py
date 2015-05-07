__author__ = 'Luis'


from DMXDevice import DMXDevice


class LEDBarDevice(DMXDevice):
    """Class handles the PixelTube device."""

    NR_PIXELS = 8

    def __init__(self, dmx_address):
        DMXDevice.__init__(self, dmx_address=dmx_address, nr_pixels=LEDBarDevice.NR_PIXELS)
