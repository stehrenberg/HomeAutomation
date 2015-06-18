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

    def __init__(self, manager_webserver_queue, manager_control_queue):
        """
        Comanager_gueuenstructor of the webserver.
        :param manager_webserver_queue: The queue which will be used to retrieve messages from the manager.
        :return: A new webserver.
        """
        multiprocessing.Process.__init__(self)
        self.manager_webserver_queue = manager_webserver_queue
        self.manager_control_queue = manager_control_queue
        self.logger = Logger()

    def run(self):
        """
        Starts the webserver in a own thread.
        """
        self.logger.log(Logger.INFO, "Running on http://127.0.0.1:8080")
        print("Webserver: Running on http://127.0.0.1:8080")

        start_new_thread(self.notify, ())

        # Initialize the RESTful and Websocket services.
        Webservices.manager_control_queue = self.manager_control_queue
        Webservices.start()

    def notify(self):
        """
        Blocks until the manager adds new user list to the queue and afterwards notifies all clients.
        """
        while True:
            # Retrieve user list.
            user_list = self.manager_webserver_queue.get()
            # Notify clients.
            notify_active_users(user_list)
