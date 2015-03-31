from lib.pipe.ReadPipe import ReadPipe
from lib.pipe.WritePipe import WritePipe

__author__ = 'markus'

import unittest


class PipeTest(unittest.TestCase):

    def setUp(self):
        self.write_pipe = WritePipe("./testpipe")
        self.read_pipe = ReadPipe("./testpipe")
        self.test_string = "test123"

    def example_function_positive(self, content):
        self.assertEqual(content, self.test_string)
        print("blub")

    def example_function_negative(self, content):
        self.assertNotEqual(content, "bla")
        print("bla")
        self.read_pipe.close()

    def test_read_write(self):
        self.read_pipe.register(self.example_function_positive)
        self.read_pipe.register(self.example_function_negative)

        self.write_pipe.notify(self.test_string)
        self.write_pipe.close()