# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
import random
from objprint import objstr
from .objtest import ObjTest, ObjprintTestCase


class TestObjStr(ObjprintTestCase):
    def test_list(self):
        lsts = (
            ([], "[]"),
            ([1, 2], "[1, 2]"),
            ([1, 'a'], "[1, 'a']"),
            ([123, 'a' * 100], f"[\n  123,\n  '{'a' * 100}'\n]")
        )
        for obj, s in lsts:
            self.assertEqual(objstr(obj), s)

    def test_tuple(self):
        lsts = (
            ((), "()"),
            ((1, 2), "(1, 2)"),
            ((1, 'a'), "(1, 'a')")
        )
        for obj, s in lsts:
            self.assertEqual(objstr(obj), s)

    def test_dict(self):
        lsts = (
            ({}, "{}"),
            ({"Age": "19"}, "{'Age': '19'}"),
            ({"Number": 1, "Letter": 'a'}, "{'Letter': 'a', 'Number': 1}")
        )
        for obj, s in lsts:
            self.assertEqual(objstr(obj), s)

    def test_one_line_object(self):
        s = io.StringIO()
        self.assertNotIn("\n", objstr(s))

    def test_get_ellipsis(self):
        obj = ObjTest({})
        self.assertEqual("<ObjTest ... >", objstr(obj, 5))

    def test_None(self):
        self.assertEqual('None', objstr(None))

    def test_function_type(self):
        def run(self):
            print("my car can run!")
        obj = ObjTest({"brand": "a", "function": run})
        self.assertEqual("<function run>", objstr(obj.function))

    def test_include(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        output = objstr(t, include=['pos1'])
        self.assertIn("pos1", output)
        self.assertNotIn("pos2", output)
        self.assertNotIn("pos3", output)

    def test_exclude(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        output = objstr(t, exclude=['pos2', 'pos3'])
        self.assertIn("pos1", output)
        self.assertNotIn("pos2", output)
        self.assertNotIn("pos3", output)

    def test_exclude_indent(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        expected = "<ObjTest\n    .pos1 = 'in'\n  >"
        self.assertEqual(objstr(t, indent_level=1, exclude=['pos2', 'pos3']), expected)

    def test_include_exclude_mix(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        output = objstr(t, include=['pos1', 'pos2'], exclude=['pos2', 'pos3'])
        self.assertIn("pos1", output)
        self.assertNotIn("pos2", output)
        self.assertNotIn("pos3", output)

    def test_multiline(self):
        n = ObjTest({"name": "Apple", "age": 10})
        m = ObjTest({"lst": [1, 2, n]})
        actual = objstr(m)
        self.assertEqual(actual.count("\n"), 9)

    def test_wo_attr(self):
        e = random._random.Random()
        actual = objstr(e)
        self.assertTrue(len(actual) > 0)

    def test_full_match(self):
        f = ObjTest({"give": "strGive", "curve": "strCurve", "head": "strHead"})
        actual = objstr(f, include=['.*e'])
        self.assertIn("give", actual)
        self.assertIn("curve", actual)
        self.assertNotIn("head", actual)

    def test_add_match(self):
        t = ObjTest({"xyz": "xyzVal", "xyzz": "xyzzVal", "xyzxz": "xyzxzVal"})
        actual = objstr(t, include=['xyz+'])
        self.assertIn("xyz", actual)
        self.assertIn("xyzz", actual)
        self.assertNotIn("xyzxz", actual)

    def test_nested_match(self):
        child = ObjTest({"x": "x_val", "y": "y_val"})
        parent = ObjTest({"x": "x_child_val", "y": "y_child_val", "child": child})
        s = objstr(parent, exclude=["x"])
        self.assertNotIn("x_child_val", s)
        self.assertIn("y_child_val", s)
        lst = [child, parent]
        s = objstr(lst, exclude=["x"])
        self.assertNotIn("x_child_val", s)
        self.assertNotIn("x_val", s)
        self.assertIn("y_child_val", s)
        self.assertIn("y_val", s)
