import multiprocessing
import time
import re
import subprocess
from lib.led.led import LED
from lib.logger.Logger import Logger

__author__ = 's.jahreiss'


class Crawler(multiprocessing.Process):
    def __init__(self, manager_queue, dummy=True):
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue
        self.dummy = dummy
        self.led = LED(LED.CRAWLER)
        self.logger = Logger()

    def _notify(self, state, mac):
        # print a pretty message
        if state == '1':
            self.logger.log(Logger.INFO, "New peer connected: " + str(mac))
        elif state == '0':
            self.logger.log(Logger.INFO, "New peer disconnected: " + str(mac))

        # send new mac to manager
        self.manager_queue.put([state, mac])

        # toggle the status led for 100ms
        self.led.toggle()
        time.sleep(0.1)
        self.led.toggle()

    def run(self):
        self.logger.log(Logger.INFO, "Running")
        print("Logger running")
        self.led.on()

        # dummy mode, send addresses in random time slices
        if self.dummy:
            while True:
                time.sleep(2)
                self._notify('1', '00:80:41:ae:fd:7e')
                time.sleep(2)
                self._notify('1', '00:80:41:ae:fd:7d')
                time.sleep(2)
                self._notify('0', '00:80:41:ae:fd:7e')
                time.sleep(2)
                self._notify('0', '00:80:41:ae:fd:7d')

        # listen of events from WIFI interface
        else:
            # regex pattern for iwevent messages
            pattern = re.compile('(.*?)\s+(.*?)\s+([\w|\s]+):(.*)$')

            # spaw new iwevent process and capture output
            result = subprocess.Popen("/sbin/iwevent", shell=False, stdout=subprocess.PIPE)

            # each line is a new event
            while True:
                line = result.stdout.readline()
                if line == '':
                    break

                # parse output
                matcher = pattern.search(line.decode("utf-8"))
                if matcher:
                    # new peer connected
                    if "Registered" in matcher.group(3):
                        self.logger.log(Logger.INFO, "New peer connected: " + matcher.group(4))
                        self.manager_queue.put(['1', matcher.group(4)])

                    # peer disconnected
                    elif "Expired" in matcher.group(3):
                        self.logger.log(Logger.INFO, "Peer disconnected: " + matcher.group(4))
                        self.manager_queue.put(['0', matcher.group(4)])

                    # toggle the status led for 100ms
                    self.led.toggle()
                    time.sleep(0.1)
                    self.led.toggle()

        self.logger.log("Exited")
        self.led.off()
