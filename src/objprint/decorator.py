# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


def add_objprint(orig_class=None, format="string", **kwargs):

    from . import _objprint

    if format == "json":
        import json

        def __str__(self):
            return json.dumps(_objprint.objjson(self), **kwargs)
    else:
        def __str__(self):
            cfg = _objprint._configs.overwrite(**kwargs)
            memo = set() if cfg.skip_recursion else None
            return _objprint._get_custom_object_str(self, memo, indent_level=0, cfg=cfg)

    if orig_class is None:
        def wrapper(cls):
            cls.__str__ = __str__
            return cls
        return wrapper
    else:
        orig_class.__str__ = __str__
        return orig_class
