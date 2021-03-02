import unittest
import io
from contextlib import redirect_stdout

from objprint import add_objprint
from objprint import objprint


@add_objprint
class B:
    def __init__(self):
        self.name = "Lisa"
        self.age = 19


class TestDecorator(unittest.TestCase):
    def test_add_op(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            print(B())
            output = buf.getvalue()

        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(B())
            expected = buf.getvalue()

        self.assertEqual(expected, output)
