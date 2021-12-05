# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import io
import json

from objprint import op
from objprint.color_util import COLOR
from .objtest import ObjTest, ObjprintTestCase


class TestObjprint(ObjprintTestCase):
    def test_op(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            b = ObjTest({})
            op(b, indent=5, depth=2, width=60)
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_multiple(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            op(1, 2)
            output = buf.getvalue()

        expectedString = "1\n2\n"
        self.assertEqual(expectedString, output)

    def test_json(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            b = ObjTest({"name": "Lisa", "age": 19})
            op(b, format="json")
            output = buf.getvalue()
        self.assertEqual(output, json.dumps({".type": "ObjTest", "name": "Lisa", "age": 19}) + "\n")

        with io.StringIO() as buf, redirect_stdout(buf):
            b = ObjTest({"name": "Lisa", "age": 19})
            op(b, format="json", indent=2)
            output = buf.getvalue()
        self.assertEqual(output, json.dumps({".type": "ObjTest", "name": "Lisa", "age": 19}, indent=2) + "\n")

    def test_config_indent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Alpha"})
            op(obj, indent=3)
            output = buf.getvalue()

        expectedString = "<ObjTest\n   .name = 'Alpha'\n>\n"
        self.assertEqual(expectedString, output)

    def test_config_width(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ['a', 'b']})
            op(obj, width=10)
            output = buf.getvalue()
        lst = "<ObjTest\n  .lst = ['a', 'b']\n>\n"
        self.assertEqual(output, lst)

    def test_config_width_fail(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ["This", "is", "for", "testing"]})
            op(obj, width=5)
            output = buf.getvalue()
        expected = "<ObjTest\n  .lst = [\n    'This',\n    'is',\n    'for',\n    'testing'\n  ]\n>\n"
        self.assertEqual(output, expected)

    def test_element(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"first": "east", "second": "west", "third": "north"})
            op(obj, elements=2)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertNotIn("third", output)
        # Make sure when elements is large, it can also handle the case
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"first": "east", "second": "west", "third": "north"})
            op(obj, elements=10)
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

            op(multiDepth, depth=2)
            output = buf.getvalue()
        self.assertIn("depthTest", output)
        self.assertIn("depth1", output)
        self.assertNotIn("depth2", output)
        self.assertNotIn("element", output)

    def test_print_methods(self):
        class ObjWithMethods:
            def obj_method(self, method_arg, **kwargs):
                pass

            def __eq__(self):
                # this should be ignored
                pass

        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjWithMethods()
            op(obj, print_methods=True)
            output = buf.getvalue()

        expected = "<ObjWithMethods\n  def obj_method(method_arg, **kwargs)\n>\n"
        self.assertEqual(output, expected)

    def test_config_include(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            op(obj, indent=1, include=['elem1', 'elem2'])
            output = buf.getvalue()
        expected = "<ObjTest\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)

    def test_config_exclude(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            op(obj, indent=1, exclude=['elem3'])
            output = buf.getvalue()
        expected = "<ObjTest\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertEqual(expected, output)

    def test_color_without_label(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Lisa"})
            op(obj, color=True)
            output = buf.getvalue()
        self.assertIn(COLOR.CYAN, output)
        self.assertIn(COLOR.GREEN, output)
        self.assertIn(COLOR.DEFAULT, output)

    def test_color_with_label(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"name": "Lisa", "age": 19})
            op(obj, color=True, label=["age"])
            output = buf.getvalue()
        self.assertIn(COLOR.YELLOW, output)
        self.assertIn(COLOR.DEFAULT, output)

    def test_color_with_print_methods(self):
        class ObjWithMethods:
            def obj_method(self, method_arg, **kwargs):
                pass

        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjWithMethods()
            op(obj, print_methods=True, color=True)
            output = buf.getvalue()

        self.assertIn(COLOR.MAGENTA, output)
        self.assertIn("obj_method", output)

    def test_no_color(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"Age": 10, "grade": 5})
            op(obj, color=False)
            output = buf.getvalue()
        self.assertNotIn(COLOR.CYAN, output)
        self.assertNotIn(COLOR.DEFAULT, output)

    def test_label_only(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"Age": 10, "grade": 5})
            op(obj, color=False, label=['grade'])
            output = buf.getvalue()
        self.assertNotIn(COLOR.CYAN, output)
        self.assertIn(COLOR.YELLOW, output)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            op({}, invalid="invalid")

        with self.assertRaises(TypeError):
            op({}, exclude="invalid")
