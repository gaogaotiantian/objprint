# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
from contextlib import redirect_stdout

from objprint import config, objprint
from .objtest import ObjTest, ObjprintTestCase


class TestConfig(ObjprintTestCase):
    def test_config_none_exist(self):
        self.assertRaises(ValueError, lambda: config(height=50))

    def test_config_wrong_type(self):
        self.assertRaises(TypeError, lambda: config(exclude=50))

    def test_config_element(self):
        config(elements=2)
        e = ObjTest({"first": 1, "second": 2, "third": 3})
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(e)
            output = buf.getvalue()
        self.assertIn("first", output)
        self.assertIn("second", output)
        self.assertNotIn("third", output)
        config(elements=-1)
