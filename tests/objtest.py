# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import unittest
import objprint


class ObjTest:
    def __init__(self, attrs):
        for key, value in attrs.items():
            setattr(self, key, value)


class ObjprintTestCase(unittest.TestCase):
    def setUp(self):
        objprint.config(color=False)
