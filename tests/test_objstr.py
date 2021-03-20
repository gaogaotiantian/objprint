# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
import unittest
import random
from objprint import objstr


class C:
    pass


class Car(object):
    def run(self):
        print("my car can run!")


class InExclude:
    def __init__(self):
        self.a = "in"
        self.b = "out"
        self.c = "ex"


class B:
    def __init__(self):
        self.name = "apple"
        self.age = 10


class Multiline:
    def __init__(self):
        self.lst = [1, 2, B()]


class TestObjStr(unittest.TestCase):
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
        self.assertEqual("<C ... >", objstr(C(), 5))

    def test_None(self):
        self.assertEqual('None', objstr(None))

    def test_function_type(self):
        self.assertEqual("<function run>", objstr(Car.run))

    def test_include(self):
        t = InExclude()
        expected = "<InExclude\n  .a = 'in'\n>"
        self.assertEqual(objstr(t, include=['a']), expected)

    def test_exclude(self):
        t = InExclude()
        expected = "<InExclude\n  .a = 'in'\n>"
        self.assertEqual(objstr(t, exclude=['b', 'c']), expected)

    def test_multiline(self):
        m = Multiline()
        actual = objstr(m)
        self.assertEqual(actual.count("\n"), 9)

    def test_wo_attr(self):
        e = random._random.Random()
        actual = objstr(e)
        self.assertTrue(len(actual) > 0)
