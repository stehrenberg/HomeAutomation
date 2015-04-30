from __future__ import print_function
import os
import time
import platform


class GPIO(object):

    DIR_OUT = "out"
    DIR_INT = "in"

    VAL_HIGH = "1"
    VAL_LOW = "0"

    @staticmethod
    def _write(file, content):
        if platform.machine() == "armv7l":
            f = open("/sys/class/gpio/" + file, "w")
            f.write(content)
            f.close()

    @staticmethod
    def export(gpionum):
        if not os.path.isdir("/sys/class/gpio/gpio" + str(gpionum)):
            GPIO._write("export", str(gpionum))

        # give the kernel module some time
        # to setup the sysfs interface
        time.sleep(0.08)


    @staticmethod
    def unexport(gpionum):
        GPIO._write("unexport", str(gpionum))

    @staticmethod
    def direction(gpionum, direction):
        GPIO._write("gpio" + str(gpionum) + "/direction", direction)

    @staticmethod
    def value(gpionum, value):
        GPIO._write("gpio" + str(gpionum) + "/value", value)