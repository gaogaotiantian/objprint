# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/objprint/blob/master/NOTICE.txt

import ast
import inspect
import io
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

        return ast.get_source_segment(source, node)
