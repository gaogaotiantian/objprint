# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
import unittest
from objprint import objstr


class C:
    pass

class Car(object):
    def __init__(self):
        self.number = 1249
    def run(self):
        print("my car can run!")

class InExclude:
    def __init__(self):
        self.a = "in"
        self.b = "out"
        self.c = "ex"

class testObj:
    def __init__(self):
        self.name = "Andy"
        self.car = Car()

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
            ({"Number": 1, "Letter": 'a'}, "{'Number': 1, 'Letter': 'a'}")
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

    def test_FunctionType(self):
        self.assertEqual("<function run>", objstr(Car.run))

    def test_include(self):
        t = InExclude()
        expected = "<InExclude\n  .a = 'in'\n>"
        self.assertEqual(objstr(t, include=['a']), expected)

    def test_exclude(self):
        t = InExclude()
        expected = "<InExclude\n  .a = 'in'\n>"
        self.assertEqual(objstr(t, exclude=['b','c']), expected)

    #TODO:
    def test_str(self):
        t = testObj()
        expected = "<testObj\n  .name = 'Andy',\n  .car = <Car\n    .number = 1249\n  >\n>"
        self.assertEqual(objstr(t), expected)