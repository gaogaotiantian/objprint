import unittest
import io
from contextlib import redirect_stdout

from objprint import objprint
from .objtest import ObjTest


class TestObjprint(unittest.TestCase):
    def test_objprint(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            b = ObjTest({})
            objprint(b, indent=5, depth=2, width=60)
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_config_indent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Alpha"})
            objprint(obj, indent=3)
            output = buf.getvalue()

        expectedString = "<ObjTest\n   .name = 'Alpha'\n>\n"
        self.assertEqual(expectedString, output)

    def test_config_width(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ['a', 'b']})
            objprint(obj, width=10)
            output = buf.getvalue()
        lst = "<ObjTest\n  .lst = ['a', 'b']\n>\n"
        self.assertEqual(output, lst)

    def test_config_width_fail(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ["This", "is", "for", "testing"]})
            objprint(obj, width=5)
            output = buf.getvalue()
        expected = "<ObjTest\n  .lst = [\n    'This',\n    'is',\n    'for',\n    'testing'\n  ]\n>\n"
        self.assertEqual(output, expected)

    def test_element(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"first": "east", "second": "west", "third": "north"})
            objprint(obj, elements=2)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertNotIn("third", output)

    def test_depth(self):
        with io.StringIO() as buf, redirect_stdout(buf):

            e = ObjTest({"element": "east", "second": "west"})
            depth2 = ObjTest({"attri": e, "inDepth2": "depth2"})
            depth1 = ObjTest({"content": depth2, "inDepth1": "depth1"})
            multiDepth = ObjTest({"name": "depthTest", "first": depth1})

            objprint(multiDepth, depth=2)
            output = buf.getvalue()
        self.assertIn("depthTest", output)
        self.assertIn("depth1", output)
        self.assertNotIn("depth2", output)
        self.assertNotIn("element", output)

    def test_config_include(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            objprint(obj, indent=1, include=['elem1', 'elem2'])
            output = buf.getvalue()
        expected = "<ObjTest\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)

    def test_config_exclude(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            objprint(obj, indent=1, exclude=['elem3'])
            output = buf.getvalue()
        expected = "<ObjTest\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)
