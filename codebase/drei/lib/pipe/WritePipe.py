__author__ = 'markus'


class WritePipe:

    def __init__(self, filename):
        """ Open file for pipe
        """
        self.pipe = open(filename, 'w')

    def notify(self, content):
        """ Write MAC-Address in pipe
        """
        self.pipe.write(content)

    def close(self):
        self.pipe.close()