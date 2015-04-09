import multiprocessing
from manager.Manager import Manager
from crawler.Crawler import Crawler


__author__ = 's.jahreiss'

if __name__ == '__main__':
    print("Starting Drei")

    # Initialize the message queue for crawler and manager
    crawler_manager_queue = multiprocessing.Queue()

    # Start the crawler
    crawler = Crawler(crawler_manager_queue)
    crawler.start()

    # Start the manager
    manager = Manager(crawler_manager_queue)
    manager.start()

    # Wait until both processes end
    crawler_manager_queue.close()
    crawler_manager_queue.join_thread()
    crawler.join()
    manager.join()