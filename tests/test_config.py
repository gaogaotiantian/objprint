import unittest
import io
from contextlib import redirect_stdout

from objprint import config, objprint


class ElementNum:
    def __init__(self):
        self.first = 1
        self.second = 2
        self.third = 3


class TestConfig(unittest.TestCase):
    def test_config_none_exist(self):
        self.assertRaises(TypeError, lambda: config(height=50))

    def test_config_element(self):
        config(elements=2)
        e = ElementNum()
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(e)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertNotIn("third", output)
        config(elements=None)
