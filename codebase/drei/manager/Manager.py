import multiprocessing

__author__ = 's.jahreiss'


class Manager(multiprocessing.Process):
    def __init__(self, crawler_queue, webserver_queue):
        multiprocessing.Process.__init__(self)
        self.crawler_queue = crawler_queue
        self.webserver_queue = webserver_queue

    def run(self):
        print("Manager: Running")

        # TODO: add logic

        while True:
            addresses = self.crawler_queue.get()
            print("Manager: Retrieved addresses")