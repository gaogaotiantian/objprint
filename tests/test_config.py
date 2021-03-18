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


class Element:
    def __init__(self):
        self.a = "east"
        self.b = "west"
        self.c = "north"


class Depth1:
    def __init__(self):
        self.a = Depth2()


class Depth2:
    def __init__(self):
        self.a = Element()


class MultiDepth:
    def __init__(self):
        self.name = "depthTest"
        self.first = Depth1()


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

    def test_element(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(Element(), elements=2)
            output = buf.getvalue()
        expected = "<Element\n  .a = 'east',\n  .b = 'west',\n  ...\n>\n"
        self.assertEqual(output, expected)

    def test_depth(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(MultiDepth(), depth=2)
            output = buf.getvalue()
        self.assertTrue("Depth1" in output)
        self.assertTrue("Depth2" in output)
        self.assertFalse("Element" in output)
