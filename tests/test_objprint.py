# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
from contextlib import redirect_stdout

from objprint import objprint
from objprint.color_util import COLOR
from .objtest import ObjTest, ObjprintTestCase


class TestObjprint(ObjprintTestCase):
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
        # Make sure when elements is large, it can also handle the case
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"first": "east", "second": "west", "third": "north"})
            objprint(obj, elements=10)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertIn("third", output)

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

    def test_color_without_label(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Lisa"})
            objprint(obj, color=True)
            output = buf.getvalue()
        self.assertIn(COLOR.CYAN, output)
        self.assertIn(COLOR.GREEN, output)
        self.assertIn(COLOR.DEFAULT, output)

    def test_color_with_label(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Lisa", "age": 19})
            objprint(obj, color=True, label=["age"])
            output = buf.getvalue()
        self.assertIn(COLOR.YELLOW, output)
        self.assertIn(COLOR.DEFAULT, output)

    def test_no_color(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"Age": 10, "grade": 5})
            objprint(obj, color=False)
            output = buf.getvalue()
        self.assertNotIn(COLOR.CYAN, output)
        self.assertNotIn(COLOR.DEFAULT, output)

    def test_label_only(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"Age": 10, "grade": 5})
            objprint(obj, color=False, label=['grade'])
            output = buf.getvalue()
        self.assertNotIn(COLOR.CYAN, output)
        self.assertIn(COLOR.YELLOW, output)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            objprint({}, invalid="invalid")

        with self.assertRaises(TypeError):
            objprint({}, exclude="invalid")
