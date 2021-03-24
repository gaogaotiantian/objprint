import unittest
import io
from contextlib import redirect_stdout

from objprint import objprint


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


class Element:
    def __init__(self):
        self.first = "east"
        self.second = "west"
        self.third = "north"


class Depth1:
    def __init__(self):
        self.attri = Depth2()


class Depth2:
    def __init__(self):
        self.attri = Element()


class MultiDepth:
    def __init__(self):
        self.name = "depthTest"
        self.first = Depth1()


class WithConfig:
    def __init__(self):
        self.elem1 = 1
        self.elem2 = 2
        self.elem3 = 3


class TestObjprint(unittest.TestCase):
    def test_objprint(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(B(), indent=5, depth=2, width=60)
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_config_indent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigContent(), indent=3)
            output = buf.getvalue()

        expectedString = "<ConfigContent\n   .name = 'Alpha'\n>\n"
        self.assertEqual(expectedString, output)

    def test_config_width(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigWidth(), width=10)
            output = buf.getvalue()
        lst = "<ConfigWidth\n  .lst = ['a', 'b']\n>\n"
        self.assertEqual(output, lst)

    def test_config_width_fail(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(ConfigWidth2(), width=5)
            output = buf.getvalue()
        expected = "<ConfigWidth2\n  .lst = [\n    'This',\n    'is',\n    'for',\n    'testing'\n  ]\n>\n"
        self.assertEqual(output, expected)

    def test_element(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(Element(), elements=2)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertNotIn("third", output)

    def test_depth(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(MultiDepth(), depth=2)
            output = buf.getvalue()
        self.assertIn("Depth1", output)
        self.assertIn("Depth2", output)
        self.assertNotIn("Element", output)

    def test_config_include(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(WithConfig(), indent=1, include=['elem1', 'elem2'])
            output = buf.getvalue()
        expected = "<WithConfig\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)

    def test_config_exclude(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(WithConfig(), indent=1, exclude=['elem3'])
            output = buf.getvalue()
        expected = "<WithConfig\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)
