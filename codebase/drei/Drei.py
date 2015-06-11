#!/usr/bin/env python
import multiprocessing
import Const
import platform

from manager.Manager import Manager
from lib.database import InitTables
from crawler.Crawler import Crawler
from webserver.Webserver import Webserver
from lib.logger.Logger import Logger


__author__ = 's.jahreiss'

if __name__ == '__main__':
    logger = Logger()
    logger.log(Logger.INFO, "Starting Drei")
    print("Starting Drei")

    # Initializing database with tables (if necessary)
    InitTables.main()

    # Initialize the message queue for crawler and manager
    manager_queue = multiprocessing.Queue()

    # Initialize the message queue for manager and webserver
    manager_webserver_queue = multiprocessing.Queue()

    # Start the crawler
    crawler = Crawler(manager_queue, platform.machine() != Const.PI_PLATFORM)
    crawler.start()

    # Start the manager
    manager = Manager(manager_queue, manager_webserver_queue)
    manager.start()

    # Start the webserver
    webserver = Webserver(manager_webserver_queue, manager_queue)
    webserver.start()

    # Wait until both processes end
    manager_queue.close()
    manager_queue.join_thread()
    crawler.join()
    manager.join()
    webserver.join()
