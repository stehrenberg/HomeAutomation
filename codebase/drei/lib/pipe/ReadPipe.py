from threading import _start_new_thread

__author__ = 'markus'


class ReadPipe:

    def __init__(self, filename):
        """ Open file for pipe, create array for functions, start reading
        """
        self.pipe = open(filename, 'r')
        self.functions = []
        self.run = True
        _start_new_thread(self.read, ())

    def register(self, function):
        """ Insert function in function array
        """
        self.functions.append(function)

    def close(self):
        """ Stop reading
        """
        self.run = False

    def read(self):
        while self.run:
            """ Reads MAC-Address from the pipe, calls all functions in array with
                MAC-Address as parameter
            """
            content = self.pipe.read()
            for function in self.functions:
                function(content)
        self.pipe.close()
