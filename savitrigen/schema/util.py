import re
from dataclasses import is_dataclass, asdict as std_asdict

def asdict(obj):
    return {
        **std_asdict(obj),
        **{
            a: getattr(obj, a)
            for a in getattr(obj, '__add_to_dict__', [])
        }
    }

def snake_to_camel(what:str) -> str:
    def replace(match):
        g = match.group(1)
        return g[0].upper() + g[1:]

    return re.sub(r'_(\w)', replace, what)

def dataclass_to_dict(a, convert_casing=False):
    if not a:
        return None

    res = {}
    for k, v in std_asdict(a).items():
        if v is None or k[0] == '_':
            continue

        if convert_casing:
            k = snake_to_camel(k)

        res[k] = dataclass_to_dict(v) \
            if is_dataclass(v) \
            else v

    return res

