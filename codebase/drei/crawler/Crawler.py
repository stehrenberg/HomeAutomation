import multiprocessing
import time
import re
import subprocess

__author__ = 's.jahreiss'


class Crawler(multiprocessing.Process):

    def __init__(self, manager_queue, dummy=True):
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue
        self.dummy = dummy

    def run(self):
        print("Crawler: Running")

        # dummy mode, send addresses in random time slices
        if self.dummy:
            while True:
                time.sleep(2)
                self.manager_queue.put(['1', '00:80:41:ae:fd:7e'])
                print("New peer connected: ", '00:80:41:ae:fd:7e')
                time.sleep(2)
                self.manager_queue.put(['1', '00:80:41:ae:fd:7d'])
                print("New peer connected: ", '00:80:41:ae:fd:7d')
                time.sleep(2)
                self.manager_queue.put(['0', '00:80:41:ae:fd:7e'])
                print("Peer disconnected: ", '00:80:41:ae:fd:7e')
                time.sleep(2)
                self.manager_queue.put(['0', '00:80:41:ae:fd:7d'])
                print("Peer disconnected: ", '00:80:41:ae:fd:7d')

        # listen of events from WIFI interface
        else:
            # regex pattern for iwevent messages
            pattern = re.compile('(.*?)\s+(.*?)\s+([\w|\s]+):(.*)$')

            # spaw new iwevent process and capture output
            result = subprocess.Popen("iwevent", shell=True, stdout=subprocess.PIPE)

            # each line is a new event
            for line in result.stdout:
                matcher = pattern.search(line.decode("utf-8"))
                if matcher:
                    # new peer connected
                    if "Registered" in matcher.group(3):
                        print("New peer connected: " + matcher.group(4))
                        self.manager_queue.put(['1', matcher.group(4)])

                    # peer disconnected
                    elif "Expired" in matcher.group(3):
                        print("Peer disconnected: " + matcher.group(4))
                        self.manager_queue.put(['0', matcher.group(4)])

        print("Crawler exited")
