__author__ = 'Luis'

import dmxConnection
from time import sleep
import ColorFactory


#############################
#   Device configurations   #
#############################

DEV_TTY_USB_D = '/dev/ttyUSB%d'

# It's the number of USB ports on the Raspberry Pi 2 Model B
NR_USB_PORTS = 4

# Number of pixel that the pixel tube has
# The pixel goes from 0 to 15
NR_PIXELS = 16

# Number of channels for each pixel
NR_CHANNELS = 3

RED_CHANNEL = 1
GREEN_CHANNEL = 2
BLUE_CHANNEL = 3


class TubeController(object):
    """The tube controller manage all interactions with the PixelTube."""

    def __init__(self, dmx_address=0):
        """Initialize the Tube controller."""

        self.connected = 0
        self.running = 0

        # Search the right USB port
        for i in range(NR_USB_PORTS):
            try:
                device = DEV_TTY_USB_D % i
                self.tube = dmxConnection.DMXConnection(device=device, dmx_address=dmx_address)

                self.connected = 1
                break

            except dmxConnection.PortNotOpenException:
                pass

        if not self.is_connected():
            raise dmxConnection.NoConnectionException('The device is not plugged in.')

    def __del__(self):
        self.clear()

    def run(self):
        """The thread shows the KnightRider ..."""

        self.running = 1

        try:
            while self.running:
                self.knight_rider()
            self.stop()

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stops the controller and reset the PixelTube"""

        self.running = 0
        self.clear()

    def clear(self):
        """Darken the PixelTube."""

        self.tube.clear()
        self.render()

    def render(self):
        """Render the actual view."""

        self.tube.render()

    def is_connected(self):
        """Check the status if the device is connected."""

        return self.connected

    def set_pixel_color(self, pixel, color=ColorFactory.WHITE, auto_render=False):
        """Set the color with red, green and blue values for a specific pixel.
            You can select if the status change should be rendered immediately."""

        self.tube.set_channel((NR_CHANNELS * pixel) + RED_CHANNEL,   color.get_red(),   auto_render)
        self.tube.set_channel((NR_CHANNELS * pixel) + GREEN_CHANNEL, color.get_green(), auto_render)
        self.tube.set_channel((NR_CHANNELS * pixel) + BLUE_CHANNEL,  color.get_blue(),  auto_render)

    def move_pixel_left(self, pixel, color, old_color=ColorFactory.BLACK):
        """Moves the specified pixel to the left hand-side with the selected color.
            You can select the color of the old pixel position as well."""

        if pixel < NR_PIXELS - 1:
            self.set_pixel_color((pixel + 1) % NR_PIXELS, color)
        self.set_pixel_color(pixel, old_color)

        self.render()

    def move_pixel_right(self, pixel, color, old_color=ColorFactory.BLACK):
        """Moves the specified pixel to the right hand-side with the selected color.
            You can select the color of the old pixel position as well."""

        if pixel > 0:
            self.set_pixel_color((pixel - 1) % NR_PIXELS, color)
        self.set_pixel_color(pixel, old_color)

        self.render()

    def user_add(self, nr, color):
        """For every user a new light is added in the selected color."""

        self.set_pixel_color(nr, color)
        self.render()

    def user_rem(self, nr):

        self.set_pixel_color(nr, ColorFactory.BLACK)
        self.render()

    def test(self):
        while True:
            for i in range(16):
                for j in range(0, 256/4, 16):
                    self.user_add(i, ColorFactory.RGBColor(red=j, green=j, blue=j))
                self.render()
                sleep(1)
            self.clear()

    def knight_rider(self):
        """A red pixel goes back and forth as the car in KnightRider did."""

        delay = .1

        for i in range(0, NR_PIXELS):
            self.move_pixel_left(i, ColorFactory.RED)
            sleep(delay)

        for i in range(NR_PIXELS - 1, 0, -1):
            self.move_pixel_right(i, ColorFactory.RED)
            sleep(delay)

    def theme1(self, color=ColorFactory.GREY):
        """Wandering Pixel Queue"""

        delay = .02

        # Add pixels from the left hand-side and push them to the right hand-side
        for i in range(NR_PIXELS):
            for j in range(NR_PIXELS - i):

                # If it's the first pixel you set it
                if j == 0:
                    self.set_pixel_color(j, color, auto_render=True)
                else:

                    # Then you move it right, till you cant push it further
                    self.move_pixel_left(j, color)
                sleep(delay)

        # Remove pixels from the left hand-side and push them to the right hand-side
        for i in range(NR_PIXELS):
            for j in range(i, NR_PIXELS):

                # If it is the most left pixel
                if j == i:
                    self.set_pixel_color(j - 1, ColorFactory.BLACK, auto_render=True)
                else:

                    # Its pushed till the end
                    self.move_pixel_left(j, ColorFactory.BLACK, color)

                sleep(delay)

    def theme2(self, color=ColorFactory.GREY):
        """Create a """

        delay = .1

        for i in range(NR_PIXELS / 2):
                self.move_pixel_left(i+1, color, ColorFactory.create_inverse(color))
                sleep(delay)

    def theme3(self, color=ColorFactory.BLACK):
        """Create from the center on a flood to the ends."""

        delay = .1

        for j in range(NR_PIXELS/2, 0, -1):
            old_color = color
            color = ColorFactory.brighter_color(color)
            if j == NR_PIXELS/2:
                self.set_pixel_color(j - 1,         color)
                self.set_pixel_color(NR_PIXELS - j, color)
                self.render()
            else:
                self.move_pixel_right(j - 1,        color, old_color)
                self.move_pixel_left(NR_PIXELS - j, color, old_color)

            sleep(delay)


if __name__ == '__main__':
    tube = TubeController()
    # tube.test()
