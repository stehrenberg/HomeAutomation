import multiprocessing
from thread import start_new_thread
import time

from webserver import Webservices
from webserver.Webservices import notify_clients


__author__ = 's.jahreiss'


class Webserver(multiprocessing.Process):
    def __init__(self, manager_queue):
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue

    def run(self):
        print("Webserver: Running on http://127.0.0.1:8080")

        start_new_thread(notify, ())

        # Initialize the RESTful and Websocket services.
        Webservices.start()


def notify():
    while True:
        time.sleep(5)
        notify_clients('Juhu!')