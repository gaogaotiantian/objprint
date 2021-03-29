# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
import os
from contextlib import redirect_stdout
from objprint import objprint, objstr, config, install
from .objtest import ObjprintTestCase


class A:
    pass


class TestBasic(ObjprintTestCase):
    def test_print(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            objprint(A())
            self.assertTrue(len(buf.getvalue()) > 0)

    def test_print_to_file(self):
        fname = "./test.txt"
        with open(fname, "w") as f:
            objprint(A(), file=f)
        with open(fname, "r") as f:
            self.assertGreater(len(f.read()), 0)
        os.remove(fname)

    def test_print_to_buffer(self):
        with io.StringIO() as buf:
            objprint(A(), file=buf)
            self.assertGreater(len(buf.getvalue()), 0)

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
