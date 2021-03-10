# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
import unittest
from contextlib import redirect_stdout
from objprint import objprint, objstr, config, install


class A:
    pass


class TestBasic(unittest.TestCase):
    def test_print(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(A())
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_str(self):
        s = objstr(A())
        self.assertTrue(len(s) > 0)

    def test_config(self):
        config(indent=4)
        config(indent=2)

    def test_install(self):
        install("my_objprint")
        with io.StringIO() as buf, redirect_stdout(buf):
            my_objprint(A())  # noqa: F821
            self.assertTrue(len(buf.getvalue()) > 0)
