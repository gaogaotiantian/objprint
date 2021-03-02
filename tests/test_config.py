import unittest
import io
from contextlib import redirect_stdout
from objprint import config, objprint


class B:
    pass


class TestConfig(unittest.TestCase):
    def test_config(self):
        self.assertRaises(TypeError, lambda: config(height=50))

    def test_objprint(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(B(), indent=5, depth=2, width=60)
            self.assertTrue(len(buf.getvalue()) > 0)
