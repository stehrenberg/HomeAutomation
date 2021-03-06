__author__ = 'Luis'

import platform

import Const
from lib.logger.Logger import Logger


if platform.machine() == Const.PI_PLATFORM:
    import serial


###########################
# Protocol configurations #
###########################

START_VAL = 0x7E
END_VAL = 0xE7

MIN_VAL = 0
MAX_VAL = 255

MIN_CHANNELS = 1
MAX_CHANNELS = 512

COM_BAUD = 57600
COM_TIMEOUT = 1
COM_PORT = 7

LABELS = {'GET_WIDGET_PARAMETERS': 3,
          'SET_WIDGET_PARAMETERS': 4,
          'RX_DMX_PACKET': 5,
          'TX_DMX_PACKET': 6,
          'TX_RDM_PACKET_REQUEST': 7,
          'RX_DMX_ON_CHANGE': 8
          }


class DMXConnection(object):
    """DMXConnection represents the connection to a single DMX device.
        The DMX address can be set."""

    def __init__(self, device, dmx_address=0):

        self.logger = Logger()

        self.com = 0
        self.dmx_frame = list()
        self.dmx_address = dmx_address

        # setup channel output list
        for i in xrange(MAX_CHANNELS + 1):
            self.dmx_frame.append(MIN_VAL)

        if platform.machine() == Const.PI_PLATFORM:
            try:
                self.com = serial.Serial(device, baudrate=COM_BAUD, timeout=COM_TIMEOUT)
            except:
                self.logger.log(Logger.ERROR, "Could not open %s" % device)

            self.logger.log(Logger.INFO, "Opened %s" % self.com.portstr)

    def set_channel(self, channel, val, auto_render=False):
        """Set the channel to a specified value.
            You can select if the channel should be rendered directly.
            The default is False.
        """

        #  takes channel and value arguments to set a channel level in the local
        #  dmx frame, to be rendered the next time the render() method is called
        if (channel > MAX_CHANNELS) or (channel < MIN_CHANNELS):
            self.logger.log(Logger.WARNING, "Invalid channel %d" % channel)

        if val > MAX_VAL:
            val = MAX_VAL

        if val < MIN_VAL:
            val = MIN_VAL

        self.dmx_frame[self.dmx_address + channel] = val

        if auto_render:
            self.render()

    def clear(self, channel=0):
        """Clear all channels.
            Set channel to clear only the specified channel."""

        if channel == 0:
            for i in xrange(MIN_CHANNELS, MAX_CHANNELS):
                self.dmx_frame[i] = MIN_VAL
        else:
            self.dmx_frame[channel] = MIN_VAL

        self.render()

    def render(self):
        """Set all the pixel that were set before."""

        #  updates the dmx output from the USB DMX Pro with the values from self.dmx_frame
        packet = list()
        packet.append(chr(START_VAL))
        packet.append(chr(LABELS['TX_DMX_PACKET']))
        packet.append(chr(len(self.dmx_frame) & 0xFF))
        packet.append(chr((len(self.dmx_frame) >> 8) & 0xFF))

        for j in xrange(len(self.dmx_frame)):
            packet.append(chr(self.dmx_frame[j]))

        packet.append(chr(END_VAL))

        if platform.machine() == Const.PI_PLATFORM:
            self.com.write(''.join(packet))

    def close(self):
        """Close the port."""

        if platform.machine() == Const.PI_PLATFORM:
            self.com.close()


def search_port(device_string, nr_of_ports):
    """Search the port where the DMX interface is plugged in."""

    connection = None

    for i in range(nr_of_ports):
        try:
            port = device_string % i
            connection = DMXConnection(port)
            break

        except PortNotOpenException:
            pass

    return connection


class PortNotOpenException(Exception):
    """Exception is raised when the port couldn't be open."""

    def __init__(self, arg):
        self.arg = arg


class InvalidChannelException(Exception):
    """Exception is raised when you try to assign a channel outside of the range."""

    def __init__(self, arg):
        self.arg = arg


class NoConnectionException(Exception):
    """The Exception is raised when the device is not plugged in."""

    def __init__(self, arg):
        self.arg = arg
