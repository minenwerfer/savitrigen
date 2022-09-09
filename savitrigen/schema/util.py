import re
from dataclasses import is_dataclass

def dataclass_to_dict(a):
    res = {}
    for k, v in a.__dict__.items():
        if v is None:
            continue

        if k[0] == '_':
            k = k[1:]

        res[k] = dataclass_to_dict(v) \
            if is_dataclass(v) \
            else v

    return res

def snake_to_camel(what:str) -> str:
    def replace(match):
        g = match.group(1)
        return g[0].upper() + g[1:]

    return re.sub(r'_(\w)', replace, what)
