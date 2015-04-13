import multiprocessing
import time

__author__ = 's.jahreiss'


class Crawler(multiprocessing.Process):
    def __init__(self, manager_queue):
        multiprocessing.Process.__init__(self)
        self.manager_queue = manager_queue

    def run(self):
        print("Crawler: Running")

        # TODO: add logic

        while True:
            time.sleep(2)
            self.manager_queue.put(['a1', 'a2'])
            time.sleep(2)
            self.manager_queue.put(['a1', 'b2'])
            time.sleep(2)
            self.manager_queue.put(['b2', 'a3'])
            print("Crawler: Sent some addresses")