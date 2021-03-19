# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


def add_objprint(orig_class=None, include=[], exclude=[]):

    def __str__(self):
        return _objprint._get_custom_object_str(self, indent_level=0, include=include, exclude=exclude)

    from . import _objprint

    if orig_class is None:
        def wrapper(cls):
            cls.__str__ = __str__
            return cls
        return wrapper
    else:
        orig_class.__str__ = __str__
        return orig_class
