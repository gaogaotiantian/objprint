# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


from .objprint import ObjPrint


def add_objprint(orig_class):
    op = ObjPrint()

    def __str__(self):
        return op.objstr(self)

    orig_class.__str__ = __str__
    return orig_class
