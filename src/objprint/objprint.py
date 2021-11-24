# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt


import json
import re
from types import FunctionType
from .color_util import COLOR, set_color


class _PrintConfig:
    indent = 2
    depth = 100
    width = 80
    color = True
    label = []
    elements = -1
    exclude = []
    include = []
    skip_recursion = True
    honor_existing = True

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key):
                if isinstance(val, type(getattr(self, key))):
                    setattr(self, key, val)
                else:
                    raise TypeError(f"Wrong type for {key} - {val}")
            else:
                raise ValueError(f"{key} is not configurable")

    def set(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(_PrintConfig, key):
                if isinstance(val, type(getattr(_PrintConfig, key))):
                    setattr(_PrintConfig, key, val)
                else:
                    raise TypeError(f"Wrong type for {key} - {val}")
            else:
                raise ValueError(f"{key} is not configurable")

    def overwrite(self, **kwargs):
        ret = _PrintConfig(**kwargs)
        return ret


class ObjPrint:
    def __init__(self):
        self._configs = _PrintConfig()

        self.indicator_map = {
            list: "[]",
            tuple: "()",
            dict: "{}",
            set: "{}"
        }
        self._sys_print = print

    def objprint(self, *objs, file=None, format="string", **kwargs):
        if format == "json":
            for obj in objs:
                self._sys_print(json.dumps(self.objjson(obj), **kwargs))
        else:
            # Force color with cfg as if color is not in cfg, objstr will default to False
            cfg = self._configs.overwrite(**kwargs)
            kwargs["color"] = cfg.color
            for obj in objs:
                self._sys_print(self.objstr(obj, **kwargs), file=file)

    def objstr(self, obj, **kwargs):
        # If no color option is specified, don't use color
        if "color" not in kwargs:
            kwargs["color"] = False
        cfg = self._configs.overwrite(**kwargs)
        memo = set() if cfg.skip_recursion else None
        return self._objstr(obj, memo, indent_level=0, cfg=cfg)

    def _objstr(self, obj, memo, indent_level, cfg):
        # If it's builtin type, return it directly
        if isinstance(obj, str):
            return f"'{obj}'"
        elif isinstance(obj, int) or \
                isinstance(obj, float) or \
                obj is None:
            return str(obj)
        elif isinstance(obj, FunctionType):
            return f"<function {obj.__name__}>"

        # Otherwise we may need to unpack it. Figure out if we should do that first
        if (memo is not None and id(obj) in memo) or \
                (cfg.depth is not None and indent_level >= cfg.depth):
            return self._get_ellipsis(obj, cfg)

        if memo is not None:
            memo = memo.copy()
            memo.add(id(obj))

        if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            elems = (f"{self._objstr(val, memo, indent_level + 1, cfg)}" for val in obj)
        elif isinstance(obj, dict):
            elems = (
                f"{self._objstr(key, None, indent_level + 1, cfg)}: {self._objstr(val, memo, indent_level + 1, cfg)}"
                for key, val in sorted(obj.items())
            )
        else:
            # It's an object

            # If it has __str__ or __repr__ overloaded, honor that
            if cfg.honor_existing and \
                    (obj.__class__.__str__ is not object.__str__ or obj.__class__.__repr__ is not object.__repr__):
                # Make sure we indent properly
                s = str(obj)
                lines = s.split("\n")
                lines[1:] = [self.add_indent(line, indent_level, cfg) for line in lines[1:]]
                return "\n".join(lines)
            return self._get_custom_object_str(obj, memo, indent_level, cfg)

        return self._get_pack_str(elems, obj, indent_level, cfg)

    def objjson(self, obj):
        return self._objjson(obj, set())

    def _objjson(self, obj, memo):
        """
        return a jsonifiable object from obj
        """
        if isinstance(obj, (str, int, float)) or obj is None:
            return obj

        if id(obj) in memo:
            raise ValueError("Can't jsonify a recursive object")

        memo.add(id(obj))

        if isinstance(obj, (list, tuple)):
            return [self._objjson(elem, memo.copy()) for elem in obj]

        if isinstance(obj, dict):
            return {key: self._objjson(val, memo.copy()) for key, val in obj.items()}

        # For generic object
        ret = {".type": type(obj).__name__}

        if hasattr(obj, "__dict__"):
            for key, val in obj.__dict__.items():
                ret[key] = self._objjson(val, memo.copy())

        return ret

    def _get_custom_object_str(self, obj, memo, indent_level, cfg):

        def _get_line(key):
            val = self._objstr(obj.__dict__[key], memo, indent_level + 1, cfg)
            if cfg.label and any(re.fullmatch(pattern, key) is not None for pattern in cfg.label):
                return set_color(f".{key} = {val}", COLOR.YELLOW)
            elif cfg.color:
                return f"{set_color('.'+key, COLOR.GREEN)} = {val}"
            else:
                return f".{key} = {val}"

        if hasattr(obj, "__dict__"):
            keys = []
            for key in obj.__dict__.keys():
                if cfg.include:
                    if not any((re.fullmatch(pattern, key) is not None for pattern in cfg.include)):
                        continue
                if cfg.exclude:
                    if any((re.fullmatch(pattern, key) is not None for pattern in cfg.exclude)):
                        continue
                keys.append(key)

            elems = (_get_line(key) for key in sorted(keys))
        else:
            return str(obj)

        return self._get_pack_str(elems, obj, indent_level, cfg)

    def config(self, **kwargs):
        self._configs.set(**kwargs)

    def install(self, name="op"):
        import builtins
        builtins.__dict__[name] = self.objprint

    def add_indent(self, line, indent_level, cfg):
        if isinstance(line, str):
            return " " * (indent_level * cfg.indent) + line
        return [" " * (indent_level * cfg.indent) + ll for ll in line]

    def _get_header_footer(self, obj, cfg):
        obj_type = type(obj)
        if obj_type in self.indicator_map:
            indicator = self.indicator_map[obj_type]
            return indicator[0], indicator[1]
        else:
            if cfg.color:
                return set_color(f"<{obj_type.__name__} {hex(id(obj))}", COLOR.CYAN), set_color(">", COLOR.CYAN)
            else:
                return f"<{obj_type.__name__}", ">"

    def _get_ellipsis(self, obj, cfg):
        header, footer = self._get_header_footer(obj, cfg)
        return f"{header} ... {footer}"

    def _get_pack_str(self, elems, obj, indent_level, cfg):
        """
        :param elems generator: generator of string elements to pack together
        :param obj_type type: object type
        :param indent_level int: current indent level
        """
        header, footer = self._get_header_footer(obj, cfg)

        if cfg.elements == -1:
            elems = list(elems)
        else:
            first_elems = []
            try:
                for _ in range(cfg.elements):
                    first_elems.append(next(elems))
            except StopIteration:
                pass
            if next(elems, None) is not None:
                first_elems.append("...")
            elems = first_elems

        multiline = False
        if len(header) > 1 and len(elems) > 0:
            # If it's not built in, always do multiline
            multiline = True
        elif any(("\n" in elem for elem in elems)):
            # Has \n, need multiple mode
            multiline = True
        elif cfg.width is not None and sum((len(elem) for elem in elems)) > cfg.width:
            multiline = True

        if multiline:
            s = ",\n".join(self.add_indent(elems, indent_level + 1, cfg))
            return f"{header}\n{s}\n{self.add_indent('', indent_level, cfg)}{footer}"
        else:
            s = ", ".join(elems)
            return f"{header}{s}{footer}"
