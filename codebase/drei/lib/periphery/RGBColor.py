__author__ = 'Luis'

from dmxConnection import MIN_VAL
from dmxConnection import MAX_VAL


class RGBColor(object):
    """Defines a RGB color."""

    MIN_DIM = MIN_VAL
    MAX_DIM = MAX_VAL

    def __init__(self, red=MIN_DIM, green=MIN_DIM, blue=MIN_DIM):
        """Initialize the color. You can set a value for every channel (i.e. red, green and blue).
            The default color is black."""

        if red > RGBColor.MAX_DIM:
            self._red = RGBColor.MAX_DIM
        else:
            self._red = red
        if green > RGBColor.MAX_DIM:
            self._green = RGBColor.MAX_DIM
        else:
            self._green = green
        if blue > RGBColor.MAX_DIM:
            self._blue = RGBColor.MAX_DIM
        else:
            self._blue = blue

    def __eq__(self, other):
        """Check if it's the same color."""

        if isinstance(other, RGBColor):
            if self.get_red() is not other.get_red():
                return False
            elif self.get_green() is not other.get_green():
                return False
            elif self.get_blue() is not other.get_blue():
                return False
            else:
                return True
        else:
            return False

    def __cmp__(self, other):
        """Compare two colors by there RGB values."""

        if isinstance(other, RGBColor):
            val = (self.get_red() - other.get_red())
            val *= 256 + (self.get_green() - other.get_green())
            val *= 256 + (self.get_blue() - other.get_blue())

            return val
        else:
            return -1

    def __str__(self):
        """Return the hex form of the color."""

        val = self.get_red()
        val *= 256 + self.get_green()
        val *= 256 + self.get_blue()

        return ''.join(['#', hex(val)[2:]])

    def get_red(self):
        """Return the value of the red channel."""

        return self._red

    def get_green(self):
        """Return the value of the green channel."""

        return self._green

    def get_blue(self):
        """Return the value of the blue channel."""

        return self._blue
