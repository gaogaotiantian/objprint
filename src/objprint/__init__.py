# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt

__version__ = "0.2.3"


from .objprint import ObjPrint
from .decorator import add_objprint

_objprint = ObjPrint()
op = objprint = _objprint
objstr = _objprint.objstr
objjson = _objprint.objjson
config = _objprint.config
install = _objprint.install


__all__ = [
    "op",
    "objstr",
    "objjson",
    "config",
    "add_objprint",
    "install"
]
