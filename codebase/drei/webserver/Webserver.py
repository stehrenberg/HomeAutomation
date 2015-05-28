import multiprocessing
from thread import start_new_thread

from webserver import Webservices
from webserver.Webservices import notify_active_users
from lib.logger.Logger import Logger


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
        self.logger = Logger()

    def run(self):
        """
        Starts the webserver in a own thread.
        """
        self.logger.log(Logger.INFO, "Webserver: Running on http://127.0.0.1:8080")

        start_new_thread(self.notify, ())

        # Initialize the RESTful and Websocket services.
        Webservices.start()

    def notify(self):
        """
        Blocks until the manager adds new user list to the queue and afterwards notifies all clients.
        """
        while True:
            # Retrieve user list.
            user_list = self.manager_queue.get()
            # Notify clients.
            notify_active_users(user_list)
