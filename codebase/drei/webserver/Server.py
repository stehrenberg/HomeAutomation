import multiprocessing

from webserver.RestEndpoint import start_rest_endpoint


__author__ = 's.jahreiss'


class Server(multiprocessing.Process):
    def __init__(self, manager_queue):
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue

    def run(self):
        print("Webserver: Running at http://127.0.0.1:5000")

        # Initialize the RESTful webservice
        start_rest_endpoint()