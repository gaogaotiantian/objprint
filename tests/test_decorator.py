# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import io
from contextlib import redirect_stdout

from objprint import add_objprint
from objprint import op
from .objtest import ObjprintTestCase


@add_objprint
class DecoratedClass:
    def __init__(self):
        self.name = "Lisa"
        self.age = 19


class NotDecorated:
    def __init__(self):
        self.name = "Lisa"
        self.age = 19


@add_objprint(include=['color1', 'color2'])
class TestWrapper:
    def __init__(self):
        self.color1 = "red"
        self.color2 = "blue"
        self.color3 = "yellow"


class TestDecorator(ObjprintTestCase):
    def test_two_class(self):
        actual = []
        with io.StringIO() as buf, redirect_stdout(buf):
            print(DecoratedClass())
            output = buf.getvalue()
            split_line_dec = output.splitlines()
            actual = split_line_dec[1:]

        expected = []
        with io.StringIO() as buf, redirect_stdout(buf):
            op(NotDecorated())
            expect = buf.getvalue()
            split_line_nodec = expect.splitlines()
            expected = split_line_nodec[1:]

        self.assertEqual(expected, actual)

    def test_single_class(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            print(DecoratedClass())
            output = buf.getvalue()

        with io.StringIO() as buf, redirect_stdout(buf):
            op(DecoratedClass())
            expected = buf.getvalue()

        self.assertEqual(expected, output)

    def test_wrapper(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            print(TestWrapper())
            output = buf.getvalue()

        with io.StringIO() as buf, redirect_stdout(buf):
            op(TestWrapper(), include=['color1', 'color2'])
            expected = buf.getvalue()

        self.assertEqual(output, expected)
