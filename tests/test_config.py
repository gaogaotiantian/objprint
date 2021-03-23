import unittest
import io
from contextlib import redirect_stdout

from objprint import config, objprint


class ElementNum:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3


class TestConfig(unittest.TestCase):
    def test_config_none_exist(self):
        self.assertRaises(TypeError, lambda: config(height=50))

    def test_config_element(self):
        config(elements=2)
        e = ElementNum()
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(e)
            output = buf.getvalue()
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertNotIn("3", output)
        config(elements=None)
