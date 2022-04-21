import json
from savitrigen.path import PathlibWrapper

def TreeClass(layer:str, scope:str=None):
    def decorator(cls):
        cls.layer = layer
        cls.scope = scope
        class TreeClass(cls, Tree):
            pass
        return TreeClass
    return decorator

class Tree(object):
    path = PathlibWrapper()

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def json_dumps(what:object) -> str:
        return json.dumps(what, indent=4)
