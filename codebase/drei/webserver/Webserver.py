import multiprocessing
from thread import start_new_thread

from webserver import Webservices
from webserver.Webservices import notify_active_users


__author__ = 's.jahreiss'


class Webserver(multiprocessing.Process):
    """
    Represents the webserver. It starts a RESTful and a websocket service.
    """

    def __init__(self, manager_queue):
        """
        Constructor of the webserver.
        :param manager_queue: The queue which will be used to retrieve messages from the manager.
        :return: A new webserver.
        """
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue

    def run(self):
        """
        Starts the webserver.
        """
        print("Webserver: Running on http://127.0.0.1:8080")

        start_new_thread(self.notify, ())

        # Initialize the RESTful and Websocket services.
        Webservices.start()

    def notify(self):
        while True:
            user_list = self.manager_queue.get()
            notify_active_users(user_list)