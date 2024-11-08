# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import functools
from typing import Callable, Optional, Type, TypeVar, Set, Union, overload


T = TypeVar("T", bound=Type)


@overload
def add_objprint(
        orig_class: None = None,
        format: str = "string", **kwargs) -> Callable[[T], T]:
    ...  # pragma: no cover


@overload
def add_objprint(
        orig_class: T,
        format: str = "string", **kwargs) -> T:
    ...  # pragma: no cover


def add_objprint(
        orig_class: Optional[T] = None,
        format: str = "string", **kwargs) -> Union[T, Callable[[T], T]]:

    from . import _objprint

    if format == "json":
        import json

        def __str__(self) -> str:
            return json.dumps(_objprint.objjson(self), **kwargs)
    else:
        def __str__(self) -> str:
            cfg = _objprint._configs.overwrite(**kwargs)
            memo: Optional[Set] = set() if cfg.skip_recursion else None
            return _objprint._get_custom_object_str(self, memo, indent_level=0, cfg=cfg)

    if orig_class is None:
        def wrapper(cls: T) -> T:
            cls.__str__ = functools.wraps(cls.__str__)(__str__)  # type: ignore
            return cls
        return wrapper
    else:
        orig_class.__str__ = functools.wraps(orig_class.__str__)(__str__)  # type: ignore
        return orig_class
