import pathlib
import contextlib
import logging
import typing
from shutil import copy
from string import Template
from multipledispatch import dispatch
from diff_match_patch import diff_match_patch as Diff

class PathlibWrapper(object):
    def __init__(self, silent:bool=False):
        self.silent = silent
        self.on_cache = False
        self.logger = logging.getLogger('path')
        self.parent_dir = None
        self.dmp = Diff()

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
        path = self._get_path(dirname)
        with contextlib.suppress(FileExistsError):
            path.mkdir(parents=True)
            if not self.silent:
                self.logger.info('MKDIR %s', dirname)
        return path

    def copy_file(self, src:str, dest:str) -> pathlib.Path:
        res = copy(src, '{}/{}'.format(self.parent_dir, dest))
        return self._get_path(res)

    def read_file(self, file:typing.Union[str, pathlib.Path]) -> str:
        path = self._get_path(file)
        return path.read_text()

    def _write_file(self, file:typing.Union[pathlib.PosixPath, str], content:str, patch=True) -> pathlib.Path:
        path = self._get_path(file)

        if not self.on_cache and path.exists():
            cached_path = str(path).replace('source/', '.savitricache/', 1)
            cached_path = pathlib.Path(cached_path)

            if cached_path.exists():
                cached = cached_path.read_text()
                patches = self.dmp.patch_make(cached, content)
                content, _ = self.dmp.patch_apply(patches, path.read_text())

        path.write_bytes(content.encode())
        if not self.silent:
            self.logger.info('WRITE %s', file)
        return path

    @dispatch(pathlib.PosixPath, str)
    def write_file(self, *args, **kwargs) -> pathlib.Path:
        return self._write_file(*args, **kwargs)

    @dispatch(pathlib.PosixPath, Template, dict)
    def write_file(self, fname:pathlib.PosixPath, template:Template, replacements:dict) -> pathlib.Path:
        return self._write_file(fname, template.substitute(**replacements))

    @dispatch(pathlib.PosixPath, Template, dict, dict)
    def write_file(self, fname:pathlib.PosixPath, template:Template, fallback:dict, replacements:dict) -> pathlib.Path:
        return self._write_file(fname, template.substitute(fallback, **replacements))
