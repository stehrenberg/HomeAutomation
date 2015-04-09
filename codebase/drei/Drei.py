import multiprocessing

from manager.Manager import Manager

from crawler.Crawler import Crawler
from webserver.Server import Server


__author__ = 's.jahreiss'

if __name__ == '__main__':
    print("Starting Drei")

    # Initialize the message queue for crawler and manager
    crawler_manager_queue = multiprocessing.Queue()

    # Initialize the message queue for manager and webserver
    manager_webserver_queue = multiprocessing.Queue()

    # Start the crawler
    crawler = Crawler(crawler_manager_queue)
    crawler.start()

    # Start the manager
    manager = Manager(crawler_manager_queue, manager_webserver_queue)
    manager.start()

    # Start the webserver
    webserver = Server(manager_webserver_queue)
    webserver.start()

    # Wait until both processes end
    crawler_manager_queue.close()
    crawler_manager_queue.join_thread()
    crawler.join()
    manager.join()
    webserver.join()