# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt

import ast
import inspect
import io
import sys
import tokenize
from .executing import Source


class FrameAnalyzer:
    def __init__(self):
        pass

    def get_args(self, frame):
        func_call_str = self.get_executing_function_call_str(frame)
        if func_call_str is None:
            return None
        func_call_io = io.StringIO(func_call_str)
        depth = 0
        args = []
        curr_arg = ""
        last_pos = (0, 0)
        for token in tokenize.generate_tokens(func_call_io.readline):
            if depth == 0 and token.string == "(":
                depth = 1
            elif depth == 1 and token.string == ")":
                args.append(curr_arg.strip())
                break
            elif depth == 1 and token.string == ",":
                args.append(curr_arg.strip())
                curr_arg = ""
            elif depth >= 1:
                if token.string in "([{":
                    depth += 1
                elif token.string in ")]}":
                    depth -= 1
                if depth >= 1 and token.type != tokenize.NL:
                    if token.start[0] != last_pos[0] or token.start[1] - last_pos[1] > 0:
                        curr_arg += f" {token.string}"
                    else:
                        curr_arg += token.string
            last_pos = token.end
        return args

    def get_executing_function_call_str(self, frame):
        node = Source.executing(frame).node
        if node is None:
            return None
        try:
            source = inspect.getsource(inspect.getmodule(frame))
        except OSError:
            return None

        if sys.version_info < (3, 8):
            return self.get_source_segment3637(source, node)
        else:
            return ast.get_source_segment(source, node)

    def get_source_segment3637(self, source, node):
        if node.lineno is None or node.col_offset is None:  # pragma: no cover
            return None
        lineno = node.lineno - 1
        lines = self._splitlines_no_ff(source)
        first_line = lines[lineno].encode()[node.col_offset:].decode()
        lines = lines[lineno + 1:]
        lines.insert(0, first_line)
        return "".join(lines)

    def _splitlines_no_ff(self, source):  # pragma: no cover
        """Split a string into lines ignoring form feed and other chars.
        This mimics how the Python parser splits source code.

        :copyright: Copyright 2008 by Armin Ronacher.
        :license: Python License.
        from https://github.com/python/cpython/blob/main/Lib/ast.py
        license: https://github.com/python/cpython/blob/main/LICENSE
        """
        idx = 0
        lines = []
        next_line = ''
        while idx < len(source):
            c = source[idx]
            next_line += c
            idx += 1
            # Keep \r\n together
            if c == '\r' and idx < len(source) and source[idx] == '\n':
                next_line += '\n'
                idx += 1
            if c in '\r\n':
                lines.append(next_line)
                next_line = ''

        if next_line:
            lines.append(next_line)
        return lines
