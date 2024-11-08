# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import code
from contextlib import redirect_stdout
import io
import json
import re
import sys
from unittest.mock import patch

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

    def test_return(self):
        obj = ObjTest({})
        obj2 = ObjTest({})
        with io.StringIO() as buf, redirect_stdout(buf):
            obj_ret = op(obj)
            self.assertIs(obj_ret, obj)
            obj_ret1, obj_ret2 = op(obj, obj2)
            self.assertIs(obj_ret1, obj)
            self.assertIs(obj_ret2, obj2)
            self.assertEqual(pow(*op(3, 2)), 9)

    def test_enable(self):
        obj = ObjTest({})
        with io.StringIO() as buf, redirect_stdout(buf):
            op(obj, enable=False)
            output = buf.getvalue()
            self.assertEqual(output, "")

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

    def test_json_with_arg_name(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            unique_name = ObjTest({"name": "Lisa", "age": 19})
            op(unique_name, format="json", arg_name=True)
            output = buf.getvalue()
        self.assertIn(json.dumps({".type": "ObjTest", "name": "Lisa", "age": 19}), output)
        self.assertIn("b", output)

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

        expectedString = r"<ObjTest 0x[0-9a-fA-F]*\n   .name = 'Alpha'\n>\n"
        self.assertRegex(output, expectedString)

    def test_config_width(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ['a', 'b']})
            op(obj, width=10)
            output = buf.getvalue()
        lst = r"<ObjTest 0x[0-9a-fA-F]*\n  .lst = \['a', 'b'\]\n>\n"
        self.assertRegex(output, lst)

    def test_config_width_fail(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"lst": ["This", "is", "for", "testing"]})
            op(obj, width=5)
            output = buf.getvalue()
        expected = r"<ObjTest .*\n  .lst = \[\n    'This',\n    'is',\n    'for',\n    'testing'\n  \]\n>\n"
        self.assertRegex(output, re.compile(expected, re.DOTALL))

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

        expected = r"<ObjWithMethods 0x[0-9a-fA-F]*\n  def obj_method\(method_arg, \*\*kwargs\)\n>\n"
        self.assertRegex(output, expected)

    def test_line_number(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({})
            op(obj, line_number=True, color=False)
            output = buf.getvalue()

        first_line = output.split("\n")[0]
        self.assertIn("test_line_number", first_line)
        self.assertIn("test_objprint", first_line)

    def test_arg_name(self):
        obj = ObjTest({})
        with io.StringIO() as buf, redirect_stdout(buf):
            op(obj, arg_name=True, color=False)
            output = buf.getvalue()
        self.assertIn("obj:", output.split("\n")[0])

        obj = ObjTest({})
        with io.StringIO() as buf, redirect_stdout(buf):
            op(obj, arg_name=True, color=True)
            output = buf.getvalue()
        self.assertIn("obj:", output.split("\n")[0])

        with io.StringIO() as buf, redirect_stdout(buf):
            op(
                obj,
                arg_name=True,
                color=False
            )
            output = buf.getvalue()
        self.assertIn("obj:", output.split("\n")[0])

        d = {"b": [0, 1, 2]}
        with io.StringIO() as buf, redirect_stdout(buf):
            op(
                d["b"][0 + 1],
                obj,
                arg_name=True,
                color=False
            )
            output = buf.getvalue()
        self.assertIn("d[\"b\"][0 + 1]:", output.split("\n")[0])
        self.assertIn("obj", output.split("\n")[2])

        with patch("objprint.executing.Source.executing", return_value=ObjTest({"node": None})):
            with io.StringIO() as buf, redirect_stdout(buf):
                op(obj, arg_name=True, color=False)
                output = buf.getvalue()
            self.assertIn("Unknown", output.split("\n")[0])

        with patch("inspect.currentframe", return_value=None):
            with io.StringIO() as buf, redirect_stdout(buf):
                op(obj, arg_name=True, color=False)
                output = buf.getvalue()
            self.assertIn("Unknown", output.split("\n")[0])

        with patch("inspect.getmodule", return_value=None):
            with io.StringIO() as buf, redirect_stdout(buf):
                op(obj, arg_name=True, color=False)
                output = buf.getvalue()
            self.assertIn("Unknown", output.split("\n")[0])

        with patch("inspect.getsource", side_effect=OSError()):
            with io.StringIO() as buf, redirect_stdout(buf):
                op(obj, arg_name=True, color=False)
                output = buf.getvalue()
            self.assertIn("Unknown", output.split("\n")[0])

    def test_config_attr_pattern(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "attr3": 3})
            op(obj, indent=1, attr_pattern=r"elem.")
            output = buf.getvalue()
        expected = r"<ObjTest 0x[0-9a-fA-F]*\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertRegex(output, expected)

    def test_config_include(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            op(obj, indent=1, include=['elem1', 'elem2'])
            output = buf.getvalue()
        expected = r"<ObjTest 0x[0-9a-fA-F]*\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertRegex(output, expected)

    def test_config_exclude(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"elem1": 1, "elem2": 2, "elem3": 3})
            op(obj, indent=1, exclude=['elem3'])
            output = buf.getvalue()
        expected = r"<ObjTest 0x[0-9a-fA-F]*\n .elem1 = 1,\n .elem2 = 2\n>\n"
        self.assertRegex(output, expected)

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

    def test_color_with_line_number(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({})
            op(obj, line_number=True, color=True)
            output = buf.getvalue()

        first_line = output.split("\n")[0]
        self.assertIn("test_color_with_line_number", first_line)
        self.assertIn("test_objprint", first_line)
        self.assertIn(COLOR.GREEN, first_line)

        with patch("inspect.currentframe", return_value=None):
            with io.StringIO() as buf, redirect_stdout(buf):
                op(obj, line_number=True, color=False)
                output = buf.getvalue()
            self.assertIn("Unknown", output.split("\n")[0])

    def test_no_color(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            obj = ObjTest({"Age": 10, "grade": 5})
            op(obj, color=False)
            output = buf.getvalue()
        self.assertNotIn(COLOR.CYAN, output)
        self.assertNotIn(COLOR.DEFAULT, output)

    def test_unsortable_dict(self):
        d = {1: 2, "a": 3}
        with io.StringIO() as buf, redirect_stdout(buf):
            op(d, color=False)
            output = buf.getvalue()
        self.assertIn("1", output)
        self.assertIn("a", output)

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

    def test_console_return_value(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            console = code.InteractiveConsole()
            console.push("from objprint import op")
            console.push("op([1, 2, 3])")
            output = buf.getvalue()
        self.assertEqual("[1, 2, 3]\n", output)

    def test_exec_return_value(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            exec("from objprint import op")
            exec("op([1,2,3])")
            output = buf.getvalue()
        self.assertEqual("[1, 2, 3]\n", output)

        with io.StringIO() as buf, redirect_stdout(buf):
            exec("from objprint import op")
            exec("op(op([1,2,3]))")
            output = buf.getvalue()
        self.assertEqual("[1, 2, 3]\n[1, 2, 3]\n", output)

        with io.StringIO() as buf, redirect_stdout(buf):
            locals = sys._getframe(1).f_locals
            exec("from objprint import op", globals(), locals)
            exec("b = op([1,2,3])", globals(), locals)
            exec("print(b)", globals(), locals)
            output = buf.getvalue()
        self.assertEqual("[1, 2, 3]\n[1, 2, 3]\n", output)

    def test_inherit(self):
        class BaseClass:
            name = 'A'

        class DerivedClass(BaseClass):
            name = 'B'

        @op.register_formatter(BaseClass)
        def base_formatter(obj: BaseClass) -> str:
            return obj.name

        with io.StringIO() as buf, redirect_stdout(buf):
            op(DerivedClass())
            output = buf.getvalue()
        self.assertEqual("B\n", output)

        @op.register_formatter(DerivedClass)
        def derived_formatter(obj: DerivedClass) -> str:
            return f"DerivedClass, {obj.name}"

        with io.StringIO() as buf, redirect_stdout(buf):
            op(DerivedClass())
            output = buf.getvalue()
        self.assertEqual("DerivedClass, B\n", output)

        op.unregister_formatter()

    def test_attr_exc(self):
        class BadAttrClassA:
            __slots__ = ["a", "b"]

            def __init__(self) -> None:
                self.b = "b"

        class BadAttrClassB(BadAttrClassA):
            __slots__ = []

            @property
            def c(self):
                raise ValueError

        with io.StringIO() as buf, redirect_stdout(buf):
            op(BadAttrClassA())
            with self.assertRaises(ValueError):
                op(BadAttrClassB())
            output = buf.getvalue()
        self.assertNotIn(".a", output)
        self.assertIn(".b", output)
