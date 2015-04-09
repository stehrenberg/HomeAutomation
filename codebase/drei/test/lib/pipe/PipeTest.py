from lib.pipe.ReadPipe import ReadPipe
from lib.pipe.WritePipe import WritePipe
from unittest.mock import Mock

__author__ = 'markus'

import time
import unittest


class PipeTest(unittest.TestCase):
    first_test = False
    second_test = False

    def setUp(self):
        self.write_pipe = WritePipe("./testpipe")
        self.read_pipe = ReadPipe("./testpipe")
        self.test_string = "test123"

    def example_function_positive(self, content):
        self.assertEqual(content, self.test_string)
        PipeTest.first_test = True
        print("blub")

    def example_function_negative(self, content):
        self.assertNotEqual(content, "bla")
        PipeTest.second_test = True
        print("bla")
        self.read_pipe.close()

    def test_read_write(self):
        funktion1 = Mock()
        self.read_pipe.register(funktion1)
        """self.read_pipe.register(self.example_function_negative)"""

        self.write_pipe.notify(self.test_string)
        funktion1.assert_called_with(self.test_string)

        time.sleep(1)
        self.write_pipe.close()