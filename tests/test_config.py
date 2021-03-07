import unittest
import io
from contextlib import redirect_stdout
from objprint import config, objprint


class B:
    pass


class ConfigContent:
    def __init__(self):
        self.name = "Alpha"


class ConfigWidth:
    def __init__(self):
        self.lst = ['a', 'b']


class ConfigWidth2:
    def __init__(self):
        self.lst = ["This", "is", "for", "testing"]


class TestConfig(unittest.TestCase):
    def test_config(self):
        self.assertRaises(TypeError, lambda: config(height=50))

    def test_objprint(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(B(), indent=5, depth=2, width=60)
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_configIndent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigContent(), indent=3)
            output = buf.getvalue()

        expectedString = "<ConfigContent\n   .name = 'Alpha'\n>\n"
        self.assertEqual(expectedString, output)

    def test_configWidth(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigWidth(), width=10)
            output = buf.getvalue()
        lst = "<ConfigWidth\n  .lst = ['a', 'b']\n>\n"
        self.assertEqual(output, lst)

    def test_configWidth_fail(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigWidth2(), width=5)
            output = buf.getvalue()
        expected = "<ConfigWidth2\n  .lst = [\n    'This',\n    'is',\n    'for',\n    'testing'\n  ]\n>\n"
        self.assertEqual(output, expected)
