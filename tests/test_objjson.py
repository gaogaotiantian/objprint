# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import json
from objprint import objjson
from .objtest import ObjTest, ObjprintTestCase


class TestObjJson(ObjprintTestCase):
    def test_list(self):
        lsts = (
            [],
            [1, 2],
            [1, 'a'],
            [123, 'a' * 100]
        )
        for obj in lsts:
            self.assertEqual(json.dumps(objjson(obj)), json.dumps(obj))

    def test_tuple(self):
        lsts = (
            tuple(),
            (1, 2),
            (1, 'a')
        )
        for obj in lsts:
            self.assertEqual(json.dumps(objjson(obj)), json.dumps(obj))

    def test_dict(self):
        lsts = (
            {},
            {"Age": "19"},
            {"Number": 1, "Letter": 'a'}
        )
        for obj in lsts:
            self.assertEqual(json.dumps(objjson(obj)), json.dumps(obj))

    def test_recursive(self):
        a = []
        b = [a]
        a.append(b)
        with self.assertRaises(ValueError):
            _ = objjson(a)

    def test_simpleobj(self):
        t = ObjTest({"a": 1, "b": 3.3})
        self.assertEqual(objjson(t), {".type": "ObjTest", "a": 1, "b": 3.3})

    def test_duplicate_obj(self):
        a = [1, 2]
        t = ObjTest({"lst1": a, "lst2": a})
        self.assertEqual(objjson(t), {".type": "ObjTest", "lst1": a, "lst2": a})
