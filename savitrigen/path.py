import pathlib
import logging

class PathlibWrapper(object):
    def __init__(self):
        self.logger = logging.getLogger('path')

    def make_dir(self, dirname:str) -> pathlib.Path:
        self.logger.info('MKDIR %s', dirname)
        path = pathlib.Path(dirname)
        path.mkdir()
        return Path

    def write_file(self, fname:str, content:str) -> pathlib.Path:
        self.logger.info('WRITE %s', fname)
        path = pathlib.Path(fname)
        path.write_bytes(content.encode())
        return path
