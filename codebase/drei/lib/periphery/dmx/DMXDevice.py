__author__ = 'Luis'


class DMXDevice(object):
    """Defines an interface to a specific DMX device."""

    # Define the standard channels
    RED_CHANNEL = 1
    GREEN_CHANNEL = 2
    BLUE_CHANNEL = 3

    NR_CHANNELS = 3

    def __init__(self, dmx_address, nr_pixels):
        """Create a new DMX device with the given number of pixel on the DMX address."""

        self.dmx_address = dmx_address
        self.nr_pixels = nr_pixels

    def get_nr_pixels(self):
        """Return the number of pixels the device has."""

        return self.nr_pixels

    def get_dmx_address(self):
        """Return the DMX address."""

        return self.dmx_address
