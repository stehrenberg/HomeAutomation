#!/usr/bin/env python
from __future__ import print_function
import os
import time


class GPIO(object):

    DIR_OUT = "out"
    DIR_INT = "in"

    VAL_HIGH = "1"
    VAL_LOW = "0"

    def _write(self, file, content):
        f = open("/sys/class/gpio/" + file, "w")
        f.write(content)
        f.close()

    def export(self, gpionum):
        if not os.path.isdir("/sys/class/gpio/gpio" + str(gpionum)):
            self._write("export", str(gpionum))

    def unexport(self, gpionum):
        self._write("unexport", str(gpionum))

    def direction(self, gpionum, direction):
        self._write("gpio" + str(gpionum) + "/direction", direction)

    def value(self, gpionum, value):
        self._write("gpio" + str(gpionum) + "/value", "1")



g = GPIO()
g.export(18)
time.sleep(0.05)
g.direction(18, GPIO.DIR_OUT)
g.value(18, GPIO.VAL_HIGH)
