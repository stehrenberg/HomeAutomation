__author__ = 'Luis'

import DmxConnection as dmxConn
from time import sleep


class TubeController(object):
    def __init__(self):
        # TODO Put it in a thread
        # TODO It needs a do while loop for testing the different ports
        self.tube = dmxConn.DMXConnection(comport='/dev/ttyUSB0')

    def start(self):
        try:
            while True:
                self.knightrider()

        except KeyboardInterrupt:
            print "tube: KeyboardInterrupt"
            self.clear()

    def setrgb(self, pixel, r, g, b):
        self.tube.setChannel((3 * pixel) + 3, r)
        self.tube.setChannel((3 * pixel) + 1, g)
        self.tube.setChannel((3 * pixel) + 2, b)

    def knightrider(self):
        for i in range(16):
            self.setrgb((i - 1) % 16, 0, 0, 0)
            self.setrgb(i, 255, 0, 0)
            self.tube.render()
            sleep(.07)

        for i in range(15, 0, -1):
            self.setrgb(i, 255, 0, 0)
            self.setrgb((i + 1) % 16, 0, 0, 0)
            self.tube.render()
            sleep(.07)

    def clear(self):
        for i in range(16):
            self.setrgb(i, 0, 0, 0)

        self.tube.render()


if __name__ == '__main__':
    tube = TubeController()

    tube.start()
