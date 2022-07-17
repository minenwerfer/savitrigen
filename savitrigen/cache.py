import pathlib
import shutil

class Cache(object):
    _path:str = './.savitricache'

    def __init__(self):
        path = pathlib.Path(self._path)

        def ignore_files(dirn, files):
            return [
                name
                for name in files
                if not pathlib.Path('{}/{}'.format(dirn, name)).is_dir()
            ]

        if not path.exists():
            shutil.copytree(
                './source',
                str(path),
                ignore=ignore_files,
                symlinks=False
            )

    def create(self, trees:list):
        for tree in trees:
            tree.set_on_cache(True)
            tree.set_silent(True)
            tree.create()
