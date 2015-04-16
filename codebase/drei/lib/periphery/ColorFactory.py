__author__ = 'Luis'

from RGBColor import RGBColor


def create_rgb(r=RGBColor.MIN_DIM, g=RGBColor.MIN_DIM, b=RGBColor.MIN_DIM):
    """Create the color in the RGB color space, with a value for every channel."""

    return RGBColor(red=r, green=g, blue=b)


def create_brightness(dim):
    """Create the color with the given brightness."""

    return RGBColor(red=dim, green=dim, blue=dim)


def create_from_hex(hex_code):
    """Create a color from the hex_code. You can call it with 6 or 3 hexadecimal digits."""

    if len(hex_code) == 6:
        red = int(hex_code[0:2])
        green = int(hex_code[2:4])
        blue = int(hex_code[4:6])

        return RGBColor(red=red, green=green, blue=blue)

    elif len(hex_code) == 3:
        red = int(hex_code[0]) * 16
        green = int(hex_code[1]) * 16
        blue = int(hex_code[2]) * 16

        return RGBColor(red=red, green=green, blue=blue)

    else:
        exit(1)


def create_inverse(color):
    """Create the inverse of the color."""

    if isinstance(color, RGBColor):
        red = color.get_red()
        green = color.get_green()
        blue = color.get_blue()

        return RGBColor(red=red, green=green, blue=blue)

    # return RGBColor.sub_color(RGBColor.White, color)


def add_color(color, other):
    """Add the colors by value."""

    if isinstance(color, RGBColor) and isinstance(other, RGBColor):
        red = color.get_red() + other.get_red()
        green = color.get_green() + other.get_green()
        blue = color.get_blue() + other.get_blue()

        if red > RGBColor.MAX_DIM:
            red = RGBColor.MAX_DIM
        if green > RGBColor.MAX_DIM:
            green = RGBColor.MAX_DIM
        if blue > RGBColor.MAX_DIM:
            blue = RGBColor.MAX_DIM

        return RGBColor(red=red, green=green, blue=blue)


def sub_color(color, other):
    """Subtract the colors by value."""

    if isinstance(color, RGBColor) and isinstance(other, RGBColor):
        red = color.get_red() - other.get_red()
        green = color.get_green() - other.get_green()
        blue = color.get_blue() - other.get_blue()

        if red < RGBColor.MIN_DIM:
            red = RGBColor.MIN_DIM
        if green < RGBColor.MIN_DIM:
            green = RGBColor.MIN_DIM
        if blue < RGBColor.MIN_DIM:
            blue < RGBColor.MIN_DIM

        return RGBColor(red=red, green=green, blue=blue)


def brighter_color(color):
    """Increase the brightness of the color."""

    if isinstance(color, RGBColor):
        return add_color(color, create_brightness(1))


def darker_color(color):
    """Decrease the brightness of the color."""

    if isinstance(color, RGBColor):
        return sub_color(color, create_brightness(1))


# Create one channels pure
RED = create_rgb(r=RGBColor.MAX_DIM)
BLUE = create_rgb(b=RGBColor.MAX_DIM)
GREEN = create_rgb(g=RGBColor.MAX_DIM)


# Create two channels pure
YELLOW = create_rgb(r=RGBColor.MAX_DIM, g=RGBColor.MAX_DIM)
MAGENTA = create_rgb(r=RGBColor.MAX_DIM, b=RGBColor.MAX_DIM)
CYAN = create_rgb(g=RGBColor.MAX_DIM, b=RGBColor.MAX_DIM)


# Create one channel pure the other channel medium
ORANGE = create_rgb(r=RGBColor.MAX_DIM, g=RGBColor.MAX_DIM/2)
PURPLE = create_rgb(r=RGBColor.MAX_DIM, b=RGBColor.MAX_DIM/2)

LIME = create_rgb(r=RGBColor.MAX_DIM/2, g=RGBColor.MAX_DIM)
ROYAL = create_rgb(g=RGBColor.MAX_DIM, b=RGBColor.MAX_DIM/2)

PINK = create_rgb(r=RGBColor.MAX_DIM/2, b=RGBColor.MAX_DIM)
AZURE = create_rgb(g=RGBColor.MAX_DIM/2, b=RGBColor.MAX_DIM)


# Create main grey scale colors
BLACK = create_brightness(RGBColor.MIN_DIM)
WHITE = create_brightness(RGBColor.MAX_DIM)
GREY = create_brightness(RGBColor.MAX_DIM/2)
