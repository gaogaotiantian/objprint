# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import unittest
from objprint import objstr


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
