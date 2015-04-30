from gpio import GPIO

__author__ = 'maxi'


class LED(object):

    CRAWLER = 17
    MANAGER = 27
    WEBSERVER = 22

    def __init__(self, pin):
        GPIO.export(pin)
        GPIO.direction(pin, GPIO.DIR_OUT)

        self._pin = pin
        self._value = GPIO.VAL_LOW

    def on(self):
        GPIO.value(self._pin, GPIO.VAL_HIGH)
        self._value = GPIO.VAL_HIGH

    def off(self):
        GPIO.value(self._pin, GPIO.VAL_LOW)
        self._value = GPIO.VAL_LOW

    def toggle(self):
        if self.value() == GPIO.VAL_HIGH:
            self.off()
        elif self.value() == GPIO.VAL_LOW:
            self.on()

    def value(self):
        return self._value