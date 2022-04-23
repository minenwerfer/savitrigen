import pathlib
import contextlib
import logging

class PathlibWrapper(object):
    def __init__(self):
        self.logger = logging.getLogger('path')
        self.parent_dir = None

    def _get_path(self, path) -> pathlib.Path:
        if isinstance(path, pathlib.Path):
            return path
        return pathlib.Path(path)

    @contextlib.contextmanager
    def change_dir(self, new_dir:str):
        previous_dir = self.parent_dir
        self.parent_dir = new_dir

        try:
            yield
        finally:
            self.parent_dir = previous_dir

    def make_dir(self, dirname:str) -> pathlib.Path:
        self.logger.info('MKDIR %s', dirname)
        path = self._get_path(dirname)
        path.mkdir(parents=True)
        return path

    def write_file(self, fname:str, content:str) -> pathlib.Path:
        self.logger.info('WRITE %s', fname)
        path = self._get_path(fname)
        path.write_bytes(content.encode())
        return path
