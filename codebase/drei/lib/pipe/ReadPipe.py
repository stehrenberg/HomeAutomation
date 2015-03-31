from thread import start_new_thread

__author__ = 'markus'


class ReadPipe:

    def __init__(self, filename):
        """
        """
        self.pipe = open(filename, 'r')
        self.functions = []
        self.run = True
        start_new_thread(self.read, ())

    def register(self, function):
        self.functions.append(function)

    def close(self):
        self.run = False

    def read(self):
        while self.run:
            content = self.pipe.read()
            for function in self.functions:
                function(content)
        self.pipe.close()
