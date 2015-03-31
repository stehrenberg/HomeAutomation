__author__ = 'markus'


class WritePipe:

    def __init__(self, filename):
        """
        """
        self.pipe = open(filename, 'w')

    def notify(self, content):
        self.pipe.write(content)

    def close(self):
        self.pipe.close()