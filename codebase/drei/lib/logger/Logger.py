import logging
import inspect
import ntpath

__author__ = 'markus'


class Logger:
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(message)s')

    def log(self, level, message):
        # Retrieve caller
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        # Get caller filename
        name = ntpath.basename(caller.filename)
        logging.log(level, name + " (" + str(caller.lineno) + ") " + message)
