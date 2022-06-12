import pathlib
import shutil

class Cache(object):
    _path:str = './.savitricache'

    def __init__(self):
        path = pathlib.Path(self._path)

        if not path.exists():
            shutil.copytree(
                './source',
                str(path)
            )

    def create(self, trees:list):
        for tree in trees:
            tree.set_on_cache(True)
            tree.set_silent(True)
            tree.create()
