# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import random
from objprint import objstr, config
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
        obj = ObjTest({})
        self.assertNotIn("\n", objstr(obj))

    def test_get_ellipsis(self):
        obj = ObjTest({})
        self.assertRegex(objstr(obj, depth=0), r"<ObjTest 0x[0-9a-fA-F]* ... >")

    def test_None(self):
        self.assertEqual('None', objstr(None))

    def test_function_type(self):
        def run(self):
            print("my car can run!")
        obj = ObjTest({"brand": "a", "function": run})
        self.assertEqual("<function run>", objstr(obj.function))

    def test_id(self):
        obj = ObjTest({})
        obj_id = id(obj)
        self.assertIn(hex(obj_id), objstr(obj, color=True))
        self.assertIn(hex(obj_id), objstr(obj, color=False))

    def test_attr_pattern(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "other3": "ex"})
        output = objstr(t, attr_pattern=r"pos.")
        self.assertIn("pos1", output)
        self.assertIn("pos2", output)
        self.assertNotIn("other3", output)
        with self.assertRaises(TypeError):
            output = objstr(t, attr_pattern=[r"pos."])

    def test_include(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        output = objstr(t, include=['pos1'])
        self.assertIn("pos1", output)
        self.assertNotIn("pos2", output)
        self.assertNotIn("pos3", output)
        with self.assertRaises(TypeError):
            output = objstr(t, include="pos1")

    def test_exclude(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        output = objstr(t, exclude=['pos2', 'pos3'])
        self.assertIn("pos1", output)
        self.assertNotIn("pos2", output)
        self.assertNotIn("pos3", output)
        with self.assertRaises(TypeError):
            output = objstr(t, exclude="pos1")

    def test_exclude_indent(self):
        t = ObjTest({"pos1": "in", "pos2": "out", "pos3": "ex"})
        expected = r"<ObjTest 0x[0-9a-fA-F]*\n  .pos1 = 'in'\n>"
        self.assertRegex(objstr(t, exclude=['pos2', 'pos3']), expected)

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

    def test_honor_existing(self):
        class T:
            def __init__(self):
                self.abc = "xyz"

            def __str__(self):
                return "lol"

        t = T()
        s = objstr(t)
        self.assertIn("lol", s)
        s = objstr(t, honor_existing=False)
        self.assertNotIn("lol", s)
        self.assertIn("abc", s)
        self.assertIn("xyz", s)

    def test_color(self):
        # objstr should return string without color
        # even if the global config sets color to True
        config(color=True)
        s = objstr(ObjTest({"a": 1}))
        self.assertNotIn("\033", s)
        s = objstr(ObjTest({"a": 1}), color=True)
        self.assertIn("\033", s)
        config(color=False)

    def test_recursion(self):
        t1 = ObjTest({})
        t2 = ObjTest({"t1": t1})
        t2.t1.t2 = t2
        s = objstr(t2)
        self.assertIn("...", s)
        self.assertEqual(s.count("t2"), 1)
        s = objstr(t2, skip_recursion=False, depth=6)
        self.assertEqual(s.count("t2"), 3)
